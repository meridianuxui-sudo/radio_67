from fastapi import APIRouter
from app.services.radio_service import RadioService
from app.schemas import RadioOut
router=APIRouter(prefix="/api/radio",tags=["Radio"])
@router.get("/status",response_model=RadioOut)
async def status(): return await RadioService().status()
@router.get("/now-playing",response_model=RadioOut)
async def now_playing(): return await RadioService().status()
@router.get("/stream")
async def stream():
    radio=await RadioService().status(); return {"stream_url":radio["stream_url"],"delivery":"direct-from-icecast-or-azuracast"}
@router.get("/listeners")
async def listeners(): return {"listeners":(await RadioService().status())["listeners"]}
