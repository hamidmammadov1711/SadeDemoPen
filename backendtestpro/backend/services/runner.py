import subprocess
import socket

def run_test(target: str) -> dict:
    result = {
        "target": target,
        "status": "UNKNOWN",
        "details": [],
    }

    # 1️⃣ DNS yoxlaması
    try:
        ip = socket.gethostbyname(target)
        result["details"].append(f"Resolved IP: {ip}")
    except Exception as e:
        result["details"].append(f"DNS resolution failed: {e}")
        result["status"] = "ERROR"
        return result

    # 2️⃣ Nmap scan (simulyasiya və ya real)
    try:
        nmap_output = subprocess.check_output(
            ["nmap", "-Pn", "-T4", "-F", target],
            stderr=subprocess.STDOUT,
            text=True,
            timeout=10
        )
        result["details"].append("Nmap scan completed")
        result["details"].append(nmap_output)
    except subprocess.TimeoutExpired:
        result["details"].append("Nmap scan timed out")
    except Exception as e:
        result["details"].append(f"Nmap error: {e}")

    # 3️⃣ Whois məlumatı
    try:
        whois_output = subprocess.check_output(
            ["whois", target],
            stderr=subprocess.STDOUT,
            text=True,
            timeout=5
        )
        result["details"].append("Whois info:")
        result["details"].append(whois_output[:300])  # İlk 300 simvol
    except Exception as e:
        result["details"].append(f"Whois error: {e}")

    result["status"] = "COMPLETED"
    return result
