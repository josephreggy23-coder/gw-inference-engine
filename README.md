# gw-inference-engine

A lightweight gravitational-wave inference teaching pipeline. It synthesizes compact-binary chirps, injects them into deterministic Gaussian detector noise, calculates matched-filter-like SNR, and estimates a posterior-like mass range from a small template bank.

## Quick start

```bash
python -m gw_inference_engine.pipeline --mass-1 36 --mass-2 29 --seed 2
pytest
```

This scaffold separates waveform, detector, search, inference, and post-merger packages so real GWOSC, LALSuite, PyCBC, dynesty, NumPyro, SXS, and ligo.skymap integrations can be added without changing the public workflow. The present signal model is educational and must not be used for scientific claims.
