from __future__ import annotations

import argparse

from .detector import inject
from .inference import summarize
from .search import best_template
from .waveforms import chirp_mass, inspiral


def run(mass_1: float = 36, mass_2: float = 29, seed: int = 0) -> dict:
    duration, sample_rate = 2.0, 256
    signal = inspiral(duration, sample_rate, mass_1, mass_2)
    data = inject(signal, seed)
    templates = {round(chirp_mass(mass, mass), 2): inspiral(duration, sample_rate, mass, mass) for mass in range(8, 61, 2)}
    estimated_mass, matched_snr = best_template(data, templates)
    posterior = summarize(estimated_mass, matched_snr)
    return {"injected_chirp_mass": round(chirp_mass(mass_1, mass_2), 2), "snr": round(matched_snr, 2), "posterior": posterior}


def main() -> None:
    parser = argparse.ArgumentParser(description="Run an educational compact-binary recovery.")
    parser.add_argument("--mass-1", type=float, default=36)
    parser.add_argument("--mass-2", type=float, default=29)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()
    print(run(args.mass_1, args.mass_2, args.seed))


if __name__ == "__main__":
    main()
