from __future__ import annotations

import math


def chirp_mass(mass_1: float, mass_2: float) -> float:
    return (mass_1 * mass_2) ** (3 / 5) / (mass_1 + mass_2) ** (1 / 5)


def inspiral(duration: float, sample_rate: int, mass_1: float, mass_2: float) -> list[float]:
    """A compact, non-calibrated chirp suitable only for pipeline tests."""
    samples = int(duration * sample_rate)
    mc = chirp_mass(mass_1, mass_2)
    series = []
    phase = 0.0
    for index in range(samples):
        progress = index / max(samples - 1, 1)
        final_frequency = min(35 + 2.8 * mc, sample_rate * 0.42)
        frequency = 20 + (final_frequency - 20) * progress**2
        phase += 2 * math.pi * frequency / sample_rate
        amplitude = 0.025 + 0.16 * progress**2
        series.append(amplitude * math.sin(phase))
    return series
