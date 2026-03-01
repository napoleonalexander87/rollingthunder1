from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
import logging
from datetime import datetime

# Create router with NO automatic slash redirects
router = APIRouter()

# In-memory storage (IP → latest location)
latest_locations: dict[str, dict] = {}

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class LocationPayload(BaseModel):
    latitude: float
    longitude: float
    accuracy: Optional[float] = None
    timestamp: Optional[str] = None

@router.post("/send_location")
@router.post("/send_location/")
async def receive_location(payload: LocationPayload, request: Request):
    """
    Receives geolocation data from the client.
    Logs it and stores latest per IP.
    """
    client_ip = request.client.host
    data = payload.model_dump()

    # Add server info
    data["received_at"] = datetime.utcnow().isoformat()
    data["client_ip"] = client_ip

    latest_locations[client_ip] = data
    logger.info(f"Location received from {client_ip}: {data}")

    return {"status": "received"}

@router.get("/view_location")
async def view_latest_locations():
    """HTML view of latest locations"""
    if not latest_locations:
        return {"message": "No locations received yet."}

    html = "<h1>Latest Received Locations (Workshop Demo)</h1><ul>"
    for ip, loc in latest_locations.items():
        html += f"<li><strong>{ip}</strong>: Lat {loc['latitude']}, Lon {loc['longitude']}"
        if loc.get('accuracy'):
            html += f" (±{loc['accuracy']:.1f}m)"
        html += f" — {loc.get('received_at', '—')}</li>"
    html += "</ul>"
    html += '<p>Refresh page to update. <a href="/api/view_location/json">Raw JSON</a></p>'

    return HTMLResponse(content=html, status_code=200)

@router.get("/view_location/json")
async def view_latest_json():
    """Raw JSON endpoint"""
    return latest_locations
@router.get("/test")
async def test_route():
    return {"message": "Router is working"}