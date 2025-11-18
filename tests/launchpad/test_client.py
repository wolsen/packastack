# Copyright (C) 2025 Canonical Ltd
#
# License granted by Canonical Limited
#
# SPDX-License-Identifier: GPL-3.0-only
#
# This file is part of PackaStack. See LICENSE for details.

"""Tests for Launchpad client."""

from unittest.mock import MagicMock, patch

import pytest

from packastack.exceptions import LaunchpadError
from packastack.launchpad.client import LaunchpadClient


@patch("packastack.launchpad.client.Launchpad.login_anonymously")
def test_client_connect_success(mock_login):
    """Test successful connection to Launchpad."""
    mock_lp = MagicMock()
    mock_login.return_value = mock_lp

    client = LaunchpadClient()
    client.connect()

    assert client._lp == mock_lp
    mock_login.assert_called_once_with("packastack", "production", version="devel")


@patch("packastack.launchpad.client.Launchpad.login_anonymously")
def test_client_connect_error(mock_login):
    """Test connection error."""
    mock_login.side_effect = Exception("Connection failed")

    client = LaunchpadClient()

    with pytest.raises(LaunchpadError, match="Failed to connect to Launchpad"):
        client.connect()


@patch("packastack.launchpad.client.Launchpad.login_anonymously")
def test_client_lp_property_connects(mock_login):
    """Test lp property connects if needed."""
    mock_lp = MagicMock()
    mock_login.return_value = mock_lp

    client = LaunchpadClient()
    result = client.lp

    assert result == mock_lp
    mock_login.assert_called_once()


def test_client_lp_property_already_connected():
    """Test lp property returns existing connection."""
    client = LaunchpadClient()
    mock_lp = MagicMock()
    client._lp = mock_lp

    result = client.lp

    assert result == mock_lp


@patch("packastack.launchpad.client.Launchpad.login_anonymously")
def test_client_lp_property_none_after_connect_fails(mock_login):
    """Test lp property raises error if connection is None."""
    mock_login.return_value = None

    client = LaunchpadClient()

    with pytest.raises(LaunchpadError, match="Not connected to Launchpad"):
        _ = client.lp
