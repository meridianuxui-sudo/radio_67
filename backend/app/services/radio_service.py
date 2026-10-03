from app.core.config import get_settings
from app.services.azuracast_service import AzuraCastService
class RadioService:
    async def status(self):
        s=get_settings(); payload=await AzuraCastService().now_playing()
        if not payload: return {"is_live":False,"stream_url":s.radio_stream_url,"listeners":0,"song_title":"Campus radio is standing by","artist":"MERADIO'N","artwork_url":None,"program":None,"host":None}
        song=payload.get("now_playing",{}).get("song",{}); live=payload.get("live",{}); station=payload.get("station",{})
        return {"is_live":bool(live.get("is_live")),"stream_url":s.radio_stream_url or station.get("listen_url", ""),"listeners":payload.get("listeners",{}).get("current",0),"song_title":song.get("title", "Unknown title"),"artist":song.get("artist", "Unknown artist"),"artwork_url":song.get("art"),"program":live.get("streamer_name"),"host":live.get("streamer_name")}
