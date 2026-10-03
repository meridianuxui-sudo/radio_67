from typing import Annotated, TypeVar
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.security import get_current_user, require_roles
from app.database.database import get_db
from app.models import Announcement, Program, Role, Schedule, User
from app.schemas import AnnouncementIn,AnnouncementOut,ProgramIn,ProgramOut,ScheduleIn,ScheduleOut
admin=Depends(require_roles(Role.ADMIN,Role.STAFF))
programs=APIRouter(prefix="/api/programs",tags=["Programs"]); schedules=APIRouter(prefix="/api/schedule",tags=["Schedule"]); announcements=APIRouter(prefix="/api/announcements",tags=["Announcements"])
def entity(db,model,id):
    item=db.get(model,id)
    if not item: raise HTTPException(404,"Resource not found")
    return item
@programs.get("",response_model=list[ProgramOut])
def list_programs(db:Annotated[Session,Depends(get_db)]): return db.scalars(select(Program).order_by(Program.title)).all()
@programs.get("/{id}",response_model=ProgramOut)
def get_program(id:int,db:Annotated[Session,Depends(get_db)]): return entity(db,Program,id)
@programs.post("",response_model=ProgramOut,status_code=201,dependencies=[admin])
def create_program(payload:ProgramIn,db:Annotated[Session,Depends(get_db)]): item=Program(**payload.model_dump()); db.add(item); db.commit(); db.refresh(item); return item
@programs.put("/{id}",response_model=ProgramOut,dependencies=[admin])
def update_program(id:int,payload:ProgramIn,db:Annotated[Session,Depends(get_db)]): item=entity(db,Program,id); [setattr(item,k,v) for k,v in payload.model_dump().items()]; db.commit(); db.refresh(item); return item
@programs.delete("/{id}",status_code=204,dependencies=[admin])
def delete_program(id:int,db:Annotated[Session,Depends(get_db)]): db.delete(entity(db,Program,id)); db.commit()
@schedules.get("",response_model=list[ScheduleOut])
def list_schedule(day:int|None=None,db:Session=Depends(get_db)):
    q=select(Schedule).order_by(Schedule.day_of_week,Schedule.start_time); return db.scalars(q.where(Schedule.day_of_week==day) if day is not None else q).all()
@schedules.post("",response_model=ScheduleOut,status_code=201,dependencies=[admin])
def create_schedule(payload:ScheduleIn,db:Annotated[Session,Depends(get_db)]): entity(db,Program,payload.program_id); item=Schedule(**payload.model_dump()); db.add(item); db.commit(); db.refresh(item); return item
@schedules.put("/{id}",response_model=ScheduleOut,dependencies=[admin])
def update_schedule(id:int,payload:ScheduleIn,db:Annotated[Session,Depends(get_db)]): entity(db,Program,payload.program_id); item=entity(db,Schedule,id); [setattr(item,k,v) for k,v in payload.model_dump().items()]; db.commit(); db.refresh(item); return item
@schedules.delete("/{id}",status_code=204,dependencies=[admin])
def delete_schedule(id:int,db:Annotated[Session,Depends(get_db)]): db.delete(entity(db,Schedule,id)); db.commit()
@announcements.get("",response_model=list[AnnouncementOut])
def list_announcements(db:Annotated[Session,Depends(get_db)]): return db.scalars(select(Announcement).where(Announcement.published==True).order_by(Announcement.created_at.desc())).all()
@announcements.get("/{id}",response_model=AnnouncementOut)
def get_announcement(id:int,db:Annotated[Session,Depends(get_db)]): return entity(db,Announcement,id)
@announcements.post("",response_model=AnnouncementOut,status_code=201,dependencies=[admin])
def create_announcement(payload:AnnouncementIn,db:Annotated[Session,Depends(get_db)]): item=Announcement(**payload.model_dump()); db.add(item); db.commit(); db.refresh(item); return item
@announcements.put("/{id}",response_model=AnnouncementOut,dependencies=[admin])
def update_announcement(id:int,payload:AnnouncementIn,db:Annotated[Session,Depends(get_db)]): item=entity(db,Announcement,id); [setattr(item,k,v) for k,v in payload.model_dump().items()]; db.commit(); db.refresh(item); return item
@announcements.delete("/{id}",status_code=204,dependencies=[admin])
def delete_announcement(id:int,db:Annotated[Session,Depends(get_db)]): db.delete(entity(db,Announcement,id)); db.commit()
