import httpx
import requests
from typing import Tuple, Optional
from fastapi import HTTPException
from pydantic import BaseModel

class GeocodingService(BaseModel):
    base_url: str = "https://nominatim.openstreetmap.org/search"
    headers: dict = {
        "User-Agent": "DistanceCalculator/1.0" 
    }

    async def get_coordinates(self, address: str) -> Optional[Tuple[float, float]]:
        """Get latitude and longitude for an address using Nominatim API."""
        params = {
            "q": address,
            "format": "geocodejson",
            "limit": 1
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    self.base_url,
                    params=params,
                    headers=self.headers
                )
                response.raise_for_status()
                
                results = response.json()
                if not results:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Address not found: {address}"
                    )
                    
                lat, lon = results["features"][0]["geometry"]["coordinates"]
                return float(lat), float(lon)
                
            except requests.RequestException as e:
                raise HTTPException(
                    status_code=503,
                    detail=f"Geocoding service unavailable: {str(e)}"
                )