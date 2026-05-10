from typing import Any


def normalize(value: float, min_val: float, max_val: float) -> float:
    """Min-max normalize a value to [0, 1]. Safe against division by zero."""
    if max_val == min_val:
        return 0.0
    return max(0.0, min(1.0, (value - min_val) / (max_val - min_val)))


def clamp(value: float, lo: float = 0.0, hi: float = 1.0) -> float:
    """Clamp a float to [lo, hi]."""
    return max(lo, min(hi, value))


def weighted_sum(components: list[tuple[float, float]]) -> float:
    """
    Compute a weighted sum of (value, weight) pairs.
    Weights need not sum to 1 — result is normalized by total weight.
    """
    total_weight = sum(w for _, w in components)
    if total_weight == 0:
        return 0.0
    return sum(v * w for v, w in components) / total_weight
