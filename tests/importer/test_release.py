# Copyright (C) 2025 Canonical Ltd
#
# License granted by Canonical Limited
#
# SPDX-License-Identifier: GPL-3.0-only
#
# This file is part of PackaStack. See LICENSE for details.

"""Tests for release importer."""

from unittest.mock import Mock, patch

import pytest
import requests

from packastack.exceptions import ImporterError, NetworkError
from packastack.importer.release import ReleaseImporter


@pytest.fixture
def importer_setup(tmp_path):
    """Set up paths for release importer."""
    packaging = tmp_path / "packaging"
    upstream = tmp_path / "upstream" / "nova"
    tarballs = tmp_path / "tarballs"
    releases = tmp_path / "releases"

    packaging.mkdir()
    upstream.mkdir(parents=True)
    tarballs.mkdir()
    releases.mkdir()

    return packaging, upstream, tarballs, releases


@patch("packastack.importer.release.get_deliverable_info")
def test_get_version_success(mock_deliverable, importer_setup):
    """Test getting version from deliverable."""
    packaging, upstream, tarballs, releases = importer_setup

    mock_deliverable.return_value = {"latest_version": "27.1.0"}

    importer = ReleaseImporter(
        str(packaging), str(upstream), str(tarballs), "dalmatian", str(releases)
    )

    version = importer.get_version()
    assert version == "27.1.0"


@patch("packastack.importer.release.get_deliverable_info")
def test_get_version_no_deliverable(mock_deliverable, importer_setup):
    """Test error when no deliverable found."""
    packaging, upstream, tarballs, releases = importer_setup
    mock_deliverable.return_value = None

    importer = ReleaseImporter(
        str(packaging), str(upstream), str(tarballs), "dalmatian", str(releases)
    )

    with pytest.raises(ImporterError, match="No deliverable found"):
        importer.get_version()


@patch("packastack.importer.release.get_deliverable_info")
def test_get_version_no_version(mock_deliverable, importer_setup):
    """Test error when deliverable has no version."""
    packaging, upstream, tarballs, releases = importer_setup
    mock_deliverable.return_value = {"latest_version": None}

    importer = ReleaseImporter(
        str(packaging), str(upstream), str(tarballs), "dalmatian", str(releases)
    )

    with pytest.raises(ImporterError, match="No release version found"):
        importer.get_version()


@patch("packastack.importer.release.requests.get")
def test_download_file_success(mock_get, importer_setup, tmp_path):
    """Test successful file download."""
    packaging, upstream, tarballs, releases = importer_setup

    mock_response = Mock()
    mock_response.iter_content.return_value = [b"data"]
    mock_get.return_value = mock_response

    importer = ReleaseImporter(
        str(packaging), str(upstream), str(tarballs), "dalmatian", str(releases)
    )

    dest = tmp_path / "test.tar.gz"
    importer.download_file("https://example.com/test.tar.gz", dest)

    assert dest.exists()
    assert dest.read_bytes() == b"data"


@patch("packastack.importer.release.requests.get")
def test_download_file_error(mock_get, importer_setup, tmp_path):
    """Test download error."""
    packaging, upstream, tarballs, releases = importer_setup
    mock_get.side_effect = requests.RequestException("Network error")

    importer = ReleaseImporter(
        str(packaging), str(upstream), str(tarballs), "dalmatian", str(releases)
    )

    dest = tmp_path / "test.tar.gz"

    with pytest.raises(NetworkError, match="Failed to download"):
        importer.download_file("https://example.com/test.tar.gz", dest)


@patch("packastack.importer.release.get_signing_key")
@patch("packastack.importer.release.get_deliverable_info")
@patch("packastack.importer.release.requests.get")
def test_get_tarball_success(mock_get, mock_deliverable, mock_key, importer_setup):
    """Test successful tarball download."""
    packaging, upstream, tarballs, releases = importer_setup

    mock_deliverable.return_value = {
        "namespace": "openstack",
        "tarball_base": "nova",
    }

    mock_key.return_value = ("0xABC123", "key content")

    mock_response = Mock()
    mock_response.iter_content.return_value = [b"tarball data"]
    mock_get.return_value = mock_response

    importer = ReleaseImporter(
        str(packaging), str(upstream), str(tarballs), "dalmatian", str(releases)
    )

    tarball = importer.get_tarball("27.1.0")

    assert tarball.name == "nova-27.1.0.tar.gz"
    assert tarball.exists()


@patch("packastack.importer.release.get_signing_key")
@patch("packastack.importer.release.get_deliverable_info")
def test_get_tarball_existing_files(mock_deliverable, mock_key, importer_setup):
    """Test get_tarball with existing tarball and signature."""
    packaging, upstream, tarballs, releases = importer_setup

    mock_deliverable.return_value = {
        "namespace": "openstack",
        "tarball_base": "nova",
    }

    mock_key.return_value = ("0xABC123", "key content")

    importer = ReleaseImporter(
        str(packaging), str(upstream), str(tarballs), "dalmatian", str(releases)
    )

    # Pre-create tarball and signature
    tarball_path = tarballs / "nova-27.1.0.tar.gz"
    signature_path = tarballs / "nova-27.1.0.tar.gz.asc"
    tarball_path.write_text("existing tarball")
    signature_path.write_text("existing signature")

    tarball = importer.get_tarball("27.1.0")

    # Should return existing files without download
    assert tarball == tarball_path
    assert tarball.read_text() == "existing tarball"


def test_convert_version(importer_setup):
    """Test version conversion for release."""
    packaging, upstream, tarballs, releases = importer_setup

    importer = ReleaseImporter(
        str(packaging), str(upstream), str(tarballs), "dalmatian", str(releases)
    )

    assert importer.convert_version("27.1.0") == "27.1.0"
    assert importer.convert_version("27.1") == "27.1"


@patch("packastack.importer.release.get_deliverable_info")
def test_get_tarball_no_deliverable(mock_deliverable, importer_setup):
    """Test error when no deliverable found in get_tarball."""
    packaging, upstream, tarballs, releases = importer_setup
    mock_deliverable.return_value = None

    importer = ReleaseImporter(
        str(packaging), str(upstream), str(tarballs), "dalmatian", str(releases)
    )

    with pytest.raises(ImporterError, match="No deliverable found"):
        importer.get_tarball("27.1.0")
