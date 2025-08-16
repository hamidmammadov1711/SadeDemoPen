from fastapi import APIRouter
from backend.services.report_gen import generate_report

router = APIRouter()

@router.post("/generate-report")
def generate(scan_result: dict):
    report = generate_report(scan_result)
    return report
