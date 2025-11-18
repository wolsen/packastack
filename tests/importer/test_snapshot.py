# Copyright (C) 2025 Canonical Ltd
#
# License granted by Canonical Limited
#
# SPDX-License-Identifier: GPL-3.0-only
#
# This file is part of PackaStack. See LICENSE for details.

"""Tests for snapshot importer."""

from unittest.mock import MagicMock, Mock, patch

import pytest

from packastack.exceptions import ImporterError
from packastack.importer.snapshot import SnapshotImporter


@pytest.fixture
def importer_setup(tmp_path):
    """Set up paths for snapshot importer."""
    packaging = tmp_path / "packaging"
    upstream = tmp_path / "upstream" / "nova"
    tarballs = tmp_path / "tarballs"
    releases = tmp_path / "releases"

    packaging.mkdir()
    upstream.mkdir(parents=True)
    tarballs.mkdir()
    releases.mkdir()

    return packaging, upstream, tarballs, releases


@patch("packastack.importer.snapshot.RepoManager")
def test_get_version_no_tags(mock_repo_mgr, importer_setup):
    """Test getting version when HEAD has no tags."""
    packaging, upstream, tarballs, releases = importer_setup

    mock_mgr = MagicMock()
    mock_mgr.get_head_tags.return_value = []
    mock_mgr.git_describe.return_value = "1.0.0-5-gabcdef"
    mock_repo_mgr.return_value = mock_mgr

    importer = SnapshotImporter(
        str(packaging), str(upstream), str(tarballs), "dalmatian", str(releases)
    )

    version = importer.get_version()
    assert version == "1.0.0-5-gabcdef"


@patch("packastack.importer.snapshot.RepoManager")
def test_get_version_with_tag_non_explicit(mock_repo_mgr, importer_setup):
    """Test getting version when HEAD has tag (auto mode)."""
    packaging, upstream, tarballs, releases = importer_setup

    mock_mgr = MagicMock()
    mock_mgr.get_head_tags.return_value = ["27.1.0"]
    mock_repo_mgr.return_value = mock_mgr

    importer = SnapshotImporter(
        str(packaging),
        str(upstream),
        str(tarballs),
        "dalmatian",
        str(releases),
        explicit_snapshot=False,
    )

    with pytest.raises(ImporterError, match="HEAD is tagged"):
        importer.get_version()


@patch("packastack.importer.snapshot.RepoManager")
def test_get_version_with_tag_explicit(mock_repo_mgr, importer_setup):
    """Test getting version when HEAD has tag (explicit snapshot)."""
    packaging, upstream, tarballs, releases = importer_setup

    mock_mgr = MagicMock()
    mock_mgr.get_head_tags.return_value = ["27.1.0"]
    mock_repo_mgr.return_value = mock_mgr

    importer = SnapshotImporter(
        str(packaging),
        str(upstream),
        str(tarballs),
        "dalmatian",
        str(releases),
        explicit_snapshot=True,
    )

    with pytest.raises(SystemExit) as exc_info:
        importer.get_version()

    assert exc_info.value.code == 74  # EBADMSG


@patch("subprocess.run")
def test_get_tarball_with_uv(mock_run, importer_setup):
    """Test tarball generation with uv."""
    packaging, upstream, tarballs, releases = importer_setup

    # Create fake dist directory with tarball
    dist_dir = upstream / "dist"
    dist_dir.mkdir()
    tarball = dist_dir / "nova-1.0.0.tar.gz"
    tarball.write_text("fake tarball")

    mock_run.return_value = Mock(returncode=0)

    importer = SnapshotImporter(
        str(packaging), str(upstream), str(tarballs), "dalmatian", str(releases)
    )

    result = importer.get_tarball("1.0.0-5-gabcdef")

    assert result.name == "nova-1.0.0.tar.gz"
    assert result.parent == tarballs


