from typing import TYPE_CHECKING, Union

from fizicks.data import Universe, Vector

if TYPE_CHECKING:
    from fizicks.matter import Matter


class Collision:
    """
    Handles collision detection and resolution between objects.

    For boundary collisions, the object is teleported to the other
    side of the border.

    For object collisions, the objects are resolved using elastic
    collision formulas.

    Methods
    -------
    detect(object1: Matter, object2: Union[Matter, Universe]) -> bool
        Detects if a collision has occurred between an object and another
        object or the universe border.
    resolve(object: Matter, universe: Universe, other: Matter = None) -> None
        Resolves the collision between two objects using elastic
        collision formulas.
    """

    @staticmethod
    def detect(object: "Matter", other: Union["Matter", "Universe"]) -> bool:
        """
        Detects if a collision has occurred between an object and another object
        or the universe border.

        Parameters:
        -----------
        object : Matter
            The object to check for collision.
        other : Union[Matter, Universe]
            Either another Matter object to check for collision with object1,
            or a Universe object to check for border collision.

        Returns:
        --------
        bool
            True if a collision is detected, False otherwise.
        """
        if isinstance(other, Universe):
            return Collision._detect_border(object, other)
        else:
            return Collision._detect_objects(object, other)

    @staticmethod
    def resolve(object: "Matter", other: Union["Matter", "Universe"]) -> None:
        """
        Resolves the collision between two objects using elastic collision formulas.

        Parameters
        ----------
        object : Matter
            The object to resolve the collision for.
        universe : Universe
            The universe within which the collision is taking place.
        other : Union[Matter, Universe]
            The other object involved in the collision.
        """
        if isinstance(other, Universe):
            Collision._resolve_border(object, other)
        else:
            Collision._resolve_objects(object, other)

    @staticmethod
    def _detect_objects(object1: "Matter", object2: "Matter") -> bool:
        """
        Detects if a collision has occurred between two objects.

        Parameters
        ----------
        object1 : Matter
            The first object.
        object2 : Matter
            The second object.

        Returns
        -------
        bool
            True if a collision has occurred, False otherwise.
        """
        distance = (object1.position - object2.position).magnitude()
        return distance < (object1.radius + object2.radius)

    @staticmethod
    def _resolve_objects(object1: "Matter", object2: "Matter") -> None:
        """
        Resolves the collision between two objects using elastic collision formulas.

        Adds the correct force to the objects' debts that will be applied in
        the next update.

        Parameters
        ----------
        object1 : Matter
            The first object.
        object2 : Matter
            The second object.
        """
        # Calculate the normal and tangential vectors
        normal = (object2.position - object1.position).normalize()
        tangent = Vector(-normal.y, normal.x)

        # Decompose velocities into normal and tangential components
        v1n = normal.dot(object1.velocity)
        v1t = tangent.dot(object1.velocity)
        v2n = normal.dot(object2.velocity)
        v2t = tangent.dot(object2.velocity)

        # Update normal components using 1D elastic collision formulas
        v1n_after = (v1n * (object1.mass - object2.mass) + 2 * object2.mass * v2n) / (
            object1.mass + object2.mass
        )
        v2n_after = (v2n * (object2.mass - object1.mass) + 2 * object1.mass * v1n) / (
            object1.mass + object2.mass
        )

        # Convert scalar normal and tangential velocities into vectors
        v1n_after_vec = normal * v1n_after
        v1t_vec = tangent * v1t
        v2n_after_vec = normal * v2n_after
        v2t_vec = tangent * v2t

        # Update object debts
        #! Validate the correct force is being added.
        object1.add_debt(v1n_after_vec + v1t_vec)
        object2.add_debt(v2n_after_vec + v2t_vec)

    def _detect_border(object: "Matter", universe: "Universe") -> bool:
        """
        Detects if an object has collided with the border of the space.
        """
        if universe.toroidal:
            return False
        return (
            object.position.x < 0
            or object.position.x > universe.dimensions.x
            or object.position.y < 0
            or object.position.y > universe.dimensions.y
        )

    def _resolve_border(object: "Matter", universe: "Universe") -> None:
        """
        Resolves the collision between an object and the border of the space.
        """
        if universe.toroidal:
            # Teleport the object to the other side of the border
            if object.position.x < 0:
                object.position.x = 0
            elif object.position.x > universe.dimensions.x:
                object.position.x = universe.dimensions.x
            if object.position.y < 0:
                object.position.y = 0
            elif object.position.y > universe.dimensions.y:
                object.position.y = universe.dimensions.y


