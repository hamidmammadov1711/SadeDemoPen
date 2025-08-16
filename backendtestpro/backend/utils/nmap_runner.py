import subprocess
from backend.utils.sandbox import safe_run


def run_nmap(target: str) -> str:
    try:
        result = subprocess.run(
            ["nmap", "-Pn", target],
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.stdout
    except Exception as e:
        return f"Error: {str(e)}"
