# Copyright (C) 2025 Canonical Ltd
#
# License granted by Canonical Limited
#
# SPDX-License-Identifier: GPL-3.0-only
#
# This file is part of PackaStack. See LICENSE for details.

"""A lightweight, Python implementation of Debian's ``uscan``.

The real ``uscan`` tool reads a ``debian/watch`` file, fetches upstream
release listings, and identifies the newest available tarball.  The
implementation here mirrors the core behaviour needed for automation:

* Parse version 4 ``debian/watch`` entries (including ``opts=`` blocks)
* Fetch the upstream page and apply the supplied regex to discover
  candidate release artifacts
* Apply common mangle directives (``uversionmangle``, ``downloadurlmangle``,
  and ``filenamemangle``)
* Return the discovered matches and the newest upstream version

This module is intentionally conservative and only covers the options we
need today.  It can be extended in the future as new watch-file features
become necessary.
"""

from __future__ import annotations

import re
from collections.abc import Iterable
from dataclasses import dataclass, field
from functools import cmp_to_key
from pathlib import Path
from urllib.parse import urljoin

import requests
from debian.debian_support import version_compare
from requests import Response, Session
from requests.exceptions import RequestException

from packastack.exceptions import DebianError, NetworkError

DEFAULT_USER_AGENT = "packastack-uscan/0.1"


@dataclass
class WatchEntry:
    """Represents a single ``debian/watch`` stanza."""

    url: str
    pattern: re.Pattern[str]
    uversionmangle: list[str] = field(default_factory=list)
    downloadurlmangle: list[str] = field(default_factory=list)
    filenamemangle: list[str] = field(default_factory=list)


@dataclass
class WatchMatch:
    """Represents a discovered upstream artifact."""

    version: str
    url: str
    filename: str


@dataclass
class UscanResult:
    """Holds the matches from scanning a watch file."""

    matches: list[WatchMatch]

    @property
    def latest(self) -> WatchMatch | None:
        """Return the newest upstream match if any."""
        if not self.matches:
            return None

        def _compare(a: WatchMatch, b: WatchMatch) -> int:
            return version_compare(a.version, b.version)

        return max(self.matches, key=cmp_to_key(_compare))


