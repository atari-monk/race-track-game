import arcade
from src.car.car_state import CarState

class CarInput:
    def __init__(self, state: CarState) -> None:
        self.state = state

    def on_key_press(self, key: int) -> None:
        if key == arcade.key.UP:
            self.state.accel_input = 1.0
        elif key == arcade.key.DOWN:
            self.state.accel_input = -1.0
        elif key == arcade.key.LEFT:
            self.state.steer_input = 1.0
        elif key == arcade.key.RIGHT:
            self.state.steer_input = -1.0

    def on_key_release(self, key: int) -> None:
        if key in (arcade.key.UP, arcade.key.DOWN):
            self.state.accel_input = 0.0
        elif key in (arcade.key.LEFT, arcade.key.RIGHT):
            self.state.steer_input = 0.0
