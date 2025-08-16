from fastapi import APIRouter, HTTPException, Depends
from backend.db import USERS, WORKSPACES, PACKAGES, SUBSCRIPTIONS, NOTIFICATIONS
from backend.models_user import User, Workspace, Package, Subscription, Notification
from datetime import datetime, timedelta

router = APIRouter()

@router.post("/register")
def register(user: User):
    if any(u.email == user.email for u in USERS):
        raise HTTPException(status_code=400, detail="Email artıq qeydiyyatda var")
    user.id = len(USERS) + 1
    user.created_at = datetime.now()
    USERS.append(user)
    WORKSPACES.append(Workspace(id=user.id, user_id=user.id, name=f"Workspace_{user.username}", created_at=datetime.now()))
    return {"message": "Qeydiyyat uğurla tamamlandı", "user_id": user.id}

@router.post("/login")
def login(email: str, password: str):
    user = next((u for u in USERS if u.email == email and u.password == password), None)
    if not user:
        raise HTTPException(status_code=401, detail="Email və ya şifrə yanlışdır")
    return {"message": "Login uğurlu", "user_id": user.id}

@router.get("/workspace/{user_id}")
def get_workspace(user_id: int):
    ws = next((w for w in WORKSPACES if w.user_id == user_id), None)
    if not ws:
        raise HTTPException(status_code=404, detail="Otaq tapılmadı")
    return ws

@router.get("/packages")
def get_packages():
    return PACKAGES

@router.post("/subscribe")
def subscribe(user_id: int, package_id: int):
    sub = next((s for s in SUBSCRIPTIONS if s.user_id == user_id), None)
    pkg = next((p for p in PACKAGES if p.id == package_id), None)
    if not pkg:
        raise HTTPException(status_code=404, detail="Paket tapılmadı")
    end_date = datetime.now() + timedelta(days=pkg.duration_days)
    if sub:
        sub.package_id = package_id
        sub.start_date = datetime.now()
        sub.end_date = end_date
        sub.is_active = True
    else:
        SUBSCRIPTIONS.append(Subscription(id=len(SUBSCRIPTIONS)+1, user_id=user_id, package_id=package_id, start_date=datetime.now(), end_date=end_date, is_active=True))
    return {"message": "Paket aktivləşdirildi", "package": pkg.name}

@router.get("/subscription/{user_id}")
def get_subscription(user_id: int):
    sub = next((s for s in SUBSCRIPTIONS if s.user_id == user_id), None)
    if not sub:
        raise HTTPException(status_code=404, detail="Abunəlik tapılmadı")
    pkg = next((p for p in PACKAGES if p.id == sub.package_id), None)
    return {"package": pkg.name, "start_date": sub.start_date, "end_date": sub.end_date, "is_active": sub.is_active}

@router.get("/notifications/{user_id}")
def get_notifications(user_id: int):
    return [n for n in NOTIFICATIONS if n.user_id == user_id]
