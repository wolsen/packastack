# Copyright (C) 2025 Canonical Ltd
#
# License granted by Canonical Limited
#
# SPDX-License-Identifier: GPL-3.0-only
#
# This file is part of PackaStack. See LICENSE for details.

"""Tests for candidate importer."""

import pytest

from packastack.importer.candidate import CandidateImporter


@pytest.fixture
def importer_setup(tmp_path):
    """Set up paths for candidate importer."""
    packaging = tmp_path / "packaging"
    upstream = tmp_path / "upstream" / "nova"
    tarballs = tmp_path / "tarballs"
    releases = tmp_path / "releases"

    packaging.mkdir()
    upstream.mkdir(parents=True)
    tarballs.mkdir()
    releases.mkdir()

    return packaging, upstream, tarballs, releases


def test_convert_version_rc(importer_setup):
    """Test version conversion for release candidates."""
    packaging, upstream, tarballs, releases = importer_setup

    importer = CandidateImporter(
        str(packaging), str(upstream), str(tarballs), "dalmatian", str(releases)
    )

    assert importer.convert_version("27.1.0.0rc0") == "27.1.0~rc0"
    assert importer.convert_version("27.1.0rc1") == "27.1.0~rc1"
