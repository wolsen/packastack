# Copyright (C) 2025 Canonical Ltd
#
# License granted by Canonical Limited
#
# SPDX-License-Identifier: GPL-3.0-only
#
# This file is part of PackaStack. See LICENSE for details.

import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest

from packastack.exceptions import DebianError
from packastack.package.uscan import Uscan


@pytest.fixture
def serve_html():
    """Start a lightweight HTTP server that serves fixed HTML content."""
    servers: list[tuple[ThreadingHTTPServer, threading.Thread]] = []

    def _serve(body: str) -> str:
        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):  # noqa: N802 - HTTP verb naming
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                self.wfile.write(body.encode("utf-8"))

            def log_message(self, format, *args):  # noqa: A003 - signature required
                return

        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        servers.append((server, thread))

        host, port = server.server_address
        return f"http://{host}:{port}"

    yield _serve

    for server, thread in servers:
        server.shutdown()
        thread.join()


def test_scan_identifies_latest_release(tmp_path: Path, serve_html):
    """Ensure the scanner returns the newest upstream version."""
    html = """
    <html><body>
    <a href="pkg-1.0.0.tar.gz">1.0.0</a>
    <a href="pkg-2.1.0.tar.gz">2.1.0</a>
    <a href="pkg-2.0.0.tar.gz">2.0.0</a>
    </body></html>
    """
    base_url = serve_html(html)

    watch = tmp_path / "watch"
    watch.write_text(
        f"""version=4
{base_url}/ pkg-(?P<version>[0-9\\.]+)\\.tar\\.gz
""",
        encoding="utf-8",
    )

    result = Uscan(watch).scan()

    assert {m.version for m in result.matches} == {"1.0.0", "2.0.0", "2.1.0"}
    assert result.latest
    assert result.latest.version == "2.1.0"
    assert result.latest.url.endswith("pkg-2.1.0.tar.gz")


def test_scan_applies_mangles(tmp_path: Path, serve_html):
    """uversionmangle, downloadurlmangle, and filenamemangle are respected."""
    html = """
    <html><body>
    <a href="downloads/pkg-2.0rc1.tar.gz">Release</a>
    </body></html>
    """
    base_url = serve_html(html)

    watch = tmp_path / "watch"
    watch.write_text(
        f"""version=4
opts=uversionmangle=s/rc/~rc/,downloadurlmangle=s/\\.tar\\.gz/.zip/,filenamemangle=s/.+\\/pkg-(.*)\\.tar\\.gz/pkg-$1.orig.tar.gz/ \\
{base_url}/ pkg-(?P<version>[0-9\\.]+rc[0-9]+)\\.tar\\.gz
""",
        encoding="utf-8",
    )

    result = Uscan(watch).scan()
    assert len(result.matches) == 1

    match = result.matches[0]
    assert match.version == "2.0~rc1"
    assert match.url.endswith(".zip")
    assert match.filename == "pkg-2.0rc1.orig.tar.gz"


def test_watch_without_version_raises(tmp_path: Path):
    """watch files must declare a supported version."""
    watch = tmp_path / "watch"
    watch.write_text(
        "opts=uversionmangle=s/rc/~rc/ http://example.invalid pkg-(\\d+)\\.tar\\.gz",
        encoding="utf-8",
    )

    scanner = Uscan(watch)
    with pytest.raises(DebianError):
        _ = scanner.entries
