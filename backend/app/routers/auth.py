from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.core.security import create_access_token, get_current_user, hash_password, verify_password
from app.database.database import get_db
from app.models import User
from app.schemas import Login, Register, Token, UserOut
router=APIRouter(prefix="/api/auth", tags=["Authentication"])
@router.post("/register",response_model=Token,status_code=status.HTTP_201_CREATED)
def register(payload:Register,db:Annotated[Session,Depends(get_db)]):
    if db.scalar(select(User).where(User.email==payload.email.lower())): raise HTTPException(409,"An account with this email already exists")
    user=User(name=payload.name,email=payload.email.lower(),password_hash=hash_password(payload.password)); db.add(user); db.commit(); db.refresh(user); return Token(access_token=create_access_token(str(user.id)))
@router.post("/login",response_model=Token)
def login(payload:Login,db:Annotated[Session,Depends(get_db)]):
    user=db.scalar(select(User).where(User.email==payload.email.lower()))
    if not user or not verify_password(payload.password,user.password_hash): raise HTTPException(status_code=401,detail="Incorrect email or password")
    return Token(access_token=create_access_token(str(user.id)))
@router.get("/me",response_model=UserOut)
def me(user:Annotated[User,Depends(get_current_user)]): return user
