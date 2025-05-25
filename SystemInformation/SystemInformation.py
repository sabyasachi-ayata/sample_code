from fastapi import FastAPI, Path
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

class LocationInfo(BaseModel):
    latitude: float
    longtitude: float

class AssetInfo(BaseModel):
    wellName: str
    wellId: int
    status: str
    timeOffset: int
    refId: int
    artificialLiftType: int
    firstProductionDate: str  # ISO format date string
    locationInfo: LocationInfo

class AssetResponse(BaseModel):
    assetInfo: AssetInfo

@app.get("/data/assets/{asset_id}", response_model=AssetResponse)
async def get_asset_info(asset_id: int = Path(..., description="ID of the asset")):
    # For demonstration, returning static data. Replace with DB/query logic as needed.
    # Use async def in FastAPI to enable asynchronous, non-blocking operations for better performance and scalability— especially when your endpoint makes I/O calls (like database or network requests). If your endpoint is simple and synchronous, async is optional.
    example_response = {
        "assetInfo": {
            "wellName": "XXX",
            "wellId": 234,
            "status": "online",
            "timeOffset": 4,
            "refId": 2,
            "artificialLiftType": 5,
            "firstProductionDate": "2025-04-01",
            "locationInfo": {
                "latitude": 22.15,
                "longtitude": -23.02
            }
        }
    }
    return example_response