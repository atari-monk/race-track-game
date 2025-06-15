from dataclasses import dataclass

@dataclass
class CarState:
    center_x: float = 100.0
    center_y: float = 100.0
    heading: float = 0.0
    steer_angle: float = 0.0
    speed: float = 0.0
    acceleration: float = 0.0
    steer_input: float = 0.0
    accel_input: float = 0.0