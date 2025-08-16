from datetime import datetime, timedelta
from typing import List, Optional
from backend.models_user import User, Workspace, Package, Subscription, Notification

# Demo veri tabanı (memory)
USERS = []
WORKSPACES = []
PACKAGES = [
    Package(id=1, name="Free", features=["basic test"], test_limit=2, price=0, duration_days=0),
    Package(id=2, name="Basic", features=["server", "web", "app test"], test_limit=10, price=29, duration_days=30),
    Package(id=3, name="Pro", features=["server", "web", "app test", "AI", "API test"], test_limit=30, price=89, duration_days=30),
    Package(id=4, name="Enterprise", features=["all"], test_limit=100, price=199, duration_days=30)
]
SUBSCRIPTIONS = []
NOTIFICATIONS = []

# Demo user ekle
USERS.append(User(id=1, username="demo", email="demo@site.com", password="demo123", organization="DemoOrg", created_at=datetime.now(), is_active=True))
WORKSPACES.append(Workspace(id=1, user_id=1, name="Demo Workspace", created_at=datetime.now()))
SUBSCRIPTIONS.append(Subscription(id=1, user_id=1, package_id=2, start_date=datetime.now(), end_date=datetime.now()+timedelta(days=30), is_active=True, test_count=0))
