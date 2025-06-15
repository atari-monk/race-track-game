# Car Physics Documentation

## Overview
The `CarPhysics` class handles all physics calculations for a car in the racing game. It manages steering, movement, and position updates based on car specifications and current state.

## Dependencies
- `math`: Used for trigonometric calculations
- `CarSpecs`: Contains car specifications (constants)
- `CarState`: Contains car's current state (variables)

## Core Methods

### `update_steering()`
Updates the car's steering angle based on input and physics.

#### Internal Methods:
- `_compute_speed_factor()`: Calculates speed-based steering response
- `_compute_max_steer(speed_factor)`: Computes maximum steering angle based on speed
- `_compute_steer_rate(speed_factor)`: Calculates steering rate from input
- `_apply_steering_input(steer_rate)`: Applies steering change
- `_auto_center_steering()`: Gradually centers steering when no input
- `_clamp_steer_angle(max_steer)`: Limits steering angle

### `update_movement()`
Updates the car's speed based on acceleration and forces.

#### Internal Methods:
- `_compute_input_force()`: Calculates force from acceleration/brake input
- `_compute_drag()`: Calculates air resistance
- `_compute_net_force(force, drag)`: Combines forces
- `_apply_friction_limit(net_force)`: Limits force by friction
- `_update_speed(traction_force)`: Updates speed and acceleration

### `update_position()`
Updates the car's position and rotation.

#### Internal Methods:
- `_compute_rear_axle()`: Calculates rear axle position
- `_compute_position_deltas(beta, speed_factor)`: Calculates position change
- `_compute_rotation(beta, speed_factor)`: Calculates rotation change
- `_update_center_position(rear_x, rear_y)`: Updates car center position

## Physics Concepts

### Steering
- Steering response decreases with speed
- Steering auto-centers when no input
- Maximum steering angle decreases with speed

### Movement
- Combines input force and drag
- Limits force by friction
- Updates speed based on net force

### Position
- Uses rear axle as reference point
- Implements simple vehicle dynamics
- Speed affects turning radius