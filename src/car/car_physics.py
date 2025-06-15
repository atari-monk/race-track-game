import math
from src.car.car_specs import CarSpecs
from src.car.car_state import CarState

class CarPhysics:
    def __init__(self, specs: CarSpecs, state: CarState) -> None:
        self.specs = specs
        self.state = state

    def update_steering(self) -> None:
        speed_factor = self._compute_speed_factor()
        max_steer = self._compute_max_steer(speed_factor)
        steer_rate = self._compute_steer_rate(speed_factor)
        self._apply_steering_input(steer_rate)
        self._auto_center_steering()
        self._clamp_steer_angle(max_steer)

    def _compute_speed_factor(self) -> float:
        return 1.0 - min(1.0, abs(self.state.speed) / self.specs.max_speed) * self.specs.steer_response_curve

    def _compute_max_steer(self, speed_factor: float) -> float:
        return self.specs.max_steer_angle * speed_factor

    def _compute_steer_rate(self, speed_factor: float) -> float:
        return self.state.steer_input * self.specs.max_steer_rate * self.specs.dt * (1.0 + 2.0 * speed_factor)

    def _apply_steering_input(self, steer_rate: float) -> None:
        self.state.steer_angle += steer_rate

    def _auto_center_steering(self) -> None:
        if self.state.steer_input == 0.0:
            center_rate = self.specs.max_steer_rate * 1.5 * self.specs.dt
            if self.state.steer_angle > 0:
                self.state.steer_angle = max(0.0, self.state.steer_angle - center_rate)
            elif self.state.steer_angle < 0:
                self.state.steer_angle = min(0.0, self.state.steer_angle + center_rate)

    def _clamp_steer_angle(self, max_steer: float) -> None:
        self.state.steer_angle = max(-max_steer, min(self.state.steer_angle, max_steer))

    def update_movement(self) -> None:
        force = self._compute_input_force()
        drag = self._compute_drag()
        net_force = self._compute_net_force(force, drag)
        traction_force = self._apply_friction_limit(net_force)
        self._update_speed(traction_force)

    def _compute_input_force(self) -> float:
        if self.state.accel_input > 0:
            return self.state.accel_input * self.specs.acceleration_force
        if self.state.accel_input < 0:
            return self.state.accel_input * self.specs.brake_force
        return 0.0

    def _compute_drag(self) -> float:
        return self.specs.drag_coeff * abs(self.state.speed) * self.state.speed * (-1 if self.state.speed > 0 else 1)

    def _compute_net_force(self, force: float, drag: float) -> float:
        return force + drag

    def _apply_friction_limit(self, net_force: float) -> float:
        return max(-self.specs.friction_limit, min(net_force, self.specs.friction_limit))

    def _update_speed(self, traction_force: float) -> None:
        self.state.acceleration = traction_force / self.specs.mass
        self.state.speed += self.state.acceleration * self.specs.dt * 1.1
        self.state.speed = max(-self.specs.max_speed * 0.5, min(self.state.speed, self.specs.max_speed))

    def update_position(self) -> None:
        rear_x, rear_y = self._compute_rear_axle()
        beta = math.atan(math.tan(self.state.steer_angle) / 2)
        speed_factor = min(1.0, abs(self.state.speed) / 300)
        dx, dy = self._compute_position_deltas(beta, speed_factor)
        dtheta = self._compute_rotation(beta, speed_factor)

        rear_x += dx
        rear_y += dy
        self.state.heading += dtheta

        self._update_center_position(rear_x, rear_y)

    def _compute_rear_axle(self) -> tuple[float, float]:
        x = self.state.center_x - (self.specs.length / 2) * math.cos(self.state.heading)
        y = self.state.center_y - (self.specs.length / 2) * math.sin(self.state.heading)
        return x, y

    def _compute_position_deltas(self, beta: float, speed_factor: float) -> tuple[float, float]:
        angle = self.state.heading + beta * (1.0 - speed_factor * 0.3)
        dx = self.state.speed * math.cos(angle) * self.specs.dt
        dy = self.state.speed * math.sin(angle) * self.specs.dt
        return dx, dy

    def _compute_rotation(self, beta: float, speed_factor: float) -> float:
        return (self.state.speed / (self.specs.length * (1.0 + speed_factor * 2))) * math.sin(self.state.steer_angle) * self.specs.dt

    def _update_center_position(self, rear_x: float, rear_y: float) -> None:
        self.state.center_x = rear_x + (self.specs.length / 2) * math.cos(self.state.heading)
        self.state.center_y = rear_y + (self.specs.length / 2) * math.sin(self.state.heading)

