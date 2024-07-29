# Fizicks
![Project Status](https://img.shields.io/badge/status-in%20development-orange)

## Overview

This library provides a set of classes and methods to simulate physical phenomena in three-dimensional space. It includes representations for vectors, forces, positions, velocities, and the application of Newton's laws of motion.

## Classes

### Vector

A `Vector` represents a quantity in three-dimensional space with both magnitude and direction.

#### Initialization

```python
Vector(x: float, y: float, z: float)
```

- `x`: The x-coordinate of the vector.
- `y`: The y-coordinate of the vector.
- `z`: The z-coordinate of the vector.

#### Methods

- `__add__(self, other: Vector) -> Vector`: Adds two vectors.
- `__sub__(self, other: Vector) -> Vector`: Subtracts one vector from another.
- `__mul__(self, other: float) -> Vector`: Multiplies the vector by a scalar.
- `__truediv__(self, other: float) -> Vector`: Divides the vector by a scalar.
- `__eq__(self, other: Vector) -> bool`: Checks if two vectors are equal.
- `__ne__(self, other: Vector) -> bool`: Checks if two vectors are not equal.
- `__repr__(self) -> str`: Returns a string representation of the vector.
- `__str__(self) -> str`: Returns a string representation of the vector.

### Force

A `Force` is a vector that describes the change in momentum of an object over time. Inherits from `Vector`.

#### Initialization

```python
Force(x: float, y: float, z: float)
```

### Position

A `Position` is a vector that describes the location of an object in space. Inherits from `Vector`.

#### Initialization

```python
Position(x: float, y: float, z: float)
```

### Velocity

A `Velocity` is a vector that describes the speed and direction of an object in space. Inherits from `Vector`.

#### Initialization

```python
Velocity(x: float, y: float, z: float)
```

### FirstLaw

Represents Newton's First Law of Motion: An object in motion will remain in motion unless acted on by an external force.

#### Methods

- `apply(cls, object: Any, force: Vector)`: Updates the velocity of the object based on the force applied.

### SecondLaw

Represents Newton's Second Law of Motion: The acceleration of an object is dependent on the net force acting on the object and the object's mass.

#### Methods

- `apply(cls, object: Any)`: Updates the position of the object based on the velocity.

### ThirdLaw

Represents Newton's Third Law of Motion: For every action, there is an equal and opposite reaction.

#### Methods

- `apply(cls, object: Any)`: Updates the acceleration of the object based on the velocity and mass.

### Motion

The `Motion` class determines the motion of an object based on the sum of its forces and the net force acting on it.

#### Methods

- `update(cls, object: Any)`: Updates the object based on the forces applied and its current state.

## Usage

To use this library, initialize the vectors and apply the laws of motion to simulate physical phenomena. Here is an example:

```python
# Initialize vectors
position = Position(0.0, 0.0, 0.0)
velocity = Velocity(1.0, 1.0, 1.0)
force = Force(0.5, 0.5, 0.5)

# Create an object with these vectors
object = Any()
object.position = position
object.velocity = velocity
object.debt = [force]

# Update the motion of the object
Motion.update(object)

# Print the updated position and velocity
print(object.position)
print(object.velocity)
```

This example initializes a position, velocity, and force, applies the force to the object, and updates its motion according to the laws of motion defined in this library.