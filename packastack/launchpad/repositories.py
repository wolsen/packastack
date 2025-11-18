# Copyright (C) 2025 Canonical Ltd
#
# License granted by Canonical Limited
#
# SPDX-License-Identifier: GPL-3.0-only
#
# This file is part of PackaStack. See LICENSE for details.

"""Repository listing and management for Launchpad."""

from dataclasses import dataclass

from tenacity import retry, stop_after_attempt, wait_exponential

from packastack.constants import (
    LAUNCHPAD_TEAM,
    MAX_RETRY_ATTEMPTS,
    RETRY_MAX_WAIT_SECONDS,
    RETRY_MIN_WAIT_SECONDS,
    RETRY_MULTIPLIER,
)
from packastack.exceptions import LaunchpadError
from packastack.launchpad.client import LaunchpadClient


@dataclass
class Repository:
    """Represents a Git repository on Launchpad."""

    name: str
    url: str
    display_name: str


class RepositoryManager:
    """Manages listing and accessing repositories from Launchpad."""

    def __init__(self, client: LaunchpadClient):
        """
        Initialize repository manager.

        Args:
            client: Launchpad client instance
        """
        self.client = client

    @retry(
        stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
        wait=wait_exponential(
            multiplier=RETRY_MULTIPLIER,
            min=RETRY_MIN_WAIT_SECONDS,
            max=RETRY_MAX_WAIT_SECONDS,
        ),
        reraise=True,
    )
    def list_team_repositories(
        self, team_name: str = LAUNCHPAD_TEAM
    ) -> list[Repository]:
        """
        List all Git repositories for a team.

        Args:
            team_name: Launchpad team name (e.g., '~ubuntu-openstack-dev')

        Returns:
            List of Repository objects

        Raises:
            LaunchpadError: If team not found or listing fails
        """
        try:
            lp = self.client.lp
            team_key = team_name.lstrip("~")
            team = lp.people[team_key]

            if not team:
                raise LaunchpadError(f"Team {team_name} not found")

            repositories = []
            for git_repo in lp.git_repositories.getRepositories(target=team):
                repo = Repository(
                    name=git_repo.name,
                    url=git_repo.git_https_url,
                    display_name=git_repo.display_name,
                )
                repositories.append(repo)

            return repositories

        except Exception as e:
            raise LaunchpadError(f"Failed to list repositories for {team_name}: {e}")
