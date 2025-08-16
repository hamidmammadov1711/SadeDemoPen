from backend.utils.sandbox import safe_run

def test_safe_run_valid_command():
    output = safe_run(["echo", "hello"])
    assert "hello" in output

def test_safe_run_timeout():
    output = safe_run(["ping", "127.0.0.1", "-n", "10"], timeout=1)
    assert "timed out" in output.lower() or "Error" in output
