import click
from rich.console import Console
from gh_stats.github_client import get_user, get_repos, get_events
from gh_stats.display import show_user, show_repos, show_activity, show_compare

console = Console()


@click.group()
@click.version_option(package_name="gh-stats")
def cli():
    """GitHub profile stats in your terminal."""
    pass


@cli.command()
@click.argument("username")
def user(username):
    """Show a user's GitHub profile summary."""
    try:
        with console.status(f"Fetching {username}..."):
            user_data = get_user(username)
            repos = get_repos(username)
        show_user(user_data, repos)
    except RuntimeError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise SystemExit(1)


@cli.command()
@click.argument("username")
def repos(username):
    """List a user's repositories sorted by stars."""
    try:
        with console.status(f"Fetching repos for {username}..."):
            repo_list = get_repos(username)
        show_repos(repo_list)
    except RuntimeError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise SystemExit(1)


@cli.command()
@click.argument("username")
def activity(username):
    """Show a user's recent public activity."""
    try:
        with console.status(f"Fetching activity for {username}..."):
            events = get_events(username)
        show_activity(events, username)
    except RuntimeError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise SystemExit(1)


@cli.command()
@click.argument("user1")
@click.argument("user2")
def compare(user1, user2):
    """Compare two GitHub profiles side by side."""
    try:
        with console.status(f"Fetching {user1} and {user2}..."):
            u1 = get_user(user1)
            r1 = get_repos(user1)
            u2 = get_user(user2)
            r2 = get_repos(user2)
        show_compare(u1, r1, u2, r2)
    except RuntimeError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise SystemExit(1)
