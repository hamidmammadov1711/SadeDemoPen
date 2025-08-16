from fastapi import APIRouter, Request
from backend.utils.nmap_runner import run_nmap
from backend.utils.audit import log_request

router = APIRouter()

@router.post("/scan")
async def scan(request: Request, target: str):
    masked_target = target if not target.startswith("192.") else "PRIVATE_IP"
    log_request(request, action="nmap_scan", details={"target": masked_target})
    result = run_nmap(target)
    return {"result": result}
