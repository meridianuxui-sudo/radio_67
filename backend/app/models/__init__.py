from datetime import datetime
from enum import Enum
from sqlalchemy import Boolean, DateTime, Enum as SqlEnum, ForeignKey, Index, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.database import Base

class Role(str, Enum): ADMIN="ADMIN"; DJ="DJ"; STAFF="STAFF"; STUDENT="STUDENT"
class RequestStatus(str, Enum): PENDING="PENDING"; APPROVED="APPROVED"; REJECTED="REJECTED"; COMPLETED="COMPLETED"
class Priority(str, Enum): LOW="LOW"; NORMAL="NORMAL"; HIGH="HIGH"
class Timestamped:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
class User(Timestamped, Base):
    __tablename__="users"; id: Mapped[int]=mapped_column(primary_key=True); name: Mapped[str]=mapped_column(String(120)); email: Mapped[str]=mapped_column(String(255), unique=True, index=True); password_hash: Mapped[str]=mapped_column(String(255)); role: Mapped[Role]=mapped_column(SqlEnum(Role), default=Role.STUDENT); requests=relationship("SongRequest", back_populates="requester"); favorites=relationship("Favorite", back_populates="user", cascade="all, delete-orphan")
class Program(Timestamped, Base):
    __tablename__="programs"; id: Mapped[int]=mapped_column(primary_key=True); title: Mapped[str]=mapped_column(String(160), index=True); description: Mapped[str]=mapped_column(Text); host: Mapped[str]=mapped_column(String(120)); category: Mapped[str]=mapped_column(String(80)); image_url: Mapped[str|None]=mapped_column(String(500)); duration_minutes: Mapped[int]=mapped_column(Integer); schedules=relationship("Schedule", back_populates="program", cascade="all, delete-orphan")
class Schedule(Timestamped, Base):
    __tablename__="schedules"; id: Mapped[int]=mapped_column(primary_key=True); program_id: Mapped[int]=mapped_column(ForeignKey("programs.id"), index=True); day_of_week: Mapped[int]=mapped_column(Integer); start_time: Mapped[str]=mapped_column(String(5)); end_time: Mapped[str]=mapped_column(String(5)); program=relationship("Program", back_populates="schedules")
class Announcement(Timestamped, Base):
    __tablename__="announcements"; id: Mapped[int]=mapped_column(primary_key=True); title: Mapped[str]=mapped_column(String(200)); description: Mapped[str]=mapped_column(Text); priority: Mapped[Priority]=mapped_column(SqlEnum(Priority), default=Priority.NORMAL); image_url: Mapped[str|None]=mapped_column(String(500)); published: Mapped[bool]=mapped_column(Boolean, default=True, index=True)
class SongRequest(Timestamped, Base):
    __tablename__="song_requests"; id: Mapped[int]=mapped_column(primary_key=True); song_title: Mapped[str]=mapped_column(String(200)); artist: Mapped[str]=mapped_column(String(200)); dedication: Mapped[str|None]=mapped_column(Text); requester_name: Mapped[str]=mapped_column(String(120)); status: Mapped[RequestStatus]=mapped_column(SqlEnum(RequestStatus), default=RequestStatus.PENDING, index=True); requester_id: Mapped[int]=mapped_column(ForeignKey("users.id"), index=True); requester=relationship("User", back_populates="requests")
class Favorite(Base):
    __tablename__="favorites"; user_id: Mapped[int]=mapped_column(ForeignKey("users.id"), primary_key=True); program_id: Mapped[int]=mapped_column(ForeignKey("programs.id"), primary_key=True); created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), server_default=func.now()); user=relationship("User", back_populates="favorites")
class RadioMetadata(Base):
    __tablename__="radio_metadata"; id: Mapped[int]=mapped_column(primary_key=True); song_title: Mapped[str]=mapped_column(String(200)); artist: Mapped[str]=mapped_column(String(200)); artwork_url: Mapped[str|None]=mapped_column(String(500)); listeners: Mapped[int]=mapped_column(Integer, default=0); updated_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
Index("ix_schedule_day_start", Schedule.day_of_week, Schedule.start_time)
