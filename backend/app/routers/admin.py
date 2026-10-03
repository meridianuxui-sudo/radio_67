from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.core.security import require_roles
from app.database.database import get_db
from app.models import Announcement, RequestStatus, Role, SongRequest, User
from app.services.radio_service import RadioService
router=APIRouter(prefix="/api/admin",tags=["Administration"],dependencies=[Depends(require_roles(Role.ADMIN))])
@router.get("/dashboard")
async def dashboard(db:Annotated[Session,Depends(get_db)]): return {"radio":await RadioService().status(),"users":db.scalar(select(func.count(User.id))),"pending_requests":db.scalar(select(func.count(SongRequest.id)).where(SongRequest.status==RequestStatus.PENDING)),"announcements":db.scalar(select(func.count(Announcement.id).where(Announcement.published==True)))}
@router.get("/listeners")
async def listeners(): return {"current":(await RadioService().status())["listeners"],"series":[]}
@router.get("/requests")
def requests(db:Annotated[Session,Depends(get_db)]): return db.scalars(select(SongRequest).order_by(SongRequest.created_at.desc())).all()
@router.get("/statistics")
def statistics(db:Annotated[Session,Depends(get_db)]): return {"requests_by_status":[{"status":s.value,"count":db.scalar(select(func.count(SongRequest.id)).where(SongRequest.status==s))} for s in RequestStatus]}