@patch("subprocess.run")
def test_get_tarball_fallback_to_setuppy(mock_run, importer_setup):
    """Test tarball generation fallback to setup.py."""
    packaging, upstream, tarballs, releases = importer_setup

    # First call (uv) fails, second call (setup.py) succeeds
    def run_side_effect(cmd, *args, **kwargs):
        if "uv" in cmd:
            return Mock(returncode=1)
        else:
            # Create tarball for setup.py call
            dist_dir = upstream / "dist"
            dist_dir.mkdir(exist_ok=True)
            tarball = dist_dir / "nova-1.0.0.tar.gz"
            tarball.write_text("fake tarball")
            return Mock(returncode=0)

    mock_run.side_effect = run_side_effect

    importer = SnapshotImporter(
        str(packaging), str(upstream), str(tarballs), "dalmatian", str(releases)
    )

    result = importer.get_tarball("1.0.0-5-gabcdef")

    assert result.exists()


@patch("subprocess.run")
def test_get_tarball_no_dist_dir(mock_run, importer_setup):
    """Test tarball generation when dist dir doesn't exist."""
    packaging, upstream, tarballs, releases = importer_setup

    mock_run.return_value = Mock(returncode=0)

    importer = SnapshotImporter(
        str(packaging), str(upstream), str(tarballs), "dalmatian", str(releases)
    )

    with pytest.raises(ImporterError, match="No tarball generated"):
        importer.get_tarball("1.0.0-5-gabcdef")


@patch("subprocess.run")
def test_get_tarball_no_tarballs(mock_run, importer_setup):
    """Test tarball generation when dist dir has no tarballs."""
    packaging, upstream, tarballs, releases = importer_setup

    # Create empty dist directory
    dist_dir = upstream / "dist"
    dist_dir.mkdir()

    mock_run.return_value = Mock(returncode=0)

    importer = SnapshotImporter(
        str(packaging), str(upstream), str(tarballs), "dalmatian", str(releases)
    )

    with pytest.raises(ImporterError, match="No tarball generated"):
        importer.get_tarball("1.0.0-5-gabcdef")


def test_convert_version_snapshot(importer_setup):
    """Test snapshot version conversion."""
    packaging, upstream, tarballs, releases = importer_setup

    importer = SnapshotImporter(
        str(packaging), str(upstream), str(tarballs), "dalmatian", str(releases)
    )

    version = importer.convert_version("1.0.0-5-gabcdef")
    assert version == "1.0.0+5-gabcdef.1-1ubuntu0"


def test_convert_version_snapshot_no_existing(importer_setup):
    """Test snapshot version conversion with no existing versions."""
    packaging, upstream, tarballs, releases = importer_setup

    # Empty tarballs directory - no existing files
    importer = SnapshotImporter(
        str(packaging), str(upstream), str(tarballs), "dalmatian", str(releases)
    )

    version = importer.convert_version("1.0.0-5-gabcdef")
    # Should find no existing tarballs, return base version with counter 1
    assert version == "1.0.0+5-gabcdef.1-1ubuntu0"


def test_convert_version_snapshot_no_match(importer_setup):
    """Test snapshot version conversion with non-matching tarball."""
    packaging, upstream, tarballs, releases = importer_setup

    # Create tarball that doesn't match the pattern
    bad_tarball = tarballs / "invalid-name.orig.tar.gz"
    bad_tarball.write_text("bad")

    importer = SnapshotImporter(
        str(packaging), str(upstream), str(tarballs), "dalmatian", str(releases)
    )

    version = importer.convert_version("1.0.0-5-gabcdef")
    # Should not find matching version, return base version with counter 1
    assert version == "1.0.0+5-gabcdef.1-1ubuntu0"


def test_convert_version_snapshot_with_existing(importer_setup):
    """Test snapshot version conversion with existing version."""
    packaging, upstream, tarballs, releases = importer_setup

    # Create existing tarball
    existing = tarballs / "nova_1.0.0+5-gabcdef.1-1ubuntu0.orig.tar.gz"
    existing.write_text("existing")

    importer = SnapshotImporter(
        str(packaging), str(upstream), str(tarballs), "dalmatian", str(releases)
    )

    version = importer.convert_version("1.0.0-5-gabcdef")
    # Existing tarball has .1, resulting version should increment to .2
    assert version == "1.0.0+5-gabcdef.2-1ubuntu0"


