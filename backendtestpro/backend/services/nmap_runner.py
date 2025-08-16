# nmap_runner.py
# Pentest araçları için kodlar
import subprocess

# backend/services/nmap_runner.py
def run_nmap(target: str) -> dict:
    import subprocess
    try:
        result = subprocess.run([
            "nmap", "-Pn", "-p", "22,80,443,9999", target
        ], capture_output=True, text=True, timeout=30)
        output = result.stdout
        status = "COMPLETED" if result.returncode == 0 else "ERROR"
        details = [line for line in output.splitlines() if "open" in line]
        return {
            "status": status,
            "details": details,
            "target": target
        }
    except Exception as e:
        return {
            "status": "ERROR",
            "details": str(e),
            "target": target
        }
