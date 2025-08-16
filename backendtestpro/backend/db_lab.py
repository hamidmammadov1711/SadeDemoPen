from datetime import datetime
from backend.models_lab import Lab, Challenge, Team, Submission, Score

LABS = [
    Lab(id=1, name="Web Security Lab", description="Web tətbiqləri üçün təhlükəsizlik tapşırıqları", owner_id=1, created_at=datetime.now()),
    Lab(id=2, name="Network CTF", description="Şəbəkə və pentest üçün CTF tapşırıqları", owner_id=1, created_at=datetime.now())
]
CHALLENGES = [
    Challenge(id=1, lab_id=1, title="SQL Injection", description="Login formunda SQLi tapın", points=100, flag="flag{sql_injection_found}", is_active=True),
    Challenge(id=2, lab_id=1, title="XSS", description="Saytda XSS açığını tapın", points=80, flag="flag{xss_found}", is_active=True),
    Challenge(id=3, lab_id=2, title="Port Scan", description="Açıq portları tapın", points=50, flag="flag{open_ports}", is_active=True)
]
TEAMS = [
    Team(id=1, name="DemoTeam", members=[1], created_at=datetime.now())
]
SUBMISSIONS = []
SCORES = []
