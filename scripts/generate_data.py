"""
Script: generate_data.py
Generates synthetic matchmaking dataset and sample court CSV.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from pathlib import Path
from app.services.matchmaking.dataset_generator import generate_dataset
from app.core.constants import SUPPORTED_SPORTS, DATASET_SIZE


def generate_courts_csv(output_path: str = "data/raw/courts.csv") -> None:
    import random
    rng = random.Random(42)

    zones = {
        "North": (24.93, 67.06),
        "South": (24.81, 67.03),
        "Central": (24.86, 67.01),
        "East": (24.83, 67.13),
        "West": (24.87, 66.99),
    }

    records = []
    court_id = 1
    for sport in SUPPORTED_SPORTS:
        for zone, (base_lat, base_lon) in zones.items():
            for _ in range(4):
                lat = base_lat + rng.uniform(-0.02, 0.02)
                lon = base_lon + rng.uniform(-0.02, 0.02)
                records.append({
                    "id": court_id,
                    "name": f"{zone} {sport} Court {court_id}",
                    "sport": sport,
                    "latitude": round(lat, 6),
                    "longitude": round(lon, 6),
                    "price_per_hour": rng.choice([500, 600, 800, 1000, 1200, 1500, 2000]),
                    "rating": round(rng.uniform(3.0, 5.0), 1),
                    "available_slots": ",".join(
                        rng.sample(["6AM", "7AM", "8AM", "3PM", "4PM", "5PM", "6PM", "7PM", "8PM"], 3)
                    ),
                })
                court_id += 1

    df = pd.DataFrame(records)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"[courts] Generated {len(df)} courts → {output_path}")


if __name__ == "__main__":
    print(f"[dataset] Generating {DATASET_SIZE} matchmaking records...")
    df = generate_dataset(
        size=DATASET_SIZE,
        output_path="data/processed/matchmaking_dataset.csv",
        seed=42,
    )
    dist = df["match_compatibility"].value_counts().to_dict()
    print(f"[dataset] Class distribution: {dist}")
    print(f"[dataset] Saved → data/processed/matchmaking_dataset.csv")

    print("\n[courts] Generating court CSV...")
    generate_courts_csv()
    print("\n✅  Data generation complete.")
