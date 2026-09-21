from __future__ import annotations

import math


def snr(data: list[float], template: list[float]) -> float:
    numerator = sum(datum * model for datum, model in zip(data, template))
    norm = math.sqrt(sum(model * model for model in template))
    return numerator / max(norm, 1e-12)


def best_template(data: list[float], templates: dict[float, list[float]]) -> tuple[float, float]:
    return max(((mass, snr(data, waveform)) for mass, waveform in templates.items()), key=lambda result: result[1])
