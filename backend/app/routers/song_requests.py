from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.security import get_current_user,require_roles
from app.database.database import get_db
from app.models import RequestStatus,Role,SongRequest,User
from app.schemas import RequestIn,RequestOut
router=APIRouter(prefix="/api/song-requests",tags=["Song requests"])
@router.post("",response_model=RequestOut,status_code=201)
def create(payload:RequestIn,user:Annotated[User,Depends(get_current_user)],db:Annotated[Session,Depends(get_db)]): item=SongRequest(**payload.model_dump(),requester_id=user.id); db.add(item); db.commit(); db.refresh(item); return item
@router.get("",response_model=list[RequestOut])
def list_requests(user:Annotated[User,Depends(get_current_user)],db:Annotated[Session,Depends(get_db)]): return db.scalars(select(SongRequest).order_by(SongRequest.created_at.desc()) if user.role in {Role.ADMIN,Role.DJ,Role.STAFF} else select(SongRequest).where(SongRequest.requester_id==user.id).order_by(SongRequest.created_at.desc())).all()
@router.get("/{id}",response_model=RequestOut)
def get_request(id:int,user:Annotated[User,Depends(get_current_user)],db:Annotated[Session,Depends(get_db)]):
    item=db.get(SongRequest,id)
    if not item: raise HTTPException(404,"Song request not found")
    if item.requester_id!=user.id and user.role not in {Role.ADMIN,Role.DJ,Role.STAFF}: raise HTTPException(403,"Insufficient permissions")
    return item
def transition(id:int,target:RequestStatus,db:Session):
    item=db.get(SongRequest,id)
    if not item: raise HTTPException(404,"Song request not found")
    item.status=target; db.commit(); db.refresh(item); return item
@router.put("/{id}/approve",response_model=RequestOut,dependencies=[Depends(require_roles(Role.ADMIN,Role.DJ,Role.STAFF))])
def approve(id:int,db:Annotated[Session,Depends(get_db)]): return transition(id,RequestStatus.APPROVED,db)
@router.put("/{id}/reject",response_model=RequestOut,dependencies=[Depends(require_roles(Role.ADMIN,Role.DJ,Role.STAFF))])
def reject(id:int,db:Annotated[Session,Depends(get_db)]): return transition(id,RequestStatus.REJECTED,db)
