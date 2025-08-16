# report_gen.py
# Təkmilləşdirilmiş risk scoring və compliance analizi

from datetime import datetime

# Portlara görə risk, severity, recommendation və compliance mapping
PORT_RULES = {
    "22/tcp": {
        "score": 3,
        "severity": "High",
        "recommendation": "Disable SSH if not needed or restrict access via firewall.",
        "compliance": {
            "ISO_27001": ["A.9.2.3"],
            "PCI_DSS": ["Req 7.1"]
        }
    },
    "80/tcp": {
        "score": 2,
        "severity": "Medium",
        "recommendation": "Ensure HTTP is redirected to HTTPS.",
        "compliance": {
            "ISO_27001": ["A.10.1.1"],
            "GDPR": ["Art.32"],
            "PCI_DSS": ["Req 4.1"]
        }
    },
    "443/tcp": {
        "score": 2,
        "severity": "Medium",
        "recommendation": "Verify HTTPS certificate validity and configuration.",
        "compliance": {
            "ISO_27001": ["A.10.1.2"],
            "GDPR": ["Art.32"],
            "PCI_DSS": ["Req 4.2"]
        }
    }
}

def generate_report(scan_result: dict) -> dict:
    target = scan_result.get("target", "unknown")
    raw_details = scan_result.get("details", [])
    status = scan_result.get("status", "UNKNOWN")

    if isinstance(raw_details, str):
        details = raw_details.splitlines()
    else:
        details = raw_details

    ports_found = []
    severity_map = {}
    recommendations = []
    compliance_flags = {
        "ISO_27001": [],
        "GDPR": [],
        "PCI_DSS": []
    }

    score = 0
    for line in details:
        if "open" in line and "/" in line:
            ports_found.append(line)
            port = line.split()[0]

            rule = PORT_RULES.get(port)
            if rule:
                score += rule["score"]
                severity_map[line] = rule["severity"]
                recommendations.append(rule["recommendation"])
                for standard, flags in rule["compliance"].items():
                    compliance_flags[standard].extend(flags)
            else:
                score += 1
                severity_map[line] = "Low"
                recommendations.append(f"Review service on {port} and restrict if unnecessary.")

    category = (
        "High Risk" if score >= 6 else
        "Medium Risk" if score >= 3 else
        "Low Risk"
    )

    summary = f"{len(ports_found)} open ports detected. Risk score: {score}. Category: {category}."

    from datetime import UTC
    report = {
        "target": target,
        "status": status,
        "summary": summary,
        "risk_score": score,
        "category": category,
        "highlights": ports_found,
        "severity": severity_map,
        "recommendations": recommendations,
        "compliance_flags": compliance_flags,
        "timestamp": datetime.now(UTC).isoformat()
    }

    return report



def test_generate_report_high_risk():
    # 3 açıq port: SSH + HTTP + HTTPS
    dummy_result = {
        "target": "scanme.nmap.org",
        "status": "COMPLETED",
        "details": [
            "22/tcp   open  ssh",
            "80/tcp   open  http",
            "443/tcp  open  https"
        ]
    }
    report = generate_report(dummy_result)
    assert report["risk_score"] == 7
    assert report["category"] == "High Risk"
    assert "3 open ports detected" in report["summary"]

def test_generate_report_medium_risk():
    # 2 açıq port: HTTP + HTTPS
    dummy_result = {
        "target": "example.com",
        "status": "COMPLETED",
        "details": [
            "80/tcp   open  http",
            "443/tcp  open  https"
        ]
    }
    report = generate_report(dummy_result)
    assert report["risk_score"] == 4
    assert report["category"] == "Medium Risk"
    assert "2 open ports detected" in report["summary"]

def test_generate_report_low_risk():
    # 1 açıq port: 9999/tcp
    dummy_result = {
        "target": "test.local",
        "status": "COMPLETED",
        "details": [
            "9999/tcp open  custom"
        ]
    }
    report = generate_report(dummy_result)
    assert report["risk_score"] == 1
    assert report["category"] == "Low Risk"
    assert "1 open ports detected" in report["summary"]

def test_generate_report_no_ports():
    # Heç bir açıq port yoxdur
    dummy_result = {
        "target": "secure.host",
        "status": "COMPLETED",
        "details": [
            "All ports closed"
        ]
    }
    report = generate_report(dummy_result)
    assert report["risk_score"] == 0
    assert report["category"] == "Low Risk"
    assert "0 open ports detected" in report["summary"]

def test_generate_report_missing_fields():
    # `target` və `status` sahələri yoxdur
    dummy_result = {
        "details": [
            "22/tcp   open  ssh"
        ]
    }
    report = generate_report(dummy_result)
    assert report["target"] == "unknown"
    assert report["status"] == "UNKNOWN"
    assert report["risk_score"] == 3
    assert report["category"] == "Medium Risk"
def test_compliance_flags_for_known_ports():
    dummy_result = {
        "details": [
            "22/tcp   open  ssh",
            "80/tcp   open  http",
            "443/tcp  open  https"
        ]
    }
    report = generate_report(dummy_result)
    assert "A.9.2.3" in report["compliance_flags"]["ISO_27001"]
    assert "Art.32" in report["compliance_flags"]["GDPR"]
    assert "Req 4.2" in report["compliance_flags"]["PCI_DSS"]


