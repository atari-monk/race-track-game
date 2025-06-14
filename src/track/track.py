# src/track/track.py
from typing import Final
import arcade

class Track:
    SLOW_FACTOR: Final[float] = 0.2

    def __init__(self) -> None:
        self._center_x: float = 0.0
        self._center_y: float = 0.0
        self._outer_radius_x: float = 0.0
        self._outer_radius_y: float = 0.0
        self._inner_radius_x: float = 0.0
        self._inner_radius_y: float = 0.0
        self._width: int = 0
        self._height: int = 0

    def resize(self, width: int, height: int) -> None:
        self._width = width
        self._height = height
        self._center_x = width / 2
        self._center_y = height / 2
        self._outer_radius_x = width * 0.45
        self._outer_radius_y = height * 0.35
        self._inner_radius_x = width * 0.25
        self._inner_radius_y = height * 0.15

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

    def is_outside_track(self, x: float, y: float) -> bool:
        dx = x - self._center_x
        dy = y - self._center_y
        outer = (dx / self._outer_radius_x) ** 2 + (dy / self._outer_radius_y) ** 2
        inner = (dx / self._inner_radius_x) ** 2 + (dy / self._inner_radius_y) ** 2
        return outer > 1.0 or inner < 1.0

    def apply_penalty(self, car: arcade.Sprite) -> None:
        if self.is_outside_track(car.center_x, car.center_y):
            car.change_x *= self.SLOW_FACTOR
            car.change_y *= self.SLOW_FACTOR

