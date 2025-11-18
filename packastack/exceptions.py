# Copyright (C) 2025 Canonical Ltd
#
# License granted by Canonical Limited
#
# SPDX-License-Identifier: GPL-3.0-only
#
# This file is part of PackaStack. See LICENSE for details.

"""Custom exceptions for packastack."""


class PackastackError(Exception):
    """Base exception for all packastack errors."""

    pass  # pragma: no cover


class RepositoryError(PackastackError):
    """Raised when git repository operations fail."""

    pass  # pragma: no cover


class LaunchpadError(PackastackError):
    """Raised when Launchpad API operations fail."""

    pass  # pragma: no cover


class ImporterError(PackastackError):
    """Raised when tarball import operations fail."""

    pass  # pragma: no cover


class DebianError(PackastackError):
    """Raised when Debian packaging operations fail."""

    pass  # pragma: no cover


class NetworkError(PackastackError):
    """Raised when network operations fail."""

    pass  # pragma: no cover


class DiskSpaceError(PackastackError):
    """Raised when disk space is insufficient."""

    pass  # pragma: no cover
