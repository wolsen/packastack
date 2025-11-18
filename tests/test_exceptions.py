# Copyright (C) 2025 Canonical Ltd
#
# License granted by Canonical Limited
#
# SPDX-License-Identifier: GPL-3.0-only
#
# This file is part of PackaStack. See LICENSE for details.

"""Tests for custom exceptions."""

from packastack.exceptions import (
    DebianError,
    DiskSpaceError,
    ImporterError,
    LaunchpadError,
    NetworkError,
    PackastackError,
    RepositoryError,
)


def test_packastack_error_is_base():
    """Test that PackastackError is the base exception."""
    error = PackastackError("test error")
    assert isinstance(error, Exception)
    assert str(error) == "test error"


def test_repository_error_inherits_from_base():
    """Test RepositoryError inherits from PackastackError."""
    error = RepositoryError("repo error")
    assert isinstance(error, PackastackError)
    assert isinstance(error, Exception)


def test_launchpad_error_inherits_from_base():
    """Test LaunchpadError inherits from PackastackError."""
    error = LaunchpadError("launchpad error")
    assert isinstance(error, PackastackError)


def test_importer_error_inherits_from_base():
    """Test ImporterError inherits from PackastackError."""
    error = ImporterError("importer error")
    assert isinstance(error, PackastackError)


def test_debian_error_inherits_from_base():
    """Test DebianError inherits from PackastackError."""
    error = DebianError("debian error")
    assert isinstance(error, PackastackError)


def test_network_error_inherits_from_base():
    """Test NetworkError inherits from PackastackError."""
    error = NetworkError("network error")
    assert isinstance(error, PackastackError)


def test_disk_space_error_inherits_from_base():
    """Test DiskSpaceError inherits from PackastackError."""
    error = DiskSpaceError("disk space error")
    assert isinstance(error, PackastackError)
