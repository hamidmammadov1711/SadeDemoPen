from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base
import datetime

class Lab(Base):
    __tablename__ = "labs"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    is_active = Column(Boolean, default=True)
    challenges = relationship("Challenge", back_populates="lab")

class Challenge(Base):
    __tablename__ = "challenges"
    id = Column(Integer, primary_key=True, index=True)
    lab_id = Column(Integer, ForeignKey("labs.id"))
    title = Column(String)
    flag = Column(String)
    points = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    lab = relationship("Lab", back_populates="challenges")
    submissions = relationship("Submission", back_populates="challenge")

class Team(Base):
    __tablename__ = "teams"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    members = Column(String)  # JSON string veya virgülle ayrılmış
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    submissions = relationship("Submission", back_populates="team")

class Submission(Base):
    __tablename__ = "submissions"
    id = Column(Integer, primary_key=True, index=True)
    challenge_id = Column(Integer, ForeignKey("challenges.id"))
    team_id = Column(Integer, ForeignKey("teams.id"))
    submitted_flag = Column(String)
    is_correct = Column(Boolean, default=False)
    submitted_at = Column(DateTime, default=datetime.datetime.utcnow)
    challenge = relationship("Challenge", back_populates="submissions")
    team = relationship("Team", back_populates="submissions")

class Score(Base):
    __tablename__ = "scores"
    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"))
    total_points = Column(Integer)
    total_points: int
