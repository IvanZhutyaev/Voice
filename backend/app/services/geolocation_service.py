from typing import Optional, Dict
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from app.core.config import settings


class GeolocationService:
    """Сервис для работы с геолокацией"""
    
    def __init__(self):
        self.geolocator = Nominatim(user_agent="glas_app")
    
    async def get_address_from_coordinates(
        self,
        latitude: float,
        longitude: float
    ) -> Optional[str]:
        """Получение адреса по координатам"""
        try:
            location = self.geolocator.reverse(
                f"{latitude}, {longitude}",
                language="ru"
            )
            return location.address if location else None
        except Exception:
            return None
    
    async def get_coordinates_from_address(
        self,
        address: str
    ) -> Optional[Dict[str, float]]:
        """Получение координат по адресу"""
        try:
            location = self.geolocator.geocode(address)
            if location:
                return {
                    "latitude": location.latitude,
                    "longitude": location.longitude
                }
            return None
        except Exception:
            return None
    
    async def get_district(
        self,
        latitude: float,
        longitude: float
    ) -> Optional[str]:
        """Определение района по координатам"""
        try:
            location = self.geolocator.reverse(
                f"{latitude}, {longitude}",
                language="ru"
            )
            if location:
                address = location.raw.get("address", {})
                # Попытка найти район в разных полях
                district = (
                    address.get("suburb") or
                    address.get("city_district") or
                    address.get("district") or
                    address.get("neighbourhood")
                )
                return district
            return None
        except Exception:
            return None
    
    def calculate_distance(
        self,
        lat1: float,
        lon1: float,
        lat2: float,
        lon2: float
    ) -> float:
        """Расчет расстояния между двумя точками в километрах"""
        return geodesic((lat1, lon1), (lat2, lon2)).kilometers

