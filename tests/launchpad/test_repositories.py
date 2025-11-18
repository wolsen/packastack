# Copyright (C) 2025 Canonical Ltd
#
# License granted by Canonical Limited
#
# SPDX-License-Identifier: GPL-3.0-only
#
# This file is part of PackaStack. See LICENSE for details.

"""Tests for Launchpad repository manager."""

from unittest.mock import MagicMock

import pytest

from packastack.exceptions import LaunchpadError
from packastack.launchpad.client import LaunchpadClient
from packastack.launchpad.repositories import Repository, RepositoryManager


def test_repository_dataclass():
    """Test Repository dataclass."""
    repo = Repository(
        name="nova",
        url="https://git.launchpad.net/~ubuntu-openstack-dev/+git/nova",
        display_name="Nova",
    )

    assert repo.name == "nova"
    assert repo.url == "https://git.launchpad.net/~ubuntu-openstack-dev/+git/nova"
    assert repo.display_name == "Nova"


def test_repository_manager_init():
    """Test RepositoryManager initialization."""
    client = LaunchpadClient()
    mgr = RepositoryManager(client)

    assert mgr.client == client


def test_list_team_repositories_success():
    """Test successful repository listing."""
    # Mock Launchpad client
    mock_lp = MagicMock()
    mock_team = MagicMock()

    # Mock git repositories
    mock_repo1 = MagicMock()
    mock_repo1.name = "nova"
    mock_repo1.git_https_url = (
        "https://git.launchpad.net/ubuntu-openstack-dev/+git/nova"
    )
    mock_repo1.display_name = "Nova"

    mock_repo2 = MagicMock()
    mock_repo2.name = "neutron"
    mock_repo2.git_https_url = (
        "https://git.launchpad.net/ubuntu-openstack-dev/+git/neutron"
    )
    mock_repo2.display_name = "Neutron"

    mock_lp.people = {"ubuntu-openstack-dev": mock_team}
    mock_lp.git_repositories = MagicMock()
    mock_lp.git_repositories.getRepositories.return_value = [mock_repo1, mock_repo2]

    client = LaunchpadClient()
    client._lp = mock_lp

    mgr = RepositoryManager(client)
    repos = mgr.list_team_repositories()

    assert len(repos) == 2
    assert repos[0].name == "nova"
    assert repos[1].name == "neutron"


def test_list_team_repositories_team_not_found():
    """Test repository listing with team not found."""
    mock_lp = MagicMock()
    mock_lp.people = {"ubuntu-openstack-dev": None}

    client = LaunchpadClient()
    client._lp = mock_lp

    mgr = RepositoryManager(client)

    with pytest.raises(LaunchpadError, match="Team .* not found"):
        mgr.list_team_repositories()


def test_list_team_repositories_custom_team():
    """Test repository listing with custom team name."""
    mock_lp = MagicMock()
    mock_team = MagicMock()
    mock_lp.people = {"other-team": mock_team}
    mock_lp.git_repositories = MagicMock()
    mock_lp.git_repositories.getRepositories.return_value = []

    client = LaunchpadClient()
    client._lp = mock_lp

    mgr = RepositoryManager(client)
    repos = mgr.list_team_repositories("~other-team")

    assert len(repos) == 0


def test_list_team_repositories_error():
    """Test repository listing with error."""
    mock_lp = MagicMock()
    mock_lp.people = {"ubuntu-openstack-dev": MagicMock()}
    mock_lp.git_repositories = MagicMock()
    mock_lp.git_repositories.getRepositories.side_effect = Exception("API error")

    client = LaunchpadClient()
    client._lp = mock_lp

    mgr = RepositoryManager(client)

    with pytest.raises(LaunchpadError, match="Failed to list repositories"):
        mgr.list_team_repositories()


def test_list_team_repositories_git_repositories_not_present():
    """When lp.git_repositories is missing or fails, raise."""
    mock_lp = MagicMock()
    mock_lp.people = {"ubuntu-openstack-dev": MagicMock()}

    # Simulate missing attribute by setting lp.git_repositories to None
    mock_lp.git_repositories = None
    client = LaunchpadClient()
    client._lp = mock_lp

    mgr = RepositoryManager(client)
    with pytest.raises(LaunchpadError, match="Failed to list repositories"):
        mgr.list_team_repositories()
