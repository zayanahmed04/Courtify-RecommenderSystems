"""
Synthetic matchmaking dataset generator.

Compatibility label assignment uses skill-level as the primary axis,
with win_rate and games_played as secondary modifiers to introduce
realistic class noise and avoid a perfectly separable dataset.
"""

import random
import pandas as pd
from pathlib import Path

from app.core.constants import (
    SUPPORTED_SPORTS,
    PLAY_STYLES,
    AGE_GROUPS,
    LOCATION_ZONES,
    DATASET_SIZE,
    RANDOM_STATE,
    COMPATIBILITY_LOW,
    COMPATIBILITY_MID,
    COMPATIBILITY_HIGH,
)
from app.core.exceptions import DataGenerationError
from app.logging_config import get_logger

logger = get_logger(__name__)


def _assign_compatibility(skill: int, win_rate: float, games_played: int) -> int:
    """
    Heuristic compatibility label (0=Low, 1=Mid, 2=High).

    Primary: skill tier.
    Secondary modifiers: win_rate and experience can bump up/down by 1 tier.
    """
    if skill <= 3:
        base = COMPATIBILITY_LOW
    elif skill <= 6:
        base = COMPATIBILITY_MID
    else:
        base = COMPATIBILITY_HIGH

    # Experienced high-win-rate players get a bump
    if win_rate >= 0.80 and games_played >= 200:
        base = min(COMPATIBILITY_HIGH, base + 1)

    # Inexperienced low-win-rate players get a penalty
    if win_rate <= 0.30 and games_played <= 20:
        base = max(COMPATIBILITY_LOW, base - 1)

    return base


def generate_record(rng: random.Random) -> dict:
    skill = rng.randint(1, 10)
    win_rate = round(rng.uniform(0.2, 0.95), 2)
    games_played = rng.randint(1, 500)

    return {
        "skill_level": skill,
        "preferred_sport": rng.choice(SUPPORTED_SPORTS),
        "play_style": rng.choice(PLAY_STYLES),
        "availability_hours": rng.randint(1, 24),
        "avg_session_duration": rng.randint(30, 180),
        "win_rate": win_rate,
        "age_group": rng.choice(AGE_GROUPS),
        "location_zone": rng.choice(LOCATION_ZONES),
        "games_played": games_played,
        "match_compatibility": _assign_compatibility(skill, win_rate, games_played),
    }


def generate_dataset(
    size: int = DATASET_SIZE,
    output_path: str = "data/processed/matchmaking_dataset.csv",
    seed: int = RANDOM_STATE,
) -> pd.DataFrame:
    rng = random.Random(seed)
    records = [generate_record(rng) for _ in range(size)]
    df = pd.DataFrame(records)

    dist = df["match_compatibility"].value_counts().to_dict()
    logger.info("dataset_generated", size=size, class_distribution=dist)

    # Validate class balance — warn if any class < 10%
    for cls, count in dist.items():
        if count / size < 0.10:
            logger.warning("class_imbalance_detected", cls=cls, count=count, size=size)

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    logger.info("dataset_saved", path=output_path)

    return df


if __name__ == "__main__":
    generate_dataset()
