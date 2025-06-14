from typing import Final
import arcade

class Track:
    CENTER_X: Final[float] = 400
    CENTER_Y: Final[float] = 300
    OUTER_RADIUS_X: Final[float] = 300
    OUTER_RADIUS_Y: Final[float] = 200
    INNER_RADIUS_X: Final[float] = 200
    INNER_RADIUS_Y: Final[float] = 100
    SLOW_FACTOR: Final[float] = 0.2

    def draw(self) -> None:
        arcade.draw_ellipse_filled(
            self.CENTER_X,
            self.CENTER_Y,
            self.OUTER_RADIUS_X * 2,
            self.OUTER_RADIUS_Y * 2,
            arcade.color.DARK_SLATE_GRAY
        )
        arcade.draw_ellipse_filled(
            self.CENTER_X,
            self.CENTER_Y,
            self.INNER_RADIUS_X * 2,
            self.INNER_RADIUS_Y * 2,
            arcade.color.BLACK
        )

    def is_outside_track(self, x: float, y: float) -> bool:
        dx = x - self.CENTER_X
        dy = y - self.CENTER_Y
        outer = (dx / self.OUTER_RADIUS_X) ** 2 + (dy / self.OUTER_RADIUS_Y) ** 2
        inner = (dx / self.INNER_RADIUS_X) ** 2 + (dy / self.INNER_RADIUS_Y) ** 2
        return outer > 1.0 or inner < 1.0

    def apply_penalty(self, car: arcade.Sprite) -> None:
        if self.is_outside_track(car.center_x, car.center_y):
            car.change_x *= self.SLOW_FACTOR
            car.change_y *= self.SLOW_FACTOR

