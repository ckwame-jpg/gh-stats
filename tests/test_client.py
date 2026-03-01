from unittest.mock import patch, MagicMock
from gh_stats.github_client import get_user, get_repos, get_events


def _mock_response(data, status=200):
    resp = MagicMock()
    resp.status_code = status
    resp.json.return_value = data
    resp.raise_for_status.return_value = None
    resp.headers = {}
    return resp


@patch("gh_stats.github_client._get_cached", return_value=None)
@patch("gh_stats.github_client._set_cached")
@patch("httpx.get")
def test_get_user(mock_get, mock_set, mock_cache):
    mock_get.return_value = _mock_response({
        "login": "testuser",
        "public_repos": 10,
        "followers": 5,
        "following": 3,
    })
    user = get_user("testuser")
    assert user["login"] == "testuser"
    assert user["public_repos"] == 10


@patch("gh_stats.github_client._get_cached", return_value=None)
@patch("gh_stats.github_client._set_cached")
@patch("httpx.get")
def test_get_repos(mock_get, mock_set, mock_cache):
    mock_get.return_value = _mock_response([
        {"name": "repo1", "stargazers_count": 5, "language": "Python"},
        {"name": "repo2", "stargazers_count": 3, "language": "JavaScript"},
    ])
    repos = get_repos("testuser")
    assert len(repos) == 2
    assert repos[0]["name"] == "repo1"


@patch("gh_stats.github_client._get_cached", return_value=None)
@patch("gh_stats.github_client._set_cached")
@patch("httpx.get")
def test_get_events(mock_get, mock_set, mock_cache):
    mock_get.return_value = _mock_response([
        {"type": "PushEvent", "repo": {"name": "user/repo"}, "created_at": "2025-01-01", "payload": {}},
    ])
    events = get_events("testuser")
    assert len(events) == 1
    assert events[0]["type"] == "PushEvent"


@patch("gh_stats.github_client._get_cached", return_value=None)
@patch("httpx.get")
def test_rate_limit(mock_get, mock_cache):
    resp = MagicMock()
    resp.status_code = 403
    resp.headers = {"x-ratelimit-reset": "9999999999"}
    mock_get.return_value = resp

    try:
        get_user("testuser")
        assert False, "Should have raised"
    except RuntimeError as e:
        assert "rate limit" in str(e).lower()


@patch("gh_stats.github_client._get_cached", return_value=None)
@patch("httpx.get")
def test_user_not_found(mock_get, mock_cache):
    resp = MagicMock()
    resp.status_code = 404
    resp.headers = {}
    mock_get.return_value = resp

    try:
        get_user("nonexistent_user_xyz")
        assert False, "Should have raised"
    except RuntimeError as e:
        assert "not found" in str(e).lower()
