import httpx
from app.core.config import get_settings
class AzuraCastService:
    async def now_playing(self) -> dict | None:
        s=get_settings()
        if not s.azuracast_base_url: return None
        headers={"X-API-Key": s.azuracast_api_key} if s.azuracast_api_key else {}
        async with httpx.AsyncClient(timeout=8) as client:
            response=await client.get(f"{s.azuracast_base_url.rstrip('/')}/api/nowplaying/{s.azuracast_station_id}", headers=headers); response.raise_for_status(); return response.json()
