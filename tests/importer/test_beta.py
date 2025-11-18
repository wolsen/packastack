# Copyright (C) 2025 Canonical Ltd
#
# License granted by Canonical Limited
#
# SPDX-License-Identifier: GPL-3.0-only
#
# This file is part of PackaStack. See LICENSE for details.

"""Tests for beta importer."""

import pytest

from packastack.importer.beta import BetaImporter


@pytest.fixture
def importer_setup(tmp_path):
    """Set up paths for beta importer."""
    packaging = tmp_path / "packaging"
    upstream = tmp_path / "upstream" / "nova"
    tarballs = tmp_path / "tarballs"
    releases = tmp_path / "releases"

    packaging.mkdir()
    upstream.mkdir(parents=True)
    tarballs.mkdir()
    releases.mkdir()

    return packaging, upstream, tarballs, releases


def test_convert_version_beta(importer_setup):
    """Test version conversion for betas."""
    packaging, upstream, tarballs, releases = importer_setup

    importer = BetaImporter(
        str(packaging), str(upstream), str(tarballs), "dalmatian", str(releases)
    )

    assert importer.convert_version("27.1.0.0b0") == "27.1.0~b0"
    assert importer.convert_version("27.1.0b1") == "27.1.0~b1"
