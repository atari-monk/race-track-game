#from __future__ import annotations
from dataclasses import dataclass
import math

@dataclass
class CarSpecs:
    length: float = 60.0
    width: float = 30.0
    mass: float = 1000.0
    max_steer_angle: float = math.radians(45)
    max_steer_rate: float = math.radians(300)
    max_speed: float = 5200.0
    acceleration_force: float = 800000.0
    brake_force: float = 10000000.0
    drag_coeff: float = 1.2
    friction_limit: float = 24000.0
    dt: float = 1 / 60.0
    steer_response_curve: float = 0.5