__notes__ = """

This method, `resolve_objects`, is designed to handle the resolution of collisions between two objects in a 2D space using the principles of elastic collision. Here's a step-by-step breakdown of how it works:

### Purpose
The method is used to update the velocities of two objects after they collide. The collision is treated as an elastic collision, meaning that both kinetic energy and momentum are conserved.

### Parameters
- **object1**: The first object involved in the collision.
- **object2**: The second object involved in the collision.

Both `object1` and `object2` are instances of a class named `Matter`, which presumably has attributes like `position`, `velocity`, and `mass`.

### Step-by-Step Explanation

1. **Calculate the Normal and Tangential Vectors**:
   - The **normal vector** is calculated by subtracting the position of `object1` from `object2` and then normalizing it. This vector points from `object1` to `object2` and represents the direction in which the collision occurs.
   - The **tangential vector** is calculated by rotating the normal vector 90 degrees. This vector is perpendicular to the normal vector and represents the direction along which no force is exchanged during the collision.

2. **Decompose Velocities**:
   - The velocities of `object1` and `object2` are decomposed into their normal and tangential components.
     - **Normal Component**: The component of velocity in the direction of the normal vector. This is calculated using the dot product between the velocity vector and the normal vector.
     - **Tangential Component**: The component of velocity in the direction of the tangential vector. This is calculated using the dot product between the velocity vector and the tangential vector.

3. **Update Normal Components Using 1D Elastic Collision Formulas**:
   - The normal components of the velocities are updated using the 1D elastic collision formulas. These formulas take into account the masses of both objects and ensure that momentum and kinetic energy are conserved.
   - The updated normal components (`v1n_after` for `object1` and `v2n_after` for `object2`) are calculated based on the original normal components and the masses of the objects.

4. **Convert Scalar Normal and Tangential Velocities into Vectors**:
   - The updated normal and tangential components of the velocities are converted back into vectors.
   - The normal components are scaled by the normal vector, and the tangential components are scaled by the tangential vector.

5. **Update Velocities**:
   - The final velocity of each object is calculated by adding the updated normal and tangential components.
   - These updated velocities are then assigned back to `object1` and `object2`.

### Summary
This method effectively resolves a collision between two objects by calculating how their velocities should change based on the principles of elastic collision. It ensures that the objects' new velocities respect the conservation of momentum and kinetic energy, which are fundamental to elastic collisions.


Let's walk through an example to see how the `resolve_objects` method works in practice.

### Example Setup

- **Object 1 (object1)**:
  - Position: (2, 3)
  - Velocity: (5, 0) (moving to the right)
  - Mass: 2 kg

- **Object 2 (object2)**:
  - Position: (5, 3)
  - Velocity: (-2, 0) (moving to the left)
  - Mass: 3 kg

### Execution of `resolve_objects`

#### 1. **Calculate the Normal and Tangential Vectors**

- **Normal Vector**:
  - Difference in position: `(5, 3) - (2, 3) = (3, 0)`
  - Normalized: `(3, 0)` has a magnitude of `3`, so the normalized normal vector is `(1, 0)`.
  - `normal = (1, 0)`

- **Tangential Vector**:
  - Rotate normal vector 90 degrees: If `normal = (1, 0)`, the tangential vector is `(0, 1)`.
  - `tangent = (0, 1)`

#### 2. **Decompose Velocities**

- **Object 1 (Velocity: 5, 0)**:
  - Normal component: `v1n = normal.dot((5, 0)) = 5 * 1 + 0 * 0 = 5`
  - Tangential component: `v1t = tangent.dot((5, 0)) = 5 * 0 + 0 * 1 = 0`

- **Object 2 (Velocity: -2, 0)**:
  - Normal component: `v2n = normal.dot((-2, 0)) = -2 * 1 + 0 * 0 = -2`
  - Tangential component: `v2t = tangent.dot((-2, 0)) = -2 * 0 + 0 * 1 = 0`

#### 3. **Update Normal Components Using 1D Elastic Collision Formulas**

- **Object 1**:
  - `v1n_after = ((5 * (2 - 3)) + 2 * 3 * (-2)) / (2 + 3)`
  - Simplifying: `v1n_after = (-5 + (-12)) / 5 = -17 / 5 = -3.4`

- **Object 2**:
  - `v2n_after = ((-2 * (3 - 2)) + 2 * 2 * 5) / (2 + 3)`
  - Simplifying: `v2n_after = (-2 + 20) / 5 = 18 / 5 = 3.6`

#### 4. **Convert Scalar Normal and Tangential Velocities into Vectors**

- **Object 1**:
  - `v1n_after_vec = normal * v1n_after = (1, 0) * (-3.4) = (-3.4, 0)`
  - `v1t_vec = tangent * v1t = (0, 1) * 0 = (0, 0)`

- **Object 2**:
  - `v2n_after_vec = normal * v2n_after = (1, 0) * 3.6 = (3.6, 0)`
  - `v2t_vec = tangent * v2t = (0, 1) * 0 = (0, 0)`

#### 5. **Update Velocities**

- **Object 1**:
  - New velocity: `object1.velocity = v1n_after_vec + v1t_vec = (-3.4, 0) + (0, 0) = (-3.4, 0)`

- **Object 2**:
  - New velocity: `object2.velocity = v2n_after_vec + v2t_vec = (3.6, 0) + (0, 0) = (3.6, 0)`

### Summary of Outputs

- **Object 1**:
  - Before collision: Velocity = (5, 0)
  - After collision: Velocity = (-3.4, 0)

- **Object 2**:
  - Before collision: Velocity = (-2, 0)
  - After collision: Velocity = (3.6, 0)

This means that after the collision:
- Object 1, which was moving to the right, now moves to the left with a velocity of 3.4 units.
- Object 2, which was moving to the left, now moves to the right with a velocity of 3.6 units.

This behavior is consistent with the principles of an elastic collision, where momentum and kinetic energy are conserved, and the objects exchange velocities relative to their masses.


Let's break down the purpose of each step in the `resolve_objects` method and why each one is necessary for accurately resolving an elastic collision.

### 1. **Calculate the Normal and Tangential Vectors**

- **Purpose**: The normal and tangential vectors are essential for understanding how the objects are moving relative to each other at the moment of collision.
  - **Normal Vector**: Represents the direction along which the collision occurs. The force of the collision acts along this vector.
  - **Tangential Vector**: Represents the direction perpendicular to the collision. In an elastic collision, there is no force acting in this direction, so the tangential component of the velocity remains unchanged.

- **Why Needed**: To accurately calculate how the velocities of the objects will change, we need to separate the movement into these two components. This separation allows us to apply the correct physics only to the part of the motion directly involved in the collision (the normal component).

### 2. **Decompose Velocities**

- **Purpose**: By decomposing each object's velocity into its normal and tangential components, we can isolate the parts of the motion that will be affected by the collision.
  - **Normal Component**: This part of the velocity is involved in the collision and will be updated.
  - **Tangential Component**: This part of the velocity is unaffected by the collision and will remain the same.

- **Why Needed**: This step ensures that only the relevant part of each object's velocity (the part along the line of collision) is modified, preserving the correct behavior according to the laws of physics.

### 3. **Update Normal Components Using 1D Elastic Collision Formulas**

- **Purpose**: This is where the actual physics of the collision is applied. The formulas for 1D elastic collisions update the normal components of the velocities based on the masses of the objects and their velocities before the collision.
  - These formulas ensure that both momentum and kinetic energy are conserved in the collision.

- **Why Needed**: This step is crucial for maintaining the physical accuracy of the simulation. Without it, the objects wouldn't react correctly to the collision, resulting in unrealistic behavior. It determines the new velocities that each object will have after the collision.

### 4. **Convert Scalar Normal and Tangential Velocities into Vectors**

- **Purpose**: After calculating the new normal and tangential components, they need to be converted back into vector form. This involves scaling the normal and tangential vectors by the corresponding velocity components.
  - This step reassembles the full velocity vector for each object.

- **Why Needed**: Since the objects move in 2D space, their velocities must be represented as vectors. This step combines the updated normal and unchanged tangential components to produce the final velocity vectors for the objects.

### 5. **Update Velocities**

- **Purpose**: Finally, the method updates the velocity attributes of the two objects with the newly calculated velocities.
  - This step effectively completes the collision resolution process, giving each object its new direction and speed.

- **Why Needed**: The velocities must be updated so that the objects move correctly in subsequent time steps. Without this update, the objects would continue to move with their pre-collision velocities, ignoring the effects of the collision.

### Summary

Each step in the `resolve_objects` method serves a specific role in ensuring that the collision is resolved in a way that respects the laws of physics, particularly the conservation of momentum and kinetic energy. 

- **Normal and Tangential Vectors**: Separate the motion into components relevant to the collision.
- **Decomposing Velocities**: Isolate the components that need to be modified.
- **Updating Normal Components**: Apply the physics of elastic collision.
- **Converting Back to Vectors**: Reassemble the velocities in their correct vector form.
- **Updating Velocities**: Ensure the objects reflect the results of the collision in future motion.

By following this structured approach, the method accurately simulates the collision between two objects, ensuring a realistic outcome that aligns with physical principles.


"""
