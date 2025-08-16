from typing import List

def ai_analyze(results: List[dict]) -> dict:
    # Dummy AI analiz
    criticals = [r for r in results if "CRITICAL" in r.get("details", "")]
    warnings = [r for r in results if "WARNING" in r.get("details", "")]
    advice = []
    if criticals:
        advice.append("Sistemdə kritik risklər var, dərhal müdaxilə edin!")
    if warnings:
        advice.append("Bəzi endpointlərdə gecikmə var, optimizasiya tövsiyə olunur.")
    if not advice:
        advice.append("Sisteminiz stabil görünür.")
    return {
        "critical_count": len(criticals),
        "warning_count": len(warnings),
        "advice": advice
    }
