"""Global seed setter for reproducible experiments."""

import random
import numpy as np
from app.core.constants import RANDOM_STATE


def set_global_seed(seed: int = RANDOM_STATE) -> None:
    random.seed(seed)
    np.random.seed(seed)
