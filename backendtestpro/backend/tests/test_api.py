

# test_api.py
# API testleri
import pytest
from backend.services.nmap_runner import run_nmap
from backend.services.report_gen import generate_report

def test_run_nmap_success():
	result = run_nmap("scanme.nmap.org")
	assert "status" in result
	assert "details" in result
	assert "target" in result

def test_generate_report_high_risk():
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
