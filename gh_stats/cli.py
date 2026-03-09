import click
from rich.console import Console

from gh_stats.display import show_activity, show_compare, show_repos, show_user
from gh_stats.github_client import get_events, get_repos, get_user

console = Console()


def run_with_error_boundary(action):
    try:
        action()
    except RuntimeError as exc:
        console.print(f"[red]Error:[/red] {exc}")
        raise SystemExit(1) from exc


@click.group()
@click.version_option(package_name="gh-stats")
def cli():
    """GitHub profile stats in your terminal."""


@cli.command()
@click.argument("username")
def user(username):
    """Show a user's GitHub profile summary."""

    def action():
        with console.status(f"Fetching {username}..."):
            user_data = get_user(username)
            repos = get_repos(username)
        show_user(user_data, repos)

    run_with_error_boundary(action)


@cli.command()
@click.argument("username")
def repos(username):
    """List a user's repositories sorted by stars."""

    def action():
        with console.status(f"Fetching repos for {username}..."):
            repo_list = get_repos(username)
        show_repos(repo_list)

    run_with_error_boundary(action)


@cli.command()
@click.argument("username")
def activity(username):
    """Show a user's recent public activity."""

    def action():
        with console.status(f"Fetching activity for {username}..."):
            events = get_events(username)
        show_activity(events, username)

    run_with_error_boundary(action)


@cli.command()
@click.argument("user1")
@click.argument("user2")
def compare(user1, user2):
    """Compare two GitHub profiles side by side."""

    def action():
        with console.status(f"Fetching {user1} and {user2}..."):
            first_user = get_user(user1)
            first_repos = get_repos(user1)
            second_user = get_user(user2)
            second_repos = get_repos(user2)
        show_compare(first_user, first_repos, second_user, second_repos)

    run_with_error_boundary(action)