class Uscan:
    """Scan upstream releases described by a ``debian/watch`` file."""

    def __init__(
        self,
        watch_file: str | Path,
        session: Session | None = None,
        timeout: int = 10,
    ):
        """
        Initialize the scanner.

        Args:
            watch_file: Path to the ``debian/watch`` file.
            session: Optional requests session to reuse connections.
            timeout: HTTP timeout in seconds.
        """
        self.watch_file = Path(watch_file)
        if not self.watch_file.exists():
            raise DebianError(f"watch file not found: {self.watch_file}")

        self.session = session or requests.Session()
        self.session.headers.setdefault("User-Agent", DEFAULT_USER_AGENT)
        self.timeout = timeout
        self._entries: list[WatchEntry] | None = None

    @property
    def entries(self) -> list[WatchEntry]:
        """Parsed watch entries."""
        if self._entries is None:
            self._entries = self._parse_watch_file()
        return self._entries

    def scan(self) -> UscanResult:
        """Fetch upstream listings and return discovered artifacts."""
        matches: list[WatchMatch] = []
        for entry in self.entries:
            matches.extend(self._scan_entry(entry))
        return UscanResult(matches)

    def _parse_watch_file(self) -> list[WatchEntry]:
        """Parse the watch file into structured entries."""
        raw = self.watch_file.read_text(encoding="utf-8")
        lines = [line.strip() for line in raw.splitlines() if line.strip()]

        version_line = next(
            (line for line in lines if line.lower().startswith("version=")), None
        )
        if not version_line:
            raise DebianError("watch file missing version declaration (e.g. version=4)")

        version = version_line.split("=", maxsplit=1)[1].strip()
        if version != "4":
            raise DebianError(f"unsupported watch file version: {version}")

        entries: list[str] = []
        buffer = ""
        for line in lines:
            if line.lower().startswith("version="):
                continue
            if line.startswith("#"):
                continue

            # Handle line continuations with trailing backslashes
            if line.endswith("\\"):
                buffer += line[:-1].rstrip() + " "
                continue

            buffer += line
            entries.append(buffer.strip())
            buffer = ""

        parsed_entries = [self._parse_watch_entry(entry) for entry in entries if entry]
        if not parsed_entries:
            raise DebianError("no usable entries found in watch file")
        return parsed_entries

    def _parse_watch_entry(self, entry: str) -> WatchEntry:
        """Parse a single watch entry string."""
        # Entries are whitespace separated once continuations are resolved.
        parts = re.split(r"\s+", entry.strip())
        opts_block = next((p for p in parts if p.startswith("opts=")), None)
        opts = self._parse_opts(opts_block) if opts_block else {}

        # Remove opts=... token so the remaining two tokens are url + pattern
        without_opts = [p for p in parts if not p.startswith("opts=")]
        if len(without_opts) < 2:
            raise DebianError(f"invalid watch entry: {entry}")

        url = without_opts[0]
        pattern = without_opts[1]

        try:
            compiled_pattern: re.Pattern[str] = re.compile(pattern)
        except re.error as exc:
            raise DebianError(f"invalid regex in watch entry: {exc}") from exc

        return WatchEntry(
            url=url,
            pattern=compiled_pattern,
            uversionmangle=self._mangle_list(opts.get("uversionmangle")),
            downloadurlmangle=self._mangle_list(opts.get("downloadurlmangle")),
            filenamemangle=self._mangle_list(
                opts.get("filenamemangle") or opts.get("dversionmangle")
            ),
        )

    @staticmethod
    def _parse_opts(opts_block: str) -> dict[str, str]:
        """Parse the ``opts=`` portion of a watch entry."""
        opts_block = opts_block.removeprefix("opts=").strip()
        if opts_block.startswith('"') and opts_block.endswith('"'):
            opts_block = opts_block[1:-1]
        if not opts_block:
            return {}

        opts: dict[str, str] = {}
        for raw_opt in opts_block.split(","):
            if not raw_opt:
                continue
            if "=" in raw_opt:
                key, value = raw_opt.split("=", maxsplit=1)
                opts[key.strip()] = value.strip()
            else:
                opts[raw_opt.strip()] = ""
        return opts

    @staticmethod
    def _mangle_list(value: str | None) -> list[str]:
        """Split chained mangles into a list."""
        if not value:
            return []
        return [part for part in value.split(";") if part]

    def _scan_entry(self, entry: WatchEntry) -> list[WatchMatch]:
        """Scan a single watch entry."""
        response = self._http_get(entry.url)
        content = response.text

        matches: list[WatchMatch] = []
        for match in entry.pattern.finditer(content):
            version = self._extract_version(match)
            version = self._apply_mangles(version, entry.uversionmangle)

            matched_url = match.group(0)
            download_url = urljoin(
                entry.url, self._apply_mangles(matched_url, entry.downloadurlmangle)
            )

            filename = self._apply_mangles(matched_url, entry.filenamemangle)
            if not filename:
                filename = download_url.rsplit("/", maxsplit=1)[-1]

            matches.append(
                WatchMatch(version=version, url=download_url, filename=filename)
            )

        return matches

    def _http_get(self, url: str) -> Response:
        """Wrapper around HTTP GET with consistent error handling."""
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response
        except RequestException as exc:  # pragma: no cover - exercised in runtime
            raise NetworkError(f"failed to fetch {url}: {exc}") from exc

    @staticmethod
    def _extract_version(match: re.Match[str]) -> str:
        """Best-effort extraction of the upstream version from a regex match."""
        if "version" in match.re.groupindex:
            return match.group("version")

        # Fall back to the first capturing group
        if match.groups():
            return match.group(1)

        raise DebianError(
            "watch regex must expose an upstream version via a named "
            "group 'version' or at least one capturing group"
        )

    @staticmethod
    def _apply_mangles(value: str, mangles: Iterable[str]) -> str:
        """Apply sed-style substitution expressions in order."""
        result = value
        for mangle in mangles:
            result = Uscan._apply_single_mangle(result, mangle)
        return result

    @staticmethod
    def _apply_single_mangle(value: str, mangle: str) -> str:
        """Apply a single sed-style substitution."""
        if not mangle.startswith("s"):
            return value

        sep = mangle[1]
        parts = Uscan._split_unescaped(mangle[2:], sep)
        if len(parts) < 2:
            raise DebianError(f"invalid mangle expression: {mangle}")

        pattern = parts[0]
        replacement = parts[1]
        flags = parts[2] if len(parts) > 2 else ""

        re_flags = re.IGNORECASE if "i" in flags else 0
        count = 0 if "g" in flags else 1
        return re.sub(pattern, replacement, value, count=count, flags=re_flags)

    @staticmethod
    def _split_unescaped(value: str, delimiter: str) -> list[str]:
        """Split a string on a delimiter, ignoring escaped delimiters."""
        parts: list[str] = []
        current: list[str] = []
        escaped = False

        for char in value:
            if escaped:
                current.append(char)
                escaped = False
                continue

            if char == "\\":
                current.append(char)
                escaped = True
                continue

            if char == delimiter:
                parts.append("".join(current))
                current = []
                continue

            current.append(char)

        parts.append("".join(current))
        return parts
