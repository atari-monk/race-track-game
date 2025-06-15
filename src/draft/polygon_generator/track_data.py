from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class TrackData:
    control_points: List[Tuple[float, float]]
    spline_points: List[Tuple[float, float]]
    inner_points: List[Tuple[float, float]]
    outer_points: List[Tuple[float, float]]
    width: float
    height: float