@patch("packastack.importer.snapshot.RepoManager")
def test_get_version_git_describe_error(mock_repo_mgr, importer_setup):
    """Test error when git describe fails."""
    packaging, upstream, tarballs, releases = importer_setup

    mock_mgr = MagicMock()
    mock_mgr.get_head_tags.return_value = []
    mock_mgr.git_describe.side_effect = Exception("Git error")
    mock_repo_mgr.return_value = mock_mgr

    importer = SnapshotImporter(
        str(packaging), str(upstream), str(tarballs), "dalmatian", str(releases)
    )

    with pytest.raises(ImporterError, match="Failed to get git describe"):
        importer.get_version()


@patch("subprocess.run")
def test_get_tarball_uv_not_found(mock_run, importer_setup):
    """Test tarball generation when uv is not installed."""
    packaging, upstream, tarballs, releases = importer_setup

    # First call (uv) raises FileNotFoundError, second call (setup.py) succeeds
    def run_side_effect(cmd, *args, **kwargs):
        if "uv" in cmd:
            raise FileNotFoundError("uv not found")
        else:
            # Create tarball for setup.py call
            dist_dir = upstream / "dist"
            dist_dir.mkdir(exist_ok=True)
            tarball = dist_dir / "nova-1.0.0.tar.gz"
            tarball.write_text("fake tarball")
            return Mock(returncode=0)

    mock_run.side_effect = run_side_effect

    importer = SnapshotImporter(
        str(packaging), str(upstream), str(tarballs), "dalmatian", str(releases)
    )

    result = importer.get_tarball("1.0.0-5-gabcdef")
    assert result.exists()


@patch("subprocess.run")
def test_get_tarball_setuppy_error(mock_run, importer_setup):
    """Test tarball generation error with setup.py."""
    packaging, upstream, tarballs, releases = importer_setup

    mock_run.side_effect = [
        Mock(returncode=1),  # uv fails
        Mock(returncode=1, stderr="Setup error"),  # setup.py fails
    ]

    importer = SnapshotImporter(
        str(packaging), str(upstream), str(tarballs), "dalmatian", str(releases)
    )

    # Need to import subprocess to use CalledProcessError
    import subprocess

    # Mock run to raise CalledProcessError
    def run_side_effect(cmd, *args, **kwargs):
        if "uv" in cmd:
            return Mock(returncode=1)
        else:
            raise subprocess.CalledProcessError(1, cmd, stderr="Setup error")

    mock_run.side_effect = run_side_effect

    with pytest.raises(ImporterError, match="Failed to generate tarball"):
        importer.get_tarball("1.0.0-5-gabcdef")


@patch("subprocess.run")
def test_get_tarball_python_not_found(mock_run, importer_setup):
    """Test tarball generation when python3 is not found."""
    packaging, upstream, tarballs, releases = importer_setup

    def run_side_effect(cmd, *args, **kwargs):
        if "uv" in cmd:
            return Mock(returncode=1)
        else:
            raise FileNotFoundError("python3 not found")

    mock_run.side_effect = run_side_effect

    importer = SnapshotImporter(
        str(packaging), str(upstream), str(tarballs), "dalmatian", str(releases)
    )

    with pytest.raises(ImporterError, match="Neither uv nor python3 found"):
        importer.get_tarball("1.0.0-5-gabcdef")


@patch("subprocess.run")
def test_get_tarball_no_dist_created(mock_run, importer_setup):
    """Test error when no tarball is generated."""
    packaging, upstream, tarballs, releases = importer_setup

    mock_run.return_value = Mock(returncode=0)

    importer = SnapshotImporter(
        str(packaging), str(upstream), str(tarballs), "dalmatian", str(releases)
    )

    with pytest.raises(ImporterError, match="No tarball generated"):
        importer.get_tarball("1.0.0-5-gabcdef")
