# src/car/car.py
from typing import Final
import arcade

class Car(arcade.Sprite):
    SPEED: Final[float] = 5.0
    TEXTURE_SIZE: Final[int] = 40

    def __init__(self) -> None:
        super().__init__()
        self.color = arcade.color.RED
        self.width = self.TEXTURE_SIZE
        self.height = self.TEXTURE_SIZE
        self.center_x = 100
        self.center_y = 100
        self.change_x = 0
        self.change_y = 0

    def update(self) -> None:
        self.center_x += self.change_x
        self.center_y += self.change_y

    def draw(self) -> None:
        rect = arcade.XYWH(
            self.center_x, 
            self.center_y, 
            self.width, 
            self.height
        )
        arcade.draw_rect_filled(rect, self.color)

    def on_key_press(self, key: int) -> None:
        if key == arcade.key.UP:
            self.change_y = self.SPEED
        elif key == arcade.key.DOWN:
            self.change_y = -self.SPEED
        elif key == arcade.key.LEFT:
            self.change_x = -self.SPEED
        elif key == arcade.key.RIGHT:
            self.change_x = self.SPEED

    def on_key_release(self, key: int) -> None:
        if key in (arcade.key.UP, arcade.key.DOWN):
            self.change_y = 0
        elif key in (arcade.key.LEFT, arcade.key.RIGHT):
            self.change_x = 0
