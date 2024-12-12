from typing import Tuple
from geopy.distance import geodesic

class DistanceCalculatorService:
    def calculate_distance(
        self,
        source: Tuple[float, float],
        destination: Tuple[float, float]
    ) -> float:
        """
        Calculate the distance between two points using their coordinates.
        Returns distance in kilometers.
        """
        return round(geodesic(source, destination).kilometers, 2)