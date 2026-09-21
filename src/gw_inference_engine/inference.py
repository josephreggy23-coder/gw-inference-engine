from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PosteriorSummary:
    chirp_mass: float
    lower_90: float
    upper_90: float


def summarize(best_mass: float, matched_snr: float) -> PosteriorSummary:
    width = max(0.5, 10 / max(matched_snr, 1))
    return PosteriorSummary(best_mass, round(best_mass - width, 2), round(best_mass + width, 2))
