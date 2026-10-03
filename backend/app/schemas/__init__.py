from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from app.models import Priority, RequestStatus, Role
class ORM(BaseModel): model_config=ConfigDict(from_attributes=True)
class Register(BaseModel): name: str=Field(min_length=2,max_length=120); email: EmailStr; password: str=Field(min_length=8,max_length=128)
class Login(BaseModel): email: EmailStr; password: str
class Token(BaseModel): access_token: str; token_type: str="bearer"
class UserOut(ORM): id:int; name:str; email:EmailStr; role:Role; created_at:datetime
class UserUpdate(BaseModel): name:str=Field(min_length=2,max_length=120)
class ProgramIn(BaseModel): title:str=Field(min_length=2,max_length=160); description:str; host:str; category:str; image_url:str|None=None; duration_minutes:int=Field(gt=0,le=720)
class ProgramOut(ProgramIn,ORM): id:int; created_at:datetime
class ScheduleIn(BaseModel): program_id:int; day_of_week:int=Field(ge=0,le=6); start_time:str=Field(pattern=r"^([01]\\d|2[0-3]):[0-5]\\d$"); end_time:str=Field(pattern=r"^([01]\\d|2[0-3]):[0-5]\\d$")
class ScheduleOut(ScheduleIn,ORM): id:int
class AnnouncementIn(BaseModel): title:str=Field(min_length=2,max_length=200); description:str; priority:Priority=Priority.NORMAL; image_url:str|None=None; published:bool=True
class AnnouncementOut(AnnouncementIn,ORM): id:int; created_at:datetime
class RequestIn(BaseModel): song_title:str=Field(min_length=1,max_length=200); artist:str=Field(min_length=1,max_length=200); dedication:str|None=Field(default=None,max_length=1000); requester_name:str=Field(min_length=1,max_length=120)
class RequestOut(RequestIn,ORM): id:int; status:RequestStatus; requester_id:int; created_at:datetime
class RadioOut(BaseModel): is_live:bool; stream_url:str; listeners:int; song_title:str; artist:str; artwork_url:str|None=None; program:str|None=None; host:str|None=None
