from fastapi import APIRouter, HTTPException
from backend.db_lab import LABS, CHALLENGES, TEAMS, SUBMISSIONS, SCORES
from backend.models_lab import Lab, Challenge, Team, Submission, Score
from datetime import datetime

router = APIRouter()

@router.get("/labs")
def get_labs():
    return LABS

@router.get("/challenges/{lab_id}")
def get_challenges(lab_id: int):
    return [c for c in CHALLENGES if c.lab_id == lab_id and c.is_active]

@router.post("/submit-flag")
def submit_flag(team_id: int, challenge_id: int, submitted_flag: str):
    challenge = next((c for c in CHALLENGES if c.id == challenge_id), None)
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge tapılmadı")
    is_correct = submitted_flag.strip() == challenge.flag
    SUBMISSIONS.append(Submission(id=len(SUBMISSIONS)+1, team_id=team_id, challenge_id=challenge_id, submitted_flag=submitted_flag, is_correct=is_correct, submitted_at=datetime.now()))
    if is_correct:
        score = next((s for s in SCORES if s.team_id == team_id), None)
        if score:
            score.total_points += challenge.points
        else:
            SCORES.append(Score(team_id=team_id, total_points=challenge.points))
    return {"correct": is_correct, "points": challenge.points if is_correct else 0}

@router.get("/leaderboard")
def get_leaderboard():
    return sorted(SCORES, key=lambda s: s.total_points, reverse=True)
