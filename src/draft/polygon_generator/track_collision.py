from typing import List, Tuple
import math
import arcade
from src.draft.polygon_generator.track_data import TrackData
from src.draft.polygon_generator.track_generator import TrackGenerator

class TrackCollision:
    def __init__(self, track_data: TrackData):
        self.track_data = track_data

    def _point_to_polygon_distance(self, x: float, y: float, polygon: List[Tuple[float, float]]) -> float:
        min_distance = float('inf')
        inside = False
        n = len(polygon)

        for i in range(n):
            j = (i + 1) % n
            xi, yi = polygon[i]
            xj, yj = polygon[j]

            # Calculate distance to segment
            segment_length = (xj - xi)**2 + (yj - yi)**2
            if segment_length == 0:
                distance = math.sqrt((x - xi)**2 + (y - yi)**2)
            else:
                t = max(0, min(1, ((x - xi) * (xj - xi) + (y - yi) * (yj - yi)) / segment_length))
                closest_x = xi + t * (xj - xi)
                closest_y = yi + t * (yj - yi)
                distance = math.sqrt((x - closest_x)**2 + (y - closest_y)**2)

            # Determine if point is inside the polygon
            if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi):
                inside = not inside

            if distance < min_distance:
                min_distance = distance

        return min_distance if inside else -min_distance

    def is_outside_track(self, x: float, y: float) -> bool:
        if not self.track_data.outer_points or not self.track_data.inner_points:
            return True

        outer_dist = self._point_to_polygon_distance(x, y, self.track_data.outer_points)
        inner_dist = self._point_to_polygon_distance(x, y, self.track_data.inner_points)

        return outer_dist < 0 or inner_dist > 0

    def apply_penalty(self, car: arcade.Sprite) -> None:
        if self.is_outside_track(car.center_x, car.center_y):
            car.change_x *= TrackGenerator.SLOW_FACTOR
            car.change_y *= TrackGenerator.SLOW_FACTOR
