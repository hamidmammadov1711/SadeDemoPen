from backend.services.report_gen import generate_report

def test_generate_report_high_risk():
    dummy = {"details": "22/tcp open ssh\n80/tcp open http\n443/tcp open https"}
    report = generate_report(dummy)
    assert report["risk_score"] == 6
    assert report["category"] == "High Risk"
    assert "Close unused ports" in report["recommendation"]

def test_generate_report_secure():
    dummy = {"details": "All ports closed"}
    report = generate_report(dummy)
    assert report["risk_score"] == 0
    assert report["category"] == "Low Risk"
    assert "System appears secure" in report["recommendation"]
