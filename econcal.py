#!/usr/bin/env python3
"""
Global Economic Events Calendar - CLI
======================================

NOTE: This file is named ``econcal.py`` (not ``calendar.py``) to avoid
shadowing Python's built-in ``calendar`` module.

Commands::

    python econcal.py today              # Today's events
    python econcal.py week               # This week's events
    python econcal.py month              # This month's events (table)
    python econcal.py month --region CN,US  # Filter by region
    python econcal.py dashboard          # Generate HTML dashboard
    python econcal.py stats             # Event database statistics
    python econcal.py live              # Fetch live data via akshare

Examples::

    python econcal.py today
    python econcal.py week --min-impact 3
    python econcal.py month -m 9
    python econcal.py dashboard -o calendar.html
"""

import calendar as cal_mod
import sys
from datetime import date, datetime, timedelta
from typing import List, Optional

try:
    import click
except ImportError:
    print("Error: click is required. Run: pip install click rich")
    sys.exit(1)

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.text import Text
    from rich import box
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

from econ_calendar.events import EventDatabase, get_events, list_regions, Region
from econ_calendar.fetcher import MacroFetcher, fetch_cn_macro
from econ_calendar.dashboard import DashboardGenerator, generate_dashboard


console = Console() if RICH_AVAILABLE else None

IMPACT_LABELS = {
    1: "[dim green]1 star [/]",
    2: "[green]2 stars[/]",
    3: "[yellow]3 stars[/]",
    4: "[bold orange1]4 stars[/]",
    5: "[bold red]5 stars[/]",
}

REGION_EMOJI = {
    "CN": "[red]CN[/]",
    "US": "[blue]US[/]",
    "EU": "[cyan]EU[/]",
    "JP": "[magenta]JP[/]",
    "GLOBAL": "[bright_black]GL[/]",
}

IMPACT_PLAIN = {1: "*", 2: "**", 3: "***", 4: "****", 5: "*****"}


def _print_rich_events(events: List[dict], title: str):
    """Pretty-print events using rich table."""
    if not events:
        console.print(f"\n[bold]{title}[/]\n  [dim]No events found.[/]")
        return

    table = Table(title=title, box=box.ROUNDED, border_style="bright_black")
    table.add_column("Date", style="cyan", width=12)
    table.add_column("Rgn", width=4)
    table.add_column("Impact", width=10)
    table.add_column("Event", style="bold")
    table.add_column("Markets", style="dim")

    for e in events:
        imp = IMPACT_LABELS.get(e["impact"], f"{e['impact']} stars")
        rgn = REGION_EMOJI.get(e["region"], e["region"])
        markets = ", ".join(e.get("markets_impacted", [])[:3])
        table.add_row(
            e["date"],
            rgn,
            imp,
            e["title"],
            markets,
        )

    console.print(table)


def _print_plain_events(events: List[dict], title: str):
    """Fallback plain-text output when rich is not available."""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}")
    if not events:
        print("  No events found.")
        return
    for e in events:
        stars = "\u2605" * e["impact"]
        markets = ", ".join(e.get("markets_impacted", [])[:3])
        print(f"  {e['date']} | {stars:6s} | {e['region']:3s} | {e['title']}")
        if markets:
            print(f"  {'':12s} Markets: {markets}")
        print(f"  {'':12s} {e.get('description', '')[:80]}")
        print()


# ═══════════════════════════════════════════════════════════
# CLI Commands
# ═══════════════════════════════════════════════════════════

@click.group()
@click.version_option(version="1.0.0", prog_name="econ-calendar")
def cli():
    """Global Economic Events Calendar - Market-moving events at a glance.

    Covers China (NBS, PBoC), US (FOMC, BLS), EU (ECB, Eurostat),
    and Japan (BOJ, MoF) with 50+ pre-scheduled events for 2026 Q3-Q4.
    """


@cli.command()
@click.option("--region", "-r", default=None, help="Filter by region (CN/US/EU/JP)")
@click.option("--min-impact", "-i", default=1, type=int, help="Minimum impact rating (1-5)")
def today(region, min_impact):
    """Show today's economic events."""
    t = date.today()
    db = EventDatabase()
    events = db.by_date_range(t, t)

    if region:
        r = Region(region.upper())
        events = [e for e in events if e.region == r]
    events = [e for e in events if e.impact >= min_impact]

    result = [e.to_dict() for e in events]
    title = f"Today's Events - {t.strftime('%A, %B %d, %Y')}"
    if RICH_AVAILABLE:
        _print_rich_events(result, title)
    else:
        _print_plain_events(result, title)

    if not result:
        # fallback: show nearest upcoming
        upcoming = db.upcoming(ref_date=t, days=7)
        if region:
            upcoming = [e for e in upcoming if e.region == Region(region.upper())]
        upcoming = [e for e in upcoming if e.impact >= min_impact]
        if upcoming:
            upcoming = sorted(upcoming, key=lambda e: (e.date, -e.impact))
            print(f"\n  Nearest upcoming events in the next 7 days:")
            for e in upcoming[:5]:
                stars = "\u2605" * e.impact
                print(f"    {e.date} | {stars} | {e.region.value} | {e.title}")


