import math
from typing import Tuple
import arcade
from src.car.car_specs import CarSpecs
from src.car.car_state import CarState

class CarRenderer:
    def __init__(self, specs: CarSpecs, state: CarState) -> None:
        self.specs = specs
        self.state = state

    def draw(self) -> None:
        corners = [
            (-self.specs.length/2, -self.specs.width/2),
            (self.specs.length/2, -self.specs.width/2),
            (self.specs.length/2, self.specs.width/2),
            (-self.specs.length/2, self.specs.width/2)
        ]

        rotated_corners: list[Tuple[float, float]] = []
        for x, y in corners:
            rx = x * math.cos(self.state.heading) - y * math.sin(self.state.heading)
            ry = x * math.sin(self.state.heading) + y * math.cos(self.state.heading)
            tx = self.state.center_x + rx
            ty = self.state.center_y + ry
            rotated_corners.append((tx, ty))

        arcade.draw_polygon_filled(rotated_corners, arcade.color.RED)

        front_x = self.state.center_x + (self.specs.length/2) * math.cos(self.state.heading)
        front_y = self.state.center_y + (self.specs.length/2) * math.sin(self.state.heading)
        arcade.draw_circle_filled(front_x, front_y, 4, arcade.color.YELLOW)