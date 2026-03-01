# gh-stats

[![CI](https://github.com/ckwame-jpg/gh-stats/actions/workflows/ci.yml/badge.svg)](https://github.com/ckwame-jpg/gh-stats/actions/workflows/ci.yml)

A CLI tool that pulls GitHub profile data and displays it in your terminal. View user profiles, repo stats, recent activity, and compare two users side by side.

## Install

```bash
pip install -r requirements.txt
pip install -e .
```

## Usage

```bash
# Profile summary - repos, stars, top languages
gh-stats user ckwame-jpg

# List repos sorted by stars
gh-stats repos ckwame-jpg

# Recent public activity - pushes, PRs, issues
gh-stats activity ckwame-jpg

# Compare two profiles side by side
gh-stats compare ckwame-jpg torvalds
```

## Features

- Rich terminal output with tables, colors, and panels
- Caches API responses for 5 minutes to avoid rate limits
- Supports `GITHUB_TOKEN` env var for higher API limits
- Graceful error handling for rate limits and missing users
- Installable via pip with `gh-stats` entry point

## Tech Stack

- **Click** - CLI framework
- **Rich** - terminal formatting
- **httpx** - HTTP client
- **pytest** - test suite

## Running Tests

```bash
pytest -v
```

```text
tests/test_client.py::test_get_user           PASSED
tests/test_client.py::test_get_repos          PASSED
tests/test_client.py::test_get_events         PASSED
tests/test_client.py::test_rate_limit         PASSED
tests/test_client.py::test_user_not_found     PASSED
tests/test_cli.py::test_user_command          PASSED
tests/test_cli.py::test_repos_command         PASSED
tests/test_cli.py::test_activity_command      PASSED
tests/test_cli.py::test_compare_command       PASSED
tests/test_cli.py::test_user_not_found        PASSED
```

## Built By

Christopher Prempeh
