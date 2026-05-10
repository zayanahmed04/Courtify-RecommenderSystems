"""
Script: benchmark_astar.py
Benchmarks A* search engine performance across increasing court set sizes.
Outputs a latency table and optionally a matplotlib chart.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
import statistics
from app.models.court import Court, CourtSearchQuery
from app.services.court_search.astar_engine import AStarCourtSearch
from app.core.exceptions import NoCourtsFoundError


RUNS_PER_SIZE = 10
COURT_COUNTS = [50, 100, 250, 500, 1000, 2500, 5000]
SPORTS = ["Padel", "Cricket", "Football", "Badminton", "Basketball"]


def make_courts(n: int) -> list[Court]:
    return [
        Court(
            id=i,
            name=f"Court {i}",
            sport=SPORTS[i % len(SPORTS)],
            latitude=24.86 + (i % 50) * 0.01,
            longitude=67.00 + (i % 50) * 0.01,
            price_per_hour=500 + (i % 10) * 200,
            rating=round(3.0 + (i % 20) * 0.1, 1),
            available_slots=["6PM"],
        )
        for i in range(n)
    ]


def benchmark():
    query = CourtSearchQuery(
        sport="Padel",
        budget=5000,
        location=(24.8607, 67.0011),
        max_results=5,
    )

    print("\n" + "=" * 65)
    print(f"  CourtFind AI — A* Benchmark ({RUNS_PER_SIZE} runs per size)")
    print("=" * 65)
    print(f"  {'Courts':>8}  {'Min (ms)':>10}  {'Mean (ms)':>10}  {'Max (ms)':>10}  {'p95 (ms)':>10}")
    print("-" * 65)

    for n in COURT_COUNTS:
        courts = make_courts(n)
        engine = AStarCourtSearch(courts)
        latencies = []

        for _ in range(RUNS_PER_SIZE):
            t0 = time.perf_counter()
            try:
                engine.search(query)
            except NoCourtsFoundError:
                pass
            latencies.append((time.perf_counter() - t0) * 1000)

        latencies.sort()
        p95 = latencies[int(len(latencies) * 0.95)]

        print(
            f"  {n:>8}  "
            f"{min(latencies):>10.2f}  "
            f"{statistics.mean(latencies):>10.2f}  "
            f"{max(latencies):>10.2f}  "
            f"{p95:>10.2f}"
        )

    print("=" * 65)
    print("\n  All latencies in milliseconds.\n")


if __name__ == "__main__":
    benchmark()
