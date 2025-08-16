import subprocess

def safe_run(command: list, timeout: int = 5) -> str:
    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout,
            cwd="sandbox",  # sandbox qovluğunda icra
            env={"PATH": "/usr/bin"}  # məhdud PATH
        )
        return result.stdout
    except subprocess.TimeoutExpired:
        return "Scan timed out"
    except Exception as e:
        return f"Error: {str(e)}"
