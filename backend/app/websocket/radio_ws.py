import asyncio, json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.radio_service import RadioService
router=APIRouter()
@router.websocket("/ws/radio")
async def radio_socket(websocket: WebSocket):
    await websocket.accept(); last=None
    try:
        while True:
            status=await RadioService().status(); signature=(status["song_title"],status["artist"],status["listeners"])
            if signature != last: await websocket.send_text(json.dumps({"type":"NOW_PLAYING_CHANGED","data":status})); last=signature
            await asyncio.sleep(20)
    except WebSocketDisconnect: pass
