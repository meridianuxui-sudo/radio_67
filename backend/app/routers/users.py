from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.database.database import get_db
from app.models import User
from app.schemas import UserOut,UserUpdate
router=APIRouter(prefix="/api/users",tags=["Users"])
@router.get("/me",response_model=UserOut)
def me(user:Annotated[User,Depends(get_current_user)]): return user
@router.put("/me",response_model=UserOut)
def update(payload:UserUpdate,user:Annotated[User,Depends(get_current_user)],db:Annotated[Session,Depends(get_db)]): user.name=payload.name; db.commit(); db.refresh(user); return user
