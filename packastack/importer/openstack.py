# Copyright (C) 2025 Canonical Ltd
#
# License granted by Canonical Limited
#
# SPDX-License-Identifier: GPL-3.0-only
#
# This file is part of PackaStack. See LICENSE for details.

"""OpenStack releases repository utilities."""

from pathlib import Path

import yaml

from packastack.constants import (
    SERIES_STATUS_PATH,
    SIGNING_KEY_INDEX_PATH,
    SIGNING_KEY_PATTERN,
    SIGNING_KEY_STATIC_DIR,
)
from packastack.exceptions import ImporterError


def get_current_cycle(releases_repo_path: str | Path) -> str:
    """
    Get current development cycle from series_status.yaml.

    Args:
        releases_repo_path: Path to releases repository (str or Path)

    Returns:
        Current cycle name (e.g., 'caracal', 'dalmatian')

    Raises:
        ImporterError: If file not found or no development cycle found
    """
    series_status_file = Path(releases_repo_path) / SERIES_STATUS_PATH

    if not series_status_file.exists():
        raise ImporterError(f"Series status file not found: {series_status_file}")

    try:
        with open(series_status_file) as f:
            series_data = yaml.safe_load(f)
    except Exception as e:
        raise ImporterError(f"Failed to parse series_status.yaml: {e}")

    # Handle list format of series_status.yaml
    # series_status.yaml is a list of series with 'name' and 'status' keys
    if isinstance(series_data, list):
        for series_info in series_data:
            is_dict = isinstance(series_info, dict)
            if not is_dict:
                continue
            status = series_info.get("status")
            if status != "development":
                continue
            name = series_info.get("name")
            if name:
                return name

    raise ImporterError("No development cycle found in series_status.yaml")


def get_previous_cycle(releases_repo_path: str | Path) -> str | None:
    """
    Get previous released cycle from series_status.yaml.

    Args:
        releases_repo_path: Path to releases repository (str or Path)

    Returns:
        Previous cycle name or None if not found

    Raises:
        ImporterError: If file not found or parsing fails
    """
    series_status_file = Path(releases_repo_path) / SERIES_STATUS_PATH

    if not series_status_file.exists():
        raise ImporterError(f"Series status file not found: {series_status_file}")

    try:
        with open(series_status_file) as f:
            series_data = yaml.safe_load(f)
    except Exception as e:
        raise ImporterError(f"Failed to parse series_status.yaml: {e}")

    # Expected ordering is reverse-chronological: first entry is development
    # and the second entry is the previous release. Fail fast if structure
    # is not the expected list format.
    assert isinstance(series_data, list), "expected series_status.yaml to be a list"

    # If there are fewer than two entries, there's no previous release
    # to return.
    if len(series_data) < 2:
        return None

    second_entry = series_data[1]
    assert isinstance(second_entry, dict)

    name = second_entry.get("name")
    if name:
        return name

    return None


def get_signing_key(releases_repo_path: str | Path) -> tuple[str, str]:
    """
    Get current cycle signing key ID and content.

    Parses doc/source/index.rst to find the signing key ID for the current
    development cycle, then reads the key content from doc/source/static/.

    Args:
        releases_repo_path: Path to releases repository (str or Path)

    Returns:
        Tuple of (key_id, key_content)

    Raises:
        ImporterError: If key not found or files can't be read
    """
    index_file = Path(releases_repo_path) / SIGNING_KEY_INDEX_PATH

    if not index_file.exists():
        raise ImporterError(f"Index file not found: {index_file}")

    try:
        content = index_file.read_text()
    except Exception as e:
        raise ImporterError(f"Failed to read index.rst: {e}")

    # Find signing key ID using regex
    match = SIGNING_KEY_PATTERN.search(content)
    if not match:
        raise ImporterError("Could not find signing key in index.rst")

    key_id = match.group("key").strip()

    # Read key content from static directory
    key_file = Path(releases_repo_path) / SIGNING_KEY_STATIC_DIR / f"{key_id}.txt"

    if not key_file.exists():
        raise ImporterError(f"Signing key file not found: {key_file}")

    try:
        key_content = key_file.read_text()
    except Exception as e:
        raise ImporterError(f"Failed to read signing key file: {e}")

    return key_id, key_content


def get_deliverable_info(
    releases_repo_path: str | Path, cycle: str, project: str
) -> dict | None:
    """
    Get deliverable information for a project.

    Reads deliverables/<cycle>/<project>.yaml to extract repository settings
    and version information.

    Args:
        releases_repo_path: Path to releases repository (str or Path)
        cycle: OpenStack cycle name
        project: Project name

    Returns:
        Dictionary with deliverable info or None if not found
        Keys: namespace, project_name, tarball_base, latest_version

    Raises:
        ImporterError: If file exists but can't be parsed
    """
    deliverable_file = (
        Path(releases_repo_path) / "deliverables" / cycle / f"{project}.yaml"
    )

    if not deliverable_file.exists():
        # Not all projects have deliverable files
        return None

    try:
        with open(deliverable_file) as f:
            data = yaml.safe_load(f)
    except Exception as e:
        raise ImporterError(f"Failed to parse deliverable file {deliverable_file}: {e}")

    # Extract repository settings
    repo_settings = data.get("repository-settings", {})

    # Get the first repository (most projects have only one)
    repos = list(repo_settings.keys())
    if not repos:
        return None

    first_repo = repos[0]
    settings = repo_settings[first_repo]

    # Parse namespace and project name from repo path
    # Format: openstack/project-name
    repo_parts = first_repo.split("/")
    if len(repo_parts) >= 2:
        namespace = repo_parts[0]
        project_name = repo_parts[1]
    else:
        namespace = "openstack"
        project_name = first_repo

    # Get tarball base (if different from project name)
    tarball_base = settings.get("tarball-base", project_name)

    # Get latest version from releases
    latest_version = None
    releases = data.get("releases", [])
    if releases:
        # Releases are typically in chronological order
        latest_version = releases[-1].get("version")

    return {
        "namespace": namespace,
        "project_name": project_name,
        "tarball_base": tarball_base,
        "latest_version": latest_version,
        "repo_path": first_repo,
    }
