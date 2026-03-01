from collections import Counter
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text

console = Console()


def show_user(user, repos):
    total_stars = sum(r.get("stargazers_count", 0) for r in repos)
    languages = Counter(r["language"] for r in repos if r.get("language"))
    top_langs = [lang for lang, _ in languages.most_common(5)]

    lines = [
        f"[bold]{user['login']}[/bold]",
        f"{user.get('name') or ''}",
        "",
        f"[cyan]Public repos:[/cyan]  {user['public_repos']}",
        f"[cyan]Followers:[/cyan]     {user['followers']}",
        f"[cyan]Following:[/cyan]     {user['following']}",
        f"[cyan]Total stars:[/cyan]   {total_stars}",
        f"[cyan]Top languages:[/cyan] {', '.join(top_langs) if top_langs else 'N/A'}",
    ]

    if user.get("bio"):
        lines.insert(2, f"[dim]{user['bio']}[/dim]")

    if user.get("location"):
        lines.append(f"[cyan]Location:[/cyan]     {user['location']}")

    if user.get("company"):
        lines.append(f"[cyan]Company:[/cyan]      {user['company']}")

    console.print(Panel("\n".join(lines), title="GitHub Profile", border_style="blue"))


def show_repos(repos):
    table = Table(title="Repositories", show_lines=False)
    table.add_column("Name", style="bold cyan", max_width=30)
    table.add_column("Stars", justify="right")
    table.add_column("Language", style="yellow")
    table.add_column("Updated", style="dim")
    table.add_column("Description", max_width=40, style="dim")

    sorted_repos = sorted(repos, key=lambda r: r.get("stargazers_count", 0), reverse=True)

    for repo in sorted_repos[:20]:
        table.add_row(
            repo["name"],
            str(repo.get("stargazers_count", 0)),
            repo.get("language") or "-",
            (repo.get("updated_at") or "")[:10],
            (repo.get("description") or "-")[:40],
        )

    console.print(table)


def show_activity(events, username):
    table = Table(title=f"Recent Activity - {username}", show_lines=False)
    table.add_column("Type", style="bold")
    table.add_column("Repo", style="cyan")
    table.add_column("Date", style="dim")
    table.add_column("Detail", max_width=50)

    for event in events[:20]:
        event_type = event["type"].replace("Event", "")
        repo = event.get("repo", {}).get("name", "")
        date = (event.get("created_at") or "")[:10]

        detail = ""
        payload = event.get("payload", {})
        if event_type == "Push":
            commits = payload.get("commits", [])
            if commits:
                detail = commits[0].get("message", "")[:50]
        elif event_type == "PullRequest":
            pr = payload.get("pull_request", {})
            action = payload.get("action", "")
            detail = f"{action}: {pr.get('title', '')[:40]}"
        elif event_type == "Issues":
            issue = payload.get("issue", {})
            action = payload.get("action", "")
            detail = f"{action}: {issue.get('title', '')[:40]}"
        elif event_type == "Create":
            ref_type = payload.get("ref_type", "")
            ref = payload.get("ref") or ""
            detail = f"{ref_type} {ref}"

        table.add_row(event_type, repo, date, detail)

    console.print(table)


def show_compare(user1, repos1, user2, repos2):
    def make_panel(user, repos):
        total_stars = sum(r.get("stargazers_count", 0) for r in repos)
        languages = Counter(r["language"] for r in repos if r.get("language"))
        top_langs = [lang for lang, _ in languages.most_common(3)]

        lines = [
            f"[bold]{user['login']}[/bold]",
            "",
            f"Repos:     {user['public_repos']}",
            f"Followers: {user['followers']}",
            f"Stars:     {total_stars}",
            f"Languages: {', '.join(top_langs) if top_langs else 'N/A'}",
        ]
        return Panel("\n".join(lines), border_style="blue")

    console.print(Columns([make_panel(user1, repos1), make_panel(user2, repos2)]))
