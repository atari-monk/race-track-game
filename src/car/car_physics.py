import math
from src.car.car_specs import CarSpecs
from src.car.car_state import CarState

class CarPhysics:
    def __init__(self, specs: CarSpecs, state: CarState) -> None:
        self.specs = specs
        self.state = state

    def update_steering(self) -> None:
        speed_factor = 1.0 - min(1.0, abs(self.state.speed)/self.specs.max_speed) * self.specs.steer_response_curve
        max_steer = self.specs.max_steer_angle * speed_factor

        steer_rate = self.state.steer_input * self.specs.max_steer_rate * self.specs.dt * (1.0 + 2.0 * speed_factor)
        self.state.steer_angle += steer_rate

        if self.state.steer_input == 0.0:
            center_rate = self.specs.max_steer_rate * 1.5 * self.specs.dt
            if self.state.steer_angle > 0:
                self.state.steer_angle = max(0.0, self.state.steer_angle - center_rate)
            elif self.state.steer_angle < 0:
                self.state.steer_angle = min(0.0, self.state.steer_angle + center_rate)

        self.state.steer_angle = max(-max_steer, min(self.state.steer_angle, max_steer))

    def update_movement(self) -> None:
        if self.state.accel_input > 0:
            force = self.state.accel_input * self.specs.acceleration_force
        elif self.state.accel_input < 0:
            force = self.state.accel_input * self.specs.brake_force
        else:
            force = 0.0
        
        drag = self.specs.drag_coeff * abs(self.state.speed) * self.state.speed * (-1 if self.state.speed > 0 else 1)
        net_force = force + drag
        traction_force = max(-self.specs.friction_limit, min(net_force, self.specs.friction_limit))

        self.state.acceleration = traction_force / self.specs.mass
        self.state.speed += self.state.acceleration * self.specs.dt * 1.1
        self.state.speed = max(-self.specs.max_speed * 0.5, min(self.state.speed, self.specs.max_speed))

    def update_position(self) -> None:
        rear_axle_x = self.state.center_x - (self.specs.length / 2) * math.cos(self.state.heading)
        rear_axle_y = self.state.center_y - (self.specs.length / 2) * math.sin(self.state.heading)

        beta = math.atan(math.tan(self.state.steer_angle) / 2)
        speed_factor = min(1.0, abs(self.state.speed)/300)
        dx = self.state.speed * math.cos(self.state.heading + beta * (1.0 - speed_factor * 0.3)) * self.specs.dt
        dy = self.state.speed * math.sin(self.state.heading + beta * (1.0 - speed_factor * 0.3)) * self.specs.dt
        dtheta = (self.state.speed / (self.specs.length * (1.0 + speed_factor * 2))) * math.sin(self.state.steer_angle) * self.specs.dt

        rear_axle_x += dx
        rear_axle_y += dy
        self.state.heading += dtheta

        self.state.center_x = rear_axle_x + (self.specs.length / 2) * math.cos(self.state.heading)
        self.state.center_y = rear_axle_y + (self.specs.length / 2) * math.sin(self.state.heading)