@cli.command()
@click.option("--region", "-r", default=None, help="Filter by region (comma-separated: CN,US)")
@click.option("--min-impact", "-i", default=1, type=int, help="Minimum impact rating (1-5)")
def week(region, min_impact):
    """Show this week's economic events."""
    t = date.today()
    # Monday of current week
    start = t - timedelta(days=t.weekday())
    end = start + timedelta(days=6)

    db = EventDatabase()
    events = db.by_date_range(start, end)

    if region:
        regions = {r.strip().upper() for r in region.split(",")}
        events = [e for e in events if e.region.value in regions]
    events = [e for e in events if e.impact >= min_impact]

    result = [e.to_dict() for e in events]
    result.sort(key=lambda x: (x["date"], -x["impact"]))

    title = f"Week of {start.strftime('%b %d')} - {end.strftime('%b %d, %Y')}"
    if RICH_AVAILABLE:
        _print_rich_events(result, title)

        # Weekly summary
        high = sum(1 for e in events if e.impact >= 4)
        critical = sum(1 for e in events if e.impact == 5)
        console.print(
            f"\n  [dim]Total: {len(events)} events  |  "
            f"High Impact: {high}  |  Critical: {critical}[/]"
        )
    else:
        _print_plain_events(result, title)
        high = sum(1 for e in events if e.impact >= 4)
        critical = sum(1 for e in events if e.impact == 5)
        print(f"  Total: {len(events)} | High: {high} | Critical: {critical}")


@cli.command()
@click.option("--month", "-m", default=None, type=int, help="Month (1-12). Default: current.")
@click.option("--year", "-y", default=None, type=int, help="Year. Default: current.")
@click.option("--region", "-r", default=None, help="Filter by region (comma-separated).")
@click.option("--min-impact", "-i", default=1, type=int, help="Minimum impact rating.")
def month(month, year, min_impact, region):
    """Show all events for a specific month."""
    t = date.today()
    if month is None:
        month = t.month
    if year is None:
        year = t.year

    db = EventDatabase()
    events = db.by_month(year, month)

    if region:
        regions = {r.strip().upper() for r in region.split(",")}
        events = [e for e in events if e.region.value in regions]
    events = [e for e in events if e.impact >= min_impact]

    events.sort(key=lambda e: (e.date, -e.impact))
    result = [ev.to_dict() for ev in events]

    title = f"{cal_mod.month_name[month]} {year} - Economic Events"
    if RICH_AVAILABLE:
        _print_rich_events(result, title)

        # Group by week
        console.print(f"\n  [bold underline]Weekly Breakdown:[/]")
        weeks = {}
        for e in events:
            week_num = e.date.isocalendar()[1]
            if week_num not in weeks:
                weeks[week_num] = {"count": 0, "high": 0}
            weeks[week_num]["count"] += 1
            if e.impact >= 4:
                weeks[week_num]["high"] += 1

        for wk in sorted(weeks):
            w = weeks[wk]
            bar = "[bold red]" + "|" * w["high"] + "[/]" + "[dim]" + "." * (w["count"] - w["high"]) + "[/]"
            console.print(f"    Week {wk}: {bar}  {w['count']} events ({w['high']} high impact)")
    else:
        _print_plain_events(result, title)

    # Summary
    total = len(events)
    high = sum(1 for e in events if e.impact >= 4)
    critical = sum(1 for e in events if e.impact == 5)
    cn = sum(1 for e in events if e.region == Region.CN)
    us = sum(1 for e in events if e.region == Region.US)
    eu = sum(1 for e in events if e.region == Region.EU)
    jp = sum(1 for e in events if e.region == Region.JP)
    print(f"\n  Summary: {total} events (CN:{cn} US:{us} EU:{eu} JP:{jp}) | "
          f"High: {high} | Critical: {critical}")


@cli.command()
@click.option("--output", "-o", default="dashboard.html", help="Output HTML file path.")
@click.option("--month", "-m", default=None, type=int, help="Month (1-12).")
@click.option("--year", "-y", default=None, type=int, help="Year.")
def dashboard(output, month, year):
    """Generate an interactive HTML dashboard."""
    path = generate_dashboard(output, year=year, month=month)
    print(f"\n  Dashboard generated: {path}")
    print(f"  Open in browser: file:///{path.replace(chr(92), '/')}")


@cli.command()
def stats():
    """Show event database statistics."""
    db = EventDatabase()
    s = db.summary()

    if RICH_AVAILABLE:
        table = Table(title="Event Database Statistics", box=box.ROUNDED)
        table.add_column("Metric", style="bold cyan")
        table.add_column("Value", style="green")

        table.add_row("Total Events", str(s["total_events"]))

        for region, count in sorted(s["by_region"].items()):
            table.add_row(f"  {region} Events", str(count))

        table.add_section()
        table.add_row("By Impact Level", "")
        for level in range(5, 0, -1):
            table.add_row(f"  {level} Stars", str(s["by_impact"].get(level, 0)))

        table.add_section()
        table.add_row("By Category", "")
        for cat, count in sorted(s["by_category"].items(), key=lambda x: -x[1]):
            table.add_row(f"  {cat}", str(count))

        console.print(table)
    else:
        print(f"\nEvent Database Statistics")
        print(f"{'='*40}")
        print(f"Total Events: {s['total_events']}")
        print(f"\nBy Region:")
        for region, count in sorted(s["by_region"].items()):
            print(f"  {region}: {count}")
        print(f"\nBy Impact:")
        for level in range(5, 0, -1):
            print(f"  {level} stars: {s['by_impact'].get(level, 0)}")
        print(f"\nBy Category:")
        for cat, count in sorted(s["by_category"].items(), key=lambda x: -x[1]):
            print(f"  {cat}: {count}")


@cli.command()
@click.option("--region", "-r", default="CN", help="Region to fetch (CN supported via akshare).")
def live(region):
    """Fetch live/recent economic data via akshare or web sources."""
    fetcher = MacroFetcher()

    if region.upper() == "CN":
        print("\n  Fetching China macro data via akshare...")
        if not MacroFetcher.check_akshare_available():
            print("  [WARN] akshare not installed. Run: pip install akshare")
            print("  Showing pre-built database events instead.\n")
            db = EventDatabase()
            events = db.by_region("CN")
            events.sort(key=lambda e: e.date)
            for e in events[:10]:
                stars = "\u2605" * e.impact
                print(f"    {e.date} | {stars} | {e.title}")
            return

        data = fetch_cn_macro()
        if data:
            for item in data:
                print(f"    {item['title']}: {item.get('value', 'N/A')}")
        else:
            print("    No live data returned. Check network or akshare version.")

        # Also show upcoming from DB
        print(f"\n  Upcoming China events (next 14 days):")
        db = EventDatabase()
        t = date.today()
        upcoming = db.upcoming(ref_date=t, days=14)
        upcoming = [e for e in upcoming if e.region == Region.CN]
        for e in upcoming[:8]:
            stars = "\u2605" * e.impact
            print(f"    {e.date} | {stars} | {e.title}")
    else:
        print(f"\n  Fetching events for {region}...")
        upcoming = fetcher.fetch_upcoming(days=14)
        filtered = [e for e in upcoming if e.get("region") == region.upper()]
        if not filtered:
            print(f"  No events found for {region} in the next 14 days.")
            return
        for e in filtered[:10]:
            stars = "\u2605" * e.get("impact", 1)
            print(f"    {e.get('date', '?')} | {stars} | {e.get('title', 'Unknown')}")


@cli.command()
def regions():
    """List available regions."""
    for r in list_regions():
        label = {
            "CN": "China (NBS, PBoC)",
            "US": "United States (FOMC, BLS)",
            "EU": "Eurozone (ECB, Eurostat)",
            "JP": "Japan (BOJ, MoF)",
            "GLOBAL": "Global (OPEC, G20, holidays)",
        }.get(r, r)
        print(f"  {r}: {label}")


@cli.command()
@click.argument("keyword")
def search(keyword):
    """Search events by keyword (title or category)."""
    db = EventDatabase()
    kw = keyword.lower()
    events = [
        e for e in db.events
        if kw in e.title.lower() or kw in e.category.lower() or kw in e.description.lower()
    ]
    events.sort(key=lambda e: (e.date, -e.impact))

    if not events:
        print(f"\n  No events found matching '{keyword}'.")
        return

    result = [e.to_dict() for e in events]
    title = f"Search Results: '{keyword}' ({len(result)} events)"
    if RICH_AVAILABLE:
        _print_rich_events(result, title)
    else:
        _print_plain_events(result, title)


if __name__ == "__main__":
    cli()
