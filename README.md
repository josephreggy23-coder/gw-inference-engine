# gw-inference-engine

A lightweight gravitational-wave inference teaching pipeline. It synthesizes compact-binary chirps, injects them into deterministic Gaussian detector noise, calculates matched-filter-like SNR, and estimates a posterior-like mass range from a small template bank.

## Quick start

```bash
python -m gw_inference_engine.pipeline --mass-1 36 --mass-2 29 --seed 2
pytest
```

## MVP snapshot

| Metric | Verified demo result |
| --- | ---: |
| Synthetic observation duration | 2.0 s |
| Sampling rate | 256 Hz (512 samples) |
| Injected chirp mass | 28.10 solar masses |
| Template bank | 27 equal-mass templates |
| Demonstration matched-filter SNR | 1.41 |

These values come from `python -m gw_inference_engine.pipeline --mass-1 36 --mass-2 29 --seed 2`. They are baseline diagnostics for a deterministic teaching model, not a calibrated astrophysical recovery or a claim about real detector data.

## What is implemented today

| Stage | MVP implementation | Next research integration |
| --- | --- | --- |
| Waveform | analytic chirp-mass helper and compact inspiral proxy | LALSuite, EOB, IMRPhenom, and NR surrogate |
| Detector | seeded Gaussian-noise injection | GWOSC strain, PSD estimation, and antenna patterns |
| Search | normalized time-domain template score | FFT matched filtering and chi-squared vetoes |
| Inference | SNR-shaped posterior summary | dynesty / NumPyro 15-parameter posterior |

The source tree preserves the production pipeline boundaries while keeping the first executable example dependency-light and fully deterministic.

This scaffold separates waveform, detector, search, inference, and post-merger packages so real GWOSC, LALSuite, PyCBC, dynesty, NumPyro, SXS, and ligo.skymap integrations can be added without changing the public workflow. The present signal model is educational and must not be used for scientific claims.
