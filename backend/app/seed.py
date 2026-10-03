"""Development-only sample content. Run: python -m app.seed."""
from app.core.security import hash_password
from app.database.database import Base,SessionLocal,engine
from app.models import Announcement,Priority,Program,Role,Schedule,SongRequest,User
def run():
 Base.metadata.create_all(engine); db=SessionLocal()
 try:
  if db.query(User).first(): print("Seed skipped: database already contains data"); return
  admin=User(name="Development Admin",email="admin@meradion.test",password_hash=hash_password("ChangeMe123!"),role=Role.ADMIN); dj=User(name="Ari DJ",email="dj@meradion.test",password_hash=hash_password("ChangeMe123!"),role=Role.DJ); student=User(name="Campus Student",email="student@meradion.test",password_hash=hash_password("ChangeMe123!"),role=Role.STUDENT); db.add_all([admin,dj,student]); db.flush()
  morning=Program(title="Morning Voice",description="A bright start with campus news and music.",host="Ari DJ",category="Talk & Music",duration_minutes=120); connect=Program(title="Campus Connect",description="Student stories and community voices.",host="Leah Stone",category="Campus",duration_minutes=120); db.add_all([morning,connect]); db.flush(); db.add_all([Schedule(program_id=morning.id,day_of_week=0,start_time="08:00",end_time="10:00"),Schedule(program_id=connect.id,day_of_week=0,start_time="10:00",end_time="12:00"),Announcement(title="Annual Day",description="Save the date for an evening of performances and celebration.",priority=Priority.HIGH),SongRequest(song_title="Golden",artist="Campus Ensemble",requester_name="Campus Student",requester_id=student.id)]); db.commit(); print("Seeded development users; all use ChangeMe123! (development only).")
 finally: db.close()
if __name__=="__main__": run()
