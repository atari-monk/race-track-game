from typing import Final, List, Tuple
import math
from src.draft.polygon_generator.track_data import TrackData

class TrackGenerator:
    SLOW_FACTOR: Final[float] = 0.1
    TRACK_WIDTH: Final[float] = 0.1

    def __init__(self, width: int, height: int) -> None:
        self._width = width
        self._height = height
        self._track_data = self.generate_track()

    def _create_control_points(self) -> List[Tuple[float, float]]:
        return [
            (self._width*0.2, self._height*0.2),
            (self._width*0.5, self._height*0.1),
            (self._width*0.8, self._height*0.2),
            (self._width*0.9, self._height*0.5),
            (self._width*0.8, self._height*0.8),
            (self._width*0.5, self._height*0.9),
            (self._width*0.2, self._height*0.8),
            (self._width*0.1, self._height*0.5)
        ]

    def _catmull_rom_spline(self, p0: Tuple[float, float], p1: Tuple[float, float],
                          p2: Tuple[float, float], p3: Tuple[float, float],
                          num_points: int) -> List[Tuple[float, float]]:
        points = []
        for i in range(num_points):
            t = i / num_points
            t2 = t * t
            t3 = t2 * t

            x = 0.5 * ((2 * p1[0]) +
                      (-p0[0] + p2[0]) * t +
                      (2*p0[0] - 5*p1[0] + 4*p2[0] - p3[0]) * t2 +
                      (-p0[0] + 3*p1[0] - 3*p2[0] + p3[0]) * t3)

            y = 0.5 * ((2 * p1[1]) +
                      (-p0[1] + p2[1]) * t +
                      (2*p0[1] - 5*p1[1] + 4*p2[1] - p3[1]) * t2 +
                      (-p0[1] + 3*p1[1] - 3*p2[1] + p3[1]) * t3)

            points.append((x, y))
        return points

    def _generate_spline_points(self, control_points: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
        if len(control_points) < 4:
            return []

        spline_points = []
        n = len(control_points)

        for i in range(n):
            p0 = control_points[(i-1) % n]
            p1 = control_points[i % n]
            p2 = control_points[(i+1) % n]
            p3 = control_points[(i+2) % n]

            segment = self._catmull_rom_spline(p0, p1, p2, p3, 20)
            spline_points.extend(segment)

        return spline_points

    def _generate_boundary_points(self, spline_points: List[Tuple[float, float]]) -> Tuple[List[Tuple[float, float]], List[Tuple[float, float]]]:
        if not spline_points:
            return [], []

        inner_points = []
        outer_points = []
        track_width = min(self._width, self._height) * self.TRACK_WIDTH
        n = len(spline_points)

        for i in range(n):
            prev_point = spline_points[(i-1) % n]
            curr_point = spline_points[i]
            next_point = spline_points[(i+1) % n]

            dx1 = curr_point[0] - prev_point[0]
            dy1 = curr_point[1] - prev_point[1]
            dx2 = next_point[0] - curr_point[0]
            dy2 = next_point[1] - curr_point[1]

            dx = (dx1 + dx2) / 2
            dy = (dy1 + dy2) / 2

            length = math.sqrt(dx*dx + dy*dy)
            if length > 0:
                nx = -dy / length
                ny = dx / length

                inner_points.append((
                    curr_point[0] + nx * track_width,
                    curr_point[1] + ny * track_width
                ))
                outer_points.append((
                    curr_point[0] - nx * track_width,
                    curr_point[1] - ny * track_width
                ))

        return inner_points, outer_points

    def generate_track(self) -> TrackData:
        control_points = self._create_control_points()
        spline_points = self._generate_spline_points(control_points)
        inner_points, outer_points = self._generate_boundary_points(spline_points)

        return TrackData(
            control_points=control_points,
            spline_points=spline_points,
            inner_points=inner_points,
            outer_points=outer_points,
            width=self._width,
            height=self._height
        )

    @property
    def track_data(self) -> TrackData:
        return self._track_data