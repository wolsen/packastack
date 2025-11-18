# Copyright (C) 2025 Canonical Ltd
#
# License granted by Canonical Limited
#
# SPDX-License-Identifier: GPL-3.0-only
#
# This file is part of PackaStack. See LICENSE for details.

"""Base importer class for tarball imports."""

from abc import ABC, abstractmethod
from pathlib import Path

from packastack.exceptions import ImporterError


class BaseImporter(ABC):
    """Abstract base class for tarball importers."""

    def __init__(
        self,
        packaging_repo_path: str,
        upstream_repo_path: str,
        tarballs_dir: str,
        cycle: str,
        releases_repo_path: str,
        *args,
        **kwargs,
    ):
        """
        Initialize base importer.

        Args:
            packaging_repo_path: Path to packaging repository
            upstream_repo_path: Path to upstream repository
            tarballs_dir: Directory for storing tarballs
            cycle: OpenStack cycle name
            releases_repo_path: Path to releases repository
            *args: Additional positional arguments for subclasses
            **kwargs: Additional keyword arguments for subclasses

        Raises:
            ImporterError: If paths don't exist
        """
        self.packaging_repo_path = Path(packaging_repo_path)
        self.upstream_repo_path = Path(upstream_repo_path)
        self.tarballs_dir = Path(tarballs_dir)
        self.cycle = cycle
        self.releases_repo_path = Path(releases_repo_path)

        if not self.packaging_repo_path.exists():
            raise ImporterError(f"Packaging repo not found: {packaging_repo_path}")

        if not self.upstream_repo_path.exists():
            raise ImporterError(f"Upstream repo not found: {upstream_repo_path}")

        if not self.releases_repo_path.exists():
            raise ImporterError(f"Releases repo not found: {releases_repo_path}")

        # Ensure tarballs directory exists
        self.tarballs_dir.mkdir(parents=True, exist_ok=True)

    @abstractmethod
    def get_version(self) -> str:
        """
        Get version to import.

        Returns:
            Upstream version string

        Raises:
            ImporterError: If version cannot be determined
        """
        pass  # pragma: no cover

    @abstractmethod
    def get_tarball(self, version: str) -> Path:
        """
        Get or generate tarball for version.

        Args:
            version: Version to get tarball for

        Returns:
            Path to tarball

        Raises:
            ImporterError: If tarball cannot be obtained
        """
        pass  # pragma: no cover

    @abstractmethod
    def convert_version(self, upstream_version: str) -> str:
        """
        Convert upstream version to Debian version.

        Args:
            upstream_version: Upstream version string

        Returns:
            Debian version string

        Raises:
            ImporterError: If conversion fails
        """
        pass  # pragma: no cover

    def save_gpg_key(self, key_content: str) -> None:
        """
        Save GPG key to debian/upstream/signing-key.asc.

        Args:
            key_content: GPG key content

        Raises:
            ImporterError: If key cannot be saved
        """
        key_file = self.packaging_repo_path / "debian" / "upstream" / "signing-key.asc"

        try:
            key_file.parent.mkdir(parents=True, exist_ok=True)
            key_file.write_text(key_content)
        except Exception as e:
            raise ImporterError(f"Failed to save GPG key: {e}")

    def rename_tarball(
        self, source_path: Path, source_package: str, debian_version: str
    ) -> Path:
        """
        Rename tarball to Debian naming convention.

        Args:
            source_path: Original tarball path
            source_package: Debian source package name
            debian_version: Debian version string

        Returns:
            Path to renamed tarball

        Raises:
            ImporterError: If rename fails
        """
        # Debian tarball naming: <package>_<version>.orig.tar.gz
        dest_name = f"{source_package}_{debian_version}.orig.tar.gz"
        dest_path = self.tarballs_dir / dest_name

        try:
            if source_path != dest_path:
                source_path.rename(dest_path)
            return dest_path
        except Exception as e:
            raise ImporterError(f"Failed to rename tarball: {e}")

    def import_tarball(self) -> str:
        """
        Complete import workflow: get version, tarball, convert, and prepare.

        Returns:
            Debian version string

        Raises:
            ImporterError: If import fails at any stage
        """
        # Get version
        upstream_version = self.get_version()

        # Get tarball
        self.get_tarball(upstream_version)

        # Convert version
        debian_version = self.convert_version(upstream_version)

        return debian_version
