# Copyright (C) 2025 Canonical Ltd
#
# License granted by Canonical Limited
#
# SPDX-License-Identifier: GPL-3.0-only
#
# This file is part of PackaStack. See LICENSE for details.

"""Launchpad API client with retry logic."""

from launchpadlib.launchpad import Launchpad
from tenacity import retry, stop_after_attempt, wait_exponential

from packastack.constants import (
    MAX_RETRY_ATTEMPTS,
    RETRY_MAX_WAIT_SECONDS,
    RETRY_MIN_WAIT_SECONDS,
    RETRY_MULTIPLIER,
)
from packastack.exceptions import LaunchpadError


class LaunchpadClient:
    """Client for interacting with Launchpad API anonymously."""

    def __init__(self):
        """Initialize Launchpad client."""
        self._lp: Launchpad | None = None

    @retry(
        stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
        wait=wait_exponential(
            multiplier=RETRY_MULTIPLIER,
            min=RETRY_MIN_WAIT_SECONDS,
            max=RETRY_MAX_WAIT_SECONDS,
        ),
        reraise=True,
    )
    def connect(self) -> None:
        """
        Connect to Launchpad anonymously.

        Raises:
            LaunchpadError: If connection fails
        """
        try:
            self._lp = Launchpad.login_anonymously(
                "packastack", "production", version="devel"
            )
        except Exception as e:
            raise LaunchpadError(f"Failed to connect to Launchpad: {e}")

    @property
    def lp(self) -> Launchpad:
        """
        Get Launchpad instance, connecting if necessary.

        Returns:
            Launchpad instance

        Raises:
            LaunchpadError: If not connected
        """
        if not self._lp:
            self.connect()
        if not self._lp:
            raise LaunchpadError("Not connected to Launchpad")
        return self._lp
