import math
import arcade
from src.car.car_input import CarInput
from src.car.car_physics import CarPhysics
from src.car.car_renderer import CarRenderer
from src.car.car_specs import CarSpecs
from src.car.car_state import CarState

class Car(arcade.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.specs = CarSpecs()
        self.state = CarState()
        self.physics = CarPhysics(self.specs, self.state)
        self.renderer = CarRenderer(self.specs, self.state)
        self.input = CarInput(self.state)
        
        self.width = self.specs.width
        self.height = self.specs.length
        self.angle = math.degrees(self.state.heading)

    def update(self) -> None:
        self.physics.update_steering()
        self.physics.update_movement()
        self.physics.update_position()
        self.angle = math.degrees(self.state.heading)

    def draw(self) -> None:
        self.renderer.draw()

    def on_key_press(self, key: int) -> None:
        self.input.on_key_press(key)

    def on_key_release(self, key: int) -> None:
        self.input.on_key_release(key)