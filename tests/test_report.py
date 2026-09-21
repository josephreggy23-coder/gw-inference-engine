from gw_inference_engine.report import build_report


def test_report_writes_data_and_charts(tmp_path):
    summary = build_report(tmp_path, seed=3)
    assert summary["samples"] == 512
    assert summary["template_count"] == 27
    assert summary["absolute_recovery_error"] < 5
    assert (tmp_path / "strain_recovery.svg").exists()
    assert (tmp_path / "template_scores.csv").exists()

