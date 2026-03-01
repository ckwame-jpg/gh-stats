from unittest.mock import patch
from click.testing import CliRunner
from gh_stats.cli import cli

runner = CliRunner()

MOCK_USER = {
    "login": "testuser",
    "name": "Test User",
    "bio": "A developer",
    "public_repos": 10,
    "followers": 5,
    "following": 3,
    "location": "NYC",
    "company": None,
}

MOCK_REPOS = [
    {"name": "repo1", "stargazers_count": 5, "language": "Python", "updated_at": "2025-01-01", "description": "A project"},
    {"name": "repo2", "stargazers_count": 3, "language": "JavaScript", "updated_at": "2025-01-02", "description": "Another"},
]

MOCK_EVENTS = [
    {"type": "PushEvent", "repo": {"name": "user/repo1"}, "created_at": "2025-01-15", "payload": {"commits": [{"message": "fix bug"}]}},
    {"type": "PullRequestEvent", "repo": {"name": "user/repo2"}, "created_at": "2025-01-14", "payload": {"action": "opened", "pull_request": {"title": "Add feature"}}},
]


@patch("gh_stats.cli.get_repos", return_value=MOCK_REPOS)
@patch("gh_stats.cli.get_user", return_value=MOCK_USER)
def test_user_command(mock_user, mock_repos):
    result = runner.invoke(cli, ["user", "testuser"])
    assert result.exit_code == 0
    assert "testuser" in result.output


@patch("gh_stats.cli.get_repos", return_value=MOCK_REPOS)
def test_repos_command(mock_repos):
    result = runner.invoke(cli, ["repos", "testuser"])
    assert result.exit_code == 0
    assert "repo1" in result.output


@patch("gh_stats.cli.get_events", return_value=MOCK_EVENTS)
def test_activity_command(mock_events):
    result = runner.invoke(cli, ["activity", "testuser"])
    assert result.exit_code == 0
    assert "Push" in result.output


@patch("gh_stats.cli.get_repos", return_value=MOCK_REPOS)
@patch("gh_stats.cli.get_user", return_value=MOCK_USER)
def test_compare_command(mock_user, mock_repos):
    result = runner.invoke(cli, ["compare", "user1", "user2"])
    assert result.exit_code == 0


@patch("gh_stats.cli.get_user", side_effect=RuntimeError("User not found."))
def test_user_not_found(mock_user):
    result = runner.invoke(cli, ["user", "nonexistent"])
    assert result.exit_code == 1
    assert "Error" in result.output
