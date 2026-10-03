import os
os.environ["DATABASE_URL"]="sqlite:///./test_meradion.sqlite3"
from fastapi.testclient import TestClient
from app.database.database import Base,engine
from app.main import app
Base.metadata.drop_all(engine); Base.metadata.create_all(engine)
client=TestClient(app)
def auth(role_email="student@example.com"):
 response=client.post("/api/auth/register",json={"name":"Test Student","email":role_email,"password":"Password123!"}); return {"Authorization":f"Bearer {response.json()['access_token']}"}
def test_health_and_registration():
 assert client.get("/api/health").json()=={"status":"healthy"}; headers=auth(); assert client.get("/api/auth/me",headers=headers).status_code==200
def test_song_request_is_private():
 headers=auth("requests@example.com"); response=client.post("/api/song-requests",headers=headers,json={"song_title":"Song","artist":"Artist","requester_name":"Tester"}); assert response.status_code==201; assert response.json()["status"]=="PENDING"
def test_program_management_requires_admin():
 headers=auth("permissions@example.com"); response=client.post("/api/programs",headers=headers,json={"title":"News","description":"Daily","host":"DJ","category":"Talk","duration_minutes":30}); assert response.status_code==403
