from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fizicks.data import Vector
    from fizicks.matter import Matter


class Collision:
    """
    Handles collision detection and resolution between objects.

    Methods
    -------
    detect(object1: Matter, object2: Matter) -> bool
        Detects if a collision has occurred between two objects.
    resolve(object1: Matter, object2: Matter) -> None
        Resolves the collision between two objects using elastic collision formulas.
    """

    @staticmethod
    def detect(object1: "Matter", object2: "Matter") -> bool:
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
    def resolve(object1: "Matter", object2: "Matter") -> None:
        """
        Resolves the collision between two objects using elastic collision formulas.

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

        # Update velocities
        object1.velocity = v1n_after_vec + v1t_vec
        object2.velocity = v2n_after_vec + v2t_vec
