# Car Physics System

This document details how the car system in the race-track-game works. The car is a dynamic 2D object that responds to user input, simulates real-world physics, and renders on screen using the `arcade` library.

---

## Components Overview

The car system is composed of the following classes:

- `Car`: Main controller tying together specs, state, physics, rendering, and input.
- `CarSpecs`: Contains immutable physical constants (mass, acceleration, dimensions, etc.).
- `CarState`: Holds mutable state values (position, velocity, heading, etc.).
- `CarPhysics`: Handles physics logic—steering, speed, and position updates.
- `CarRenderer`: Renders the car based on its state and specs.
- `CarInput`: Updates `CarState` inputs based on keyboard events.

---

## 1. CarSpecs

`CarSpecs` defines the static configuration of a car:

| Parameter             | Description                             |
|-----------------------|-----------------------------------------|
| `length`              | Car's length in pixels                  |
| `width`               | Car's width in pixels                   |
| `mass`                | Car's mass in kg                        |
| `max_steer_angle`     | Maximum steering angle (radians)        |
| `max_steer_rate`      | Maximum rate of steering (radians/sec)  |
| `max_speed`           | Top speed in pixels/sec                 |
| `acceleration_force`  | Forward engine force (Newtons)          |
| `brake_force`         | Reverse brake force (Newtons)           |
| `drag_coeff`          | Air resistance coefficient              |
| `friction_limit`      | Max traction force                      |
| `dt`                  | Fixed timestep (seconds)                |
| `steer_response_curve`| How speed affects steer response        |

---

## 2. CarState

`CarState` holds all runtime variables describing the car's current physical state:

| Property        | Description                                   |
|-----------------|-----------------------------------------------|
| `center_x`      | X position of the car center                  |
| `center_y`      | Y position of the car center                  |
| `heading`       | Orientation angle (radians)                   |
| `steer_angle`   | Current steering angle                        |
| `speed`         | Current speed                                |
| `acceleration`  | Current acceleration                         |
| `steer_input`   | User input for steering (-1 to 1)             |
| `accel_input`   | User input for acceleration (-1 to 1)         |

---

## 3. CarPhysics

### 3.1 Steering Update

- **Speed-dependent steering**: At higher speeds, steering angle is reduced using a response curve.
- **Steering rate**: Controlled by `max_steer_rate`, scaled by user input and timestep.
- **Auto-centering**: When no steering input, the wheels gradually return to zero.
- **Clamping**: Final steer angle is clamped within allowed bounds.

### 3.2 Movement Update

- **Input Force**: Positive for throttle, negative for brakes, zero if no input.
- **Drag Force**: Simulated with a quadratic drag model opposing velocity.
- **Friction**: Limits maximum traction force using `friction_limit`.
- **Acceleration**: Newton’s 2nd law: `a = F / m`.
- **Speed Update**: Speed is updated based on acceleration and clamped to max limits.

### 3.3 Position Update

- **Rear axle as reference**: Car's position is updated using the rear axle, improving realism in turns.
- **Slip angle**: Approximated using the steering angle to compute `beta`.
- **Delta movement**: Uses heading + slip to calculate `dx`, `dy`.
- **Heading change**: Angular rotation based on steer angle and speed.
- **Center position**: Rear axle position + offset to get new center.

---

## 4. CarInput

Handles input mapping from keyboard to physical inputs:

| Key           | Effect                        |
|---------------|-------------------------------|
| `UP`          | Throttle forward (`+1.0`)     |
| `DOWN`        | Brake/reverse (`-1.0`)        |
| `LEFT`        | Steer left (`+1.0`)           |
| `RIGHT`       | Steer right (`-1.0`)          |

On release, inputs are reset to `0.0`.

---

## 5. CarRenderer

Uses `arcade` to render the car:

- Renders a red rectangle representing the body using `draw_polygon_filled`.
- A yellow circle is drawn at the front to indicate direction.
- Applies rotation based on `heading` and transforms local corners to world coordinates.

---

## 6. Car Class

Main `arcade.Sprite` that binds everything together:

- Holds instances of `CarSpecs`, `CarState`, `CarPhysics`, `CarRenderer`, and `CarInput`.
- `update()` calls physics update methods in sequence.
- `draw()` delegates to renderer.
- `on_key_press()` and `on_key_release()` delegate to input.

---

## Summary

The car system is a simplified simulation of real-world vehicle physics with a focus on arcade-style responsiveness. The simulation includes:

- Dynamic steering based on speed
- Acceleration and braking with traction limits
- Air drag and inertia
- Rear-axle based positioning for realistic cornering
- Complete decoupling of input, physics, and rendering for clean architecture

