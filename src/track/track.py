from typing import Final
import arcade
from src.car.car import Car
import math

class Track:
    SLOW_FACTOR: Final[float] = 0.0
    ROAD_WIDTH: Final[float] = 150.0
    RESET_DELAY: Final[float] = 3.0

    def __init__(self) -> None:
        self._center_x: float = 0.0
        self._center_y: float = 0.0
        self._outer_radius_x: float = 0.0
        self._outer_radius_y: float = 0.0
        self._inner_radius_x: float = 0.0
        self._inner_radius_y: float = 0.0
        self._width: int = 0
        self._height: int = 0
        self._out_of_bounds: bool = False
        self._reset_timer: float = 0.0
        self._reset_position: tuple[float, float] = (0.0, 0.0)
        self._reset_heading: float = 0.0

    def resize(self, width: int, height: int) -> None:
        self._width = width
        self._height = height
        self._center_x = width / 2
        self._center_y = height / 2
        self._outer_radius_x = width * 0.5
        self._outer_radius_y = height * 0.5
        self._inner_radius_x = self._outer_radius_x - self.ROAD_WIDTH
        self._inner_radius_y = self._outer_radius_y - self.ROAD_WIDTH

    def draw(self) -> None:
        arcade.draw_ellipse_filled(
            self._center_x,
            self._center_y,
            self._outer_radius_x * 2,
            self._outer_radius_y * 2,
            arcade.color.DARK_SLATE_GRAY
        )
        arcade.draw_ellipse_filled(
            self._center_x,
            self._center_y,
            self._inner_radius_x * 2,
            self._inner_radius_y * 2,
            arcade.color.BLACK
        )
        if self._out_of_bounds:
            countdown = max(0, round(self.RESET_DELAY - self._reset_timer))
            arcade.draw_text(
                f"RESETTING IN {countdown}",
                self._center_x,
                self._center_y,
                arcade.color.RED,
                font_size=48,
                anchor_x="center",
                anchor_y="center",
                bold=True
            )

    def is_outside_track(self, x: float, y: float) -> bool:
        dx = x - self._center_x
        dy = y - self._center_y
        outer = (dx / self._outer_radius_x) ** 2 + (dy / self._outer_radius_y) ** 2
        inner = (dx / self._inner_radius_x) ** 2 + (dy / self._inner_radius_y) ** 2
        return outer > 1.0 or inner < 1.0

    def _compute_reset_position(self, x: float, y: float) -> tuple[float, float, float]:
        dx = x - self._center_x
        dy = y - self._center_y
        angle = math.atan2(dy / self._outer_radius_y, dx / self._outer_radius_x)
        r_x = (self._inner_radius_x + self._outer_radius_x) / 2
        r_y = (self._inner_radius_y + self._outer_radius_y) / 2
        reset_x = self._center_x + r_x * math.cos(angle)
        reset_y = self._center_y + r_y * math.sin(angle)
        heading = self.compute_heading_clockwise(reset_x, reset_y)
        return reset_x, reset_y, heading


    def apply_penalty(self, car: Car, delta_time: float) -> None:
        outside = self.is_outside_track(car.state.center_x, car.state.center_y)
        self._out_of_bounds = outside
        if outside:
            car.state.speed = 0.0
            car.state.acceleration = 0.0
            self._reset_timer += delta_time
            if self._reset_timer == delta_time:
                x, y, heading = self._compute_reset_position(car.state.center_x, car.state.center_y)
                self._reset_position = (x, y)
                self._reset_heading = heading
            if self._reset_timer >= self.RESET_DELAY:
                car.state.center_x = self._reset_position[0]
                car.state.center_y = self._reset_position[1]
                car.state.heading = self._reset_heading
                car.state.speed = 0.0
                car.state.acceleration = 0.0
                self._reset_timer = 0.0
                self._out_of_bounds = False
        else:
            self._reset_timer = 0.0

    def compute_heading_clockwise(self, x: float, y: float) -> float:
        dx = x - self._center_x
        dy = y - self._center_y
        angle = math.atan2(dy / self._outer_radius_y, dx / self._outer_radius_x)
        return angle - math.pi / 2