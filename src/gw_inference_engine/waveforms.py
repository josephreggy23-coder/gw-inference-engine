from __future__ import annotations

import math


def chirp_mass(mass_1: float, mass_2: float) -> float:
    return (mass_1 * mass_2) ** (3 / 5) / (mass_1 + mass_2) ** (1 / 5)


def inspiral(duration: float, sample_rate: int, mass_1: float, mass_2: float) -> list[float]:
    """A compact, non-calibrated chirp suitable only for pipeline tests."""
    samples = int(duration * sample_rate)
    mc = chirp_mass(mass_1, mass_2)
    series = []
    for index in range(samples):
        remaining = max((samples - index) / sample_rate, 1 / sample_rate)
        frequency = min(20 + 16 * mc * remaining ** (-3 / 8), sample_rate / 3)
        phase = 2 * math.pi * frequency * index / sample_rate
        amplitude = 0.05 * (1 - index / samples) ** -0.25
        series.append(amplitude * math.sin(phase))
    return series
