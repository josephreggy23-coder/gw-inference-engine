from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from .detector import inject
from .inference import summarize
from .search import best_template, snr
from .waveforms import chirp_mass, inspiral


def _frame(title: str, body: str, subtitle: str) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="600" viewBox="0 0 960 600">
<rect width="960" height="600" rx="18" fill="#070b18"/>
<text x="52" y="48" fill="#f8fafc" font-family="Segoe UI, sans-serif" font-size="25" font-weight="700">{title}</text>
<text x="52" y="75" fill="#94a3b8" font-family="Segoe UI, sans-serif" font-size="14">{subtitle}</text>
{body}
</svg>'''


def _line_points(values: list[float], left: float, top: float, width: float, height: float, minimum: float, maximum: float) -> str:
    span = max(maximum - minimum, 1e-12)
    return " ".join(f"{left + index / max(len(values) - 1, 1) * width:.1f},{top + height - (value - minimum) / span * height:.1f}" for index, value in enumerate(values))


def _strain_chart(signal: list[float], data: list[float], sample_rate: int) -> str:
    minimum, maximum = min(data), max(data)
    noisy = _line_points(data, 70, 125, 840, 330, minimum, maximum)
    clean = _line_points(signal, 70, 125, 840, 330, minimum, maximum)
    body = f'''<line x1="70" y1="455" x2="910" y2="455" stroke="#475569"/>
<line x1="70" y1="125" x2="70" y2="455" stroke="#475569"/>
<polyline points="{noisy}" fill="none" stroke="#64748b" stroke-width="1.2" stroke-opacity="0.70"/>
<polyline points="{clean}" fill="none" stroke="#22d3ee" stroke-width="2.5"/>
<line x1="690" y1="510" x2="735" y2="510" stroke="#22d3ee" stroke-width="3"/><text x="748" y="515" fill="#cbd5e1" font-family="Segoe UI, sans-serif" font-size="13">injected signal</text>
<line x1="690" y1="535" x2="735" y2="535" stroke="#64748b" stroke-width="3"/><text x="748" y="540" fill="#cbd5e1" font-family="Segoe UI, sans-serif" font-size="13">noisy strain</text>
<text x="490" y="535" text-anchor="middle" fill="#94a3b8" font-family="Segoe UI, sans-serif" font-size="14">time (0–{len(data) / sample_rate:.1f} s)</text>'''
    return _frame("Synthetic compact-binary signal injection", body, f"{len(data)} samples at {sample_rate} Hz • deterministic Gaussian noise")


def _score_chart(scores: list[tuple[float, float]], injected: float) -> str:
    values = [score for _, score in scores]
    minimum, maximum = min(values), max(values)
    points = " ".join(f"{80 + index / max(len(scores) - 1, 1) * 810:.1f},{455 - (score - minimum) / max(maximum - minimum, 1e-12) * 325:.1f}" for index, (_, score) in enumerate(scores))
    injected_x = 80 + (injected - scores[0][0]) / (scores[-1][0] - scores[0][0]) * 810
    body = f'''<line x1="80" y1="455" x2="890" y2="455" stroke="#475569"/>
<line x1="80" y1="130" x2="80" y2="455" stroke="#475569"/>
<line x1="{injected_x:.1f}" y1="130" x2="{injected_x:.1f}" y2="455" stroke="#f472b6" stroke-width="2" stroke-dasharray="7 7"/>
<polyline points="{points}" fill="none" stroke="#a78bfa" stroke-width="3" stroke-linejoin="round"/>
<text x="{injected_x + 8:.1f}" y="150" fill="#f9a8d4" font-family="Segoe UI, sans-serif" font-size="13">injected chirp mass</text>
<text x="485" y="520" text-anchor="middle" fill="#94a3b8" font-family="Segoe UI, sans-serif" font-size="14">template chirp mass (solar-mass units)</text>'''
    return _frame("Template-bank response", body, "27 templates • peak response should track the injected chirp mass")


def build_report(output_dir: Path, mass_1: float = 36, mass_2: float = 29, seed: int = 2) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    duration, sample_rate = 2.0, 256
    signal = inspiral(duration, sample_rate, mass_1, mass_2)
    data = inject(signal, seed)
    templates = {round(chirp_mass(mass, mass), 2): inspiral(duration, sample_rate, mass, mass) for mass in range(8, 61, 2)}
    scores = sorted((mass, snr(data, waveform)) for mass, waveform in templates.items())
    recovered_mass, matched_snr = best_template(data, templates)
    posterior = summarize(recovered_mass, matched_snr)
    injected_mass = chirp_mass(mass_1, mass_2)

    with (output_dir / "strain_timeseries.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["time_s", "injected_signal", "noisy_strain"])
        for index, (clean, noisy) in enumerate(zip(signal, data)):
            writer.writerow([f"{index / sample_rate:.8f}", f"{clean:.9f}", f"{noisy:.9f}"])

    with (output_dir / "template_scores.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["template_chirp_mass", "score"])
        for mass, score in scores:
            writer.writerow([mass, f"{score:.8f}"])

    summary = {
        "seed": seed,
        "component_masses": [mass_1, mass_2],
        "injected_chirp_mass": round(injected_mass, 4),
        "recovered_template_chirp_mass": recovered_mass,
        "absolute_recovery_error": round(abs(injected_mass - recovered_mass), 4),
        "matched_filter_like_score": round(matched_snr, 4),
        "posterior_style_interval": [posterior.lower_90, posterior.upper_90],
        "sample_rate_hz": sample_rate,
        "duration_s": duration,
        "samples": len(data),
        "template_count": len(templates),
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    (output_dir / "strain_recovery.svg").write_text(_strain_chart(signal, data, sample_rate), encoding="utf-8")
    (output_dir / "template_response.svg").write_text(_score_chart(scores, injected_mass), encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate GW benchmark data and charts.")
    parser.add_argument("--output", type=Path, default=Path("results/demo"))
    parser.add_argument("--mass-1", type=float, default=36)
    parser.add_argument("--mass-2", type=float, default=29)
    parser.add_argument("--seed", type=int, default=2)
    args = parser.parse_args()
    print(json.dumps(build_report(args.output, args.mass_1, args.mass_2, args.seed), indent=2))


if __name__ == "__main__":
    main()
