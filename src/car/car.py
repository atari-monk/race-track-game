from __future__ import annotations
from typing import Final
import arcade
import math

class Car(arcade.Sprite):
    LENGTH: Final[float] = 60.0
    WIDTH: Final[float] = 30.0
    MASS: Final[float] = 1000.0
    MAX_STEER_ANGLE: Final[float] = math.radians(45)
    MAX_STEER_RATE: Final[float] = math.radians(300)
    MAX_SPEED: Final[float] = 5200.0
    ACCELERATION_FORCE: Final[float] = 800000.0
    BRAKE_FORCE: Final[float] = 10000000.0
    DRAG_COEFF: Final[float] = 1.2
    FRICTION_LIMIT: Final[float] = 24000.0
    DT: Final[float] = 1 / 60.0
    STEER_RESPONSE_CURVE: Final[float] = 0.5

    def __init__(self) -> None:
        super().__init__()
        self.width = self.WIDTH
        self.height = self.LENGTH
        self.center_x = 100.0
        self.center_y = 100.0
        self.heading = 0.0
        self.steer_angle = 0.0
        self.speed = 0.0
        self.acceleration = 0.0
        self.steer_input = 0.0
        self.accel_input = 0.0

    def update(self) -> None:
        speed_factor = 1.0 - min(1.0, abs(self.speed)/self.MAX_SPEED) * self.STEER_RESPONSE_CURVE
        max_steer = self.MAX_STEER_ANGLE * speed_factor
        
        steer_rate = self.steer_input * self.MAX_STEER_RATE * self.DT * (1.0 + 2.0 * speed_factor)
        self.steer_angle += steer_rate

        if self.steer_input == 0.0:
            center_rate = self.MAX_STEER_RATE * 1.5 * self.DT
            if self.steer_angle > 0:
                self.steer_angle = max(0.0, self.steer_angle - center_rate)
            elif self.steer_angle < 0:
                self.steer_angle = min(0.0, self.steer_angle + center_rate)

        self.steer_angle = max(-max_steer, min(self.steer_angle, max_steer))

        if self.accel_input > 0:
            force = self.accel_input * self.ACCELERATION_FORCE
        elif self.accel_input < 0:
            force = self.accel_input * self.BRAKE_FORCE
        else:
            force = 0.0
        drag = self.DRAG_COEFF * abs(self.speed) * self.speed * (-1 if self.speed > 0 else 1)
        net_force = force + drag
        traction_force = max(-self.FRICTION_LIMIT, min(net_force, self.FRICTION_LIMIT))

        self.acceleration = traction_force / self.MASS
        self.speed += self.acceleration * self.DT * 1.1  # Slightly faster response
        self.speed = max(-self.MAX_SPEED * 0.5, min(self.speed, self.MAX_SPEED))  # Limit reverse speed

        rear_axle_x = self.center_x - (self.LENGTH / 2) * math.cos(self.heading)
        rear_axle_y = self.center_y - (self.LENGTH / 2) * math.sin(self.heading)

        beta = math.atan(math.tan(self.steer_angle) / 2)
        speed_factor = min(1.0, abs(self.speed)/300)  # Adjust turning radius at speed
        dx = self.speed * math.cos(self.heading + beta * (1.0 - speed_factor * 0.3)) * self.DT
        dy = self.speed * math.sin(self.heading + beta * (1.0 - speed_factor * 0.3)) * self.DT
        dtheta = (self.speed / (self.LENGTH * (1.0 + speed_factor * 2))) * math.sin(self.steer_angle) * self.DT

        rear_axle_x += dx
        rear_axle_y += dy
        self.heading += dtheta

        self.center_x = rear_axle_x + (self.LENGTH / 2) * math.cos(self.heading)
        self.center_y = rear_axle_y + (self.LENGTH / 2) * math.sin(self.heading)
        self.angle = math.degrees(self.heading)

    def draw(self) -> None:
        corners = [
            (-self.LENGTH/2, -self.WIDTH/2),
            (self.LENGTH/2, -self.WIDTH/2),
            (self.LENGTH/2, self.WIDTH/2),
            (-self.LENGTH/2, self.WIDTH/2)
        ]

        rotated_corners: list[tuple[float, float]] = []
        for x, y in corners:
            rx = x * math.cos(self.heading) - y * math.sin(self.heading)
            ry = x * math.sin(self.heading) + y * math.cos(self.heading)
            tx = self.center_x + rx
            ty = self.center_y + ry
            rotated_corners.append((tx, ty))

        arcade.draw_polygon_filled(rotated_corners, arcade.color.RED)

        front_x = self.center_x + (self.LENGTH/2) * math.cos(self.heading)
        front_y = self.center_y + (self.LENGTH/2) * math.sin(self.heading)
        arcade.draw_circle_filled(front_x, front_y, 4, arcade.color.YELLOW)

    def on_key_press(self, key: int) -> None:
        if key == arcade.key.UP:
            self.accel_input = 1.0
        elif key == arcade.key.DOWN:
            self.accel_input = -1.0
        elif key == arcade.key.LEFT:
            self.steer_input = 1.0
        elif key == arcade.key.RIGHT:
            self.steer_input = -1.0

    def on_key_release(self, key: int) -> None:
        if key in (arcade.key.UP, arcade.key.DOWN):
            self.accel_input = 0.0
        elif key in (arcade.key.LEFT, arcade.key.RIGHT):
            self.steer_input = 0.0