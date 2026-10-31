from __future__ import annotations

import random


def inject(signal: list[float], seed: int = 0, noise_sigma: float = 0.2) -> list[float]:
    """Return ``signal`` plus seeded white Gaussian noise with standard deviation ``noise_sigma``."""
    rng = random.Random(seed)
    return [sample + rng.gauss(0, noise_sigma) for sample in signal]
