# backend/main.py
from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

## verify_jwt fonksiyonu main.py içinde tanımlı, import gereksiz
from backend.api.routers import nmap_router, report_router
from backend.api_user import router as user_router
from backend.api_lab import router as lab_router


## Tek bir app ve middleware tanımı bırakıldı, tekrarlar kaldırıldı



## ...existing code...
# main.py
# API giriş noktası
# main.py
# API giriş nöqtəsi
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from backend.api.routers import nmap_router, report_router
from backend.models import TestRequest, TestResponse
from backend.services.nmap_runner import run_nmap
from backend.services.report_gen import generate_report
from backend.utils.logger import log_scan
from backend.services.audit import log_event
from backend.api_user import router as user_router
from backend.api_lab import router as lab_router
from backend.db import SUBSCRIPTIONS, PACKAGES, NOTIFICATIONS
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import os
from datetime import datetime, timedelta


limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
security = HTTPBearer()

def verify_jwt(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    # Basit JWT doğrulama (geliştirmek için gerçek anahtar ile kontrol eklenmeli)
    if token != os.getenv("API_JWT", "testtoken"):
        raise HTTPException(status_code=401, detail="Invalid token")
    return True


app.include_router(nmap_router)
app.include_router(report_router)
app.include_router(user_router)
app.include_router(lab_router)


@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(status_code=429, content={"error": "Çox tez-tez sorğu göndərildi"})



@app.post("/run-test", response_model=TestResponse)
@limiter.limit("5/minute")
def run_test(req: TestRequest, request: Request, authorized: bool = Depends(verify_jwt), user_id: int = 1, lang: str = "az"):
    # Demo: user_id=1
    # Paket limitini yoxla
    sub = next((s for s in SUBSCRIPTIONS if s.user_id == user_id), None)
    pkg = next((p for p in PACKAGES if p.id == sub.package_id), None) if sub else PACKAGES[0]
    # Paket bitmə tarixi
    if sub and sub.end_date:
        days_left = (sub.end_date - datetime.now()).days
        if days_left <= 7 and sub.is_active:
            NOTIFICATIONS.append({"user_id": user_id, "message": f"Paketin bitməsinə {days_left} gün qalıb", "sent_at": datetime.now(), "type": "warning"})
        if sub.end_date < datetime.now():
            sub.package_id = 1
            sub.start_date = datetime.now()
            sub.end_date = None
            sub.is_active = False
            pkg = PACKAGES[0]
            NOTIFICATIONS.append({"user_id": user_id, "message": "Paket bitdi, Free paket aktivləşdi", "sent_at": datetime.now(), "type": "info"})
    # Test limitini yoxla
    if sub and pkg and sub.test_count >= pkg.test_limit:
        error_msg = {
            "az": "Test limiti bitib",
            "en": "Test limit reached",
            "ru": "Лимит тестов исчерпан",
            "tr": "Test limiti doldu"
        }
        return JSONResponse(status_code=403, content={"error": error_msg.get(lang, error_msg["az"] )})
    try:
        result = run_nmap(req.target)
        log_scan(req.target, result["status"], str(result["details"]))
        log_event("run-test", {
            "ip": get_remote_address(request),
            "target": req.target,
            "status": result["status"]
        })
        if sub:
            sub.test_count = getattr(sub, "test_count", 0) + 1
        return result
    except Exception as e:
        log_event("error", {"target": req.target, "error": str(e)})
        error_msg = {
            "az": "Test zamanı xəta baş verdi",
            "en": "An error occurred during testing",
            "ru": "Ошибка во время теста",
            "tr": "Test sırasında hata oluştu"
        }
        return JSONResponse(status_code=500, content={"error": error_msg.get(lang, error_msg["az"] )})

# Yeni endpoint: Rapor oluşturma
@app.post("/report")
def create_report(req: TestRequest, authorized: bool = Depends(verify_jwt), lang: str = "az"):
    scan_result = run_nmap(req.target)
    report = generate_report(scan_result)
    log_event("report", {"target": req.target, "report": report})
    summary_trans = {
        "az": report["summary"],
        "en": f"{len(report['highlights'])} open ports detected. Risk score: {report['risk_score']}. Category: {report['category']}.",
        "ru": f"Обнаружено {len(report['highlights'])} открытых портов. Риск: {report['risk_score']}. Категория: {report['category']}.",
        "tr": f"{len(report['highlights'])} açık port tespit edildi. Risk skoru: {report['risk_score']}. Kategori: {report['category']}.",
    }
    report["summary"] = summary_trans.get(lang, report["summary"])
    return report

# Yeni endpoint: Logları çekme
@app.get("/logs")
def get_logs(authorized: bool = Depends(verify_jwt)):
    try:
        with open("audit.log", "r") as f:
            logs = f.readlines()
        return {"logs": [log.strip() for log in logs]}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# Yeni endpoint: Health check
@app.get("/health")
def health():
    return {"status": "ok"}

