import os
import json
import time
import httpx
from pathlib import Path

CACHE_DIR = Path.home() / ".cache" / "gh-stats"
CACHE_TTL = 300  # 5 minutes


def _cache_path(key):
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    safe_key = key.replace("/", "_").replace("?", "_")
    return CACHE_DIR / f"{safe_key}.json"


def _get_cached(key):
    path = _cache_path(key)
    if path.exists():
        data = json.loads(path.read_text())
        if time.time() - data["ts"] < CACHE_TTL:
            return data["body"]
    return None


def _set_cached(key, body):
    path = _cache_path(key)
    path.write_text(json.dumps({"ts": time.time(), "body": body}))


def _get(url, params=None):
    cache_key = url + (str(params) if params else "")
    cached = _get_cached(cache_key)
    if cached is not None:
        return cached

    headers = {"Accept": "application/vnd.github+json"}
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    resp = httpx.get(url, headers=headers, params=params, timeout=15)

    if resp.status_code == 403:
        reset = resp.headers.get("x-ratelimit-reset")
        msg = "GitHub API rate limit hit."
        if reset:
            wait = int(reset) - int(time.time())
            msg += f" Resets in {max(wait, 0)}s."
        msg += " Set GITHUB_TOKEN env var for higher limits."
        raise RuntimeError(msg)

    if resp.status_code == 404:
        raise RuntimeError("User not found.")

    resp.raise_for_status()
    data = resp.json()
    _set_cached(cache_key, data)
    return data


def get_user(username):
    return _get(f"https://api.github.com/users/{username}")


def get_repos(username):
    repos = []
    page = 1
    while True:
        batch = _get(
            f"https://api.github.com/users/{username}/repos",
            params={"per_page": 100, "page": page, "sort": "updated"},
        )
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return repos


def get_events(username):
    return _get(
        f"https://api.github.com/users/{username}/events/public",
        params={"per_page": 30},
    )
