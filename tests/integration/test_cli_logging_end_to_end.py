# Integration test demonstrating a minimal CLI run without network calls
from pathlib import Path
from unittest.mock import patch
from click.testing import CliRunner

from packastack.cli import cli


@patch("packastack.cmds.import_tarballs.get_launchpad_repositories", return_value=[])
def test_cli_end_to_end(tmp_path, mock_get_repos):
    """Run CLI with a real releases repo and ensure logs are created.

    This test avoids network calls by ensuring the upstream/releases repo
    is a local git repository and patching get_launchpad_repositories.
    """
    # Create required directories under root
    root = tmp_path
    packaging = root / "packaging"
    upstream = root / "upstream"
    tarballs = root / "tarballs"
    logs = root / "logs"
    packaging.mkdir()
    upstream.mkdir()
    tarballs.mkdir()
    logs.mkdir()

    # Create a minimal releases repository with a data file so get_current_cycle
    # can read it without errors and create a git repo to satisfy RepoManager
    releases = upstream / "releases"
    releases.mkdir(parents=True)
    (releases / "data").mkdir()
    series = releases / "data" / "series_status.yaml"
    series.write_text("[{'name': 'gazpacho', 'status': 'development'}]")

    # Initialize a git repository for releases to avoid RepoManager clone
    import subprocess as _sub
    _sub.run(["git", "init"], cwd=str(releases), check=True)
    (releases / "README").write_text("initial")
    _sub.run(["git", "add", "README"], cwd=str(releases), check=True)
    _sub.run(["git", "-c", "commit.gpgsign=false", "-c", "user.name=Test User", "-c", "user.email=test@example.com", "commit", "-m", "init"], cwd=str(releases), check=True)

    runner = CliRunner()
    result = runner.invoke(cli, ["--root", str(root), "import"]) 
    assert result.exit_code == 0

    # Basic assertions that logs directory exists and CLI log file is present
    cli_files = list(logs.glob("packastack-*.log"))
    assert len(cli_files) >= 1
*** End Patch