"""
CLI demo — runs the full CourtFind AI pipeline interactively.
Usage: python -m app.cli.demo
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

from app.models.court import Court, CourtSearchQuery
from app.services.court_search.astar_engine import AStarCourtSearch
from app.core.exceptions import NoCourtsFoundError

console = Console()

DEMO_COURTS = [
    Court(id=1, name="Padel Arena DHA", sport="Padel", latitude=24.7966, longitude=67.0681, price_per_hour=1500, rating=4.7, available_slots=["6PM", "7PM"]),
    Court(id=2, name="Clifton Padel Club", sport="Padel", latitude=24.8121, longitude=67.0299, price_per_hour=1200, rating=4.2, available_slots=["5PM"]),
    Court(id=3, name="Green Court Badminton", sport="Badminton", latitude=24.8607, longitude=67.0011, price_per_hour=600, rating=4.5, available_slots=["7AM", "5PM"]),
    Court(id=4, name="Korangi Cricket Ground", sport="Cricket", latitude=24.8324, longitude=67.1282, price_per_hour=800, rating=3.9, available_slots=["6AM"]),
    Court(id=5, name="Defence Padel Club", sport="Padel", latitude=24.8221, longitude=67.0711, price_per_hour=2000, rating=4.9, available_slots=["9AM", "6PM"]),
    Court(id=6, name="PECHS Basketball Court", sport="Basketball", latitude=24.8780, longitude=67.0580, price_per_hour=800, rating=4.4, available_slots=["4PM", "7PM"]),
]


def demo_court_search():
    console.print(Panel("[bold emerald]🎾 A* Court Search Demo[/bold emerald]", expand=False))

    query = CourtSearchQuery(
        sport="Padel",
        budget=1600,
        location=(24.8607, 67.0011),
        max_results=3,
    )

    console.print(f"\n  Sport  : [cyan]{query.sport}[/cyan]")
    console.print(f"  Budget : [cyan]PKR {query.budget}/hr[/cyan]")
    console.print(f"  Coords : [cyan]{query.location}[/cyan]\n")

    engine = AStarCourtSearch(DEMO_COURTS)
    try:
        response = engine.search(query)
    except NoCourtsFoundError as e:
        console.print(f"[red]{e}[/red]")
        return

    table = Table(box=box.ROUNDED, show_header=True, header_style="bold magenta")
    table.add_column("Rank", justify="center", width=6)
    table.add_column("Court Name", min_width=24)
    table.add_column("Score", justify="right")
    table.add_column("Rating", justify="right")
    table.add_column("Price/hr", justify="right")
    table.add_column("Distance", justify="right")
    table.add_column("Slots")

    for i, rec in enumerate(response.recommendations, 1):
        table.add_row(
            str(i),
            rec.court,
            f"{rec.score:.4f}",
            f"⭐ {rec.rating}",
            f"PKR {rec.price}",
            f"{rec.distance_km} km",
            ", ".join(rec.available_slots) if rec.available_slots else "—",
        )

    console.print(table)


def demo_matchmaking():
    console.print(Panel("[bold cyan]🤝 ML Matchmaking Demo[/bold cyan]", expand=False))

    try:
        from app.services.matchmaking.inference import MatchmakingInference
        from app.core.exceptions import ModelNotTrainedError

        engine = MatchmakingInference()
        player = {
            "skill_level": 8,
            "preferred_sport": "Padel",
            "play_style": "Aggressive",
            "availability_hours": 10,
            "avg_session_duration": 90,
            "win_rate": 0.78,
            "age_group": "Young Adult",
            "location_zone": "South",
            "games_played": 150,
        }

        console.print("\n  [bold]Player Profile[/bold]")
        for k, v in player.items():
            console.print(f"    {k:<26}: [cyan]{v}[/cyan]")

        result = engine.predict(player)
        console.print(f"\n  Compatibility : [bold green]{result.compatibility_label}[/bold green]")
        console.print(f"  Confidence    : [bold]{result.confidence:.2%}[/bold]")
        console.print(f"  Recommendation: {result.recommendation}\n")

    except Exception as e:
        console.print(f"\n  [yellow]ℹ  Matchmaking model not trained yet.[/yellow]")
        console.print(f"  [dim]Run: python scripts/train_model.py[/dim]\n")


if __name__ == "__main__":
    console.print(Panel(
        "[bold green]CourtFind AI — Production Demo[/bold green]\n"
        "[dim]AI-powered court discovery + player matchmaking[/dim]",
        expand=False,
    ))
    console.print()
    demo_court_search()
    console.print()
    demo_matchmaking()
