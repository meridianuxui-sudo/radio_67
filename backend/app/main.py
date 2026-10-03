import logging
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import get_settings
from app.database.database import Base,engine
from app.routers import admin,auth,content,radio,song_requests,users
from app.websocket.radio_ws import router as ws_router
logging.basicConfig(level=logging.INFO,format="%(asctime)s %(levelname)s %(name)s %(message)s")
app=FastAPI(title="MERADIO'N API",version="1.0.0",description="Campus-radio business API. Audio streams directly from AzuraCast/Icecast.")
app.add_middleware(CORSMiddleware,allow_origins=get_settings().cors_origin_list,allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
@app.exception_handler(RequestValidationError)
async def validation_error(_:Request,exc:RequestValidationError): return JSONResponse(status_code=422,content={"error":{"code":"VALIDATION_ERROR","message":"Please review the submitted fields.","details":exc.errors()}})
@app.exception_handler(Exception)
async def unknown_error(_:Request,exc:Exception): logging.exception("Unhandled request error"); return JSONResponse(status_code=500,content={"error":{"code":"INTERNAL_ERROR","message":"An unexpected error occurred."}})
@app.get("/api/health",tags=["Health"])
def health(): return {"status":"healthy"}
app.include_router(auth.router); app.include_router(users.router); app.include_router(content.programs); app.include_router(content.schedules); app.include_router(content.announcements); app.include_router(song_requests.router); app.include_router(radio.router); app.include_router(admin.router); app.include_router(ws_router)
@app.on_event("startup")
def startup(): Base.metadata.create_all(bind=engine)
