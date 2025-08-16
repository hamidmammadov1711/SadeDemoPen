from backend.services.runner import run_test

def test_run_test_valid_target():
    result = run_test("scanme.nmap.org")
    assert result["status"] == "COMPLETED"
    assert any("Nmap scan" in line for line in result["details"])
