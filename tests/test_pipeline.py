from gw_inference_engine.pipeline import run


def test_recovery_is_repeatable_and_has_signal():
    result = run(seed=4)
    assert result == run(seed=4)
    assert result["snr"] > 1
    assert result["posterior"].lower_90 < result["posterior"].chirp_mass < result["posterior"].upper_90
