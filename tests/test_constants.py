# Copyright (C) 2025 Canonical Ltd
#
# License granted by Canonical Limited
#
# SPDX-License-Identifier: GPL-3.0-only
#
# This file is part of PackaStack. See LICENSE for details.

"""Tests for constants module."""

from packastack.constants import (
    DEFAULT_REMOTE,
    ERROR_LOG_FILE,
    LAUNCHPAD_TEAM,
    LOGS_DIR,
    MAX_RETRY_ATTEMPTS,
    PACKAGING_DIR,
    PRISTINE_TAR_BRANCH,
    RELEASES_DIR,
    RELEASES_REPO_URL,
    SERIES_STATUS_PATH,
    SIGNING_KEY_INDEX_PATH,
    SIGNING_KEY_PATTERN,
    SIGNING_KEY_STATIC_DIR,
    TARBALLS_BASE_URL,
    TARBALLS_DIR,
    UPSTREAM_BRANCH_PREFIX,
    UPSTREAM_DIR,
)


def test_url_constants():
    """Test URL constants are properly defined."""
    assert TARBALLS_BASE_URL == "https://tarballs.opendev.org"
    assert RELEASES_REPO_URL == "https://opendev.org/openstack/releases"


def test_launchpad_constants():
    """Test Launchpad constants."""
    assert LAUNCHPAD_TEAM == "~ubuntu-openstack-dev"


def test_directory_constants():
    """Test directory name constants."""
    assert PACKAGING_DIR == "packaging"
    assert UPSTREAM_DIR == "upstream"
    assert TARBALLS_DIR == "tarballs"
    assert RELEASES_DIR == "releases"
    assert LOGS_DIR == "logs"


def test_path_constants():
    """Test path constants."""
    assert SERIES_STATUS_PATH == "data/series_status.yaml"
    assert SIGNING_KEY_INDEX_PATH == "doc/source/index.rst"
    assert SIGNING_KEY_STATIC_DIR == "doc/source/static"


def test_branch_constants():
    """Test branch name constants."""
    assert PRISTINE_TAR_BRANCH == "pristine-tar"
    assert UPSTREAM_BRANCH_PREFIX == "upstream"


def test_git_constants():
    """Test git constants."""
    assert DEFAULT_REMOTE == "origin"


def test_retry_constants():
    """Test retry configuration constants."""
    assert MAX_RETRY_ATTEMPTS == 3
    assert isinstance(MAX_RETRY_ATTEMPTS, int)


def test_logging_constants():
    """Test logging constants."""
    assert ERROR_LOG_FILE == "import-errors.log"


def test_signing_key_pattern():
    """Test signing key regex pattern."""
    # Test with sample text
    sample = """
Some text here
present and Cycle key information
on the next line the key 0xb8e9315f48553ec5aff9ffe5e69d97da9efb5aff`_
more text
"""
    match = SIGNING_KEY_PATTERN.search(sample)
    assert match is not None
    assert match.group("key") == "0xb8e9315f48553ec5aff9ffe5e69d97da9efb5aff"
