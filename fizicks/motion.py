from typing import TYPE_CHECKING, Any

from fizicks.collision import Collision

if TYPE_CHECKING:
    from fizicks.data import Force, Universe
    from fizicks.matter import Matter


class FirstLaw:
    """An object in motion will remain in motion unless acted on by an external force."""

    @classmethod
    def apply(cls, object: "Matter", force: "Force") -> None:
        """
        Updates the velocity of the object based on the force applied.

        Parameters
        ----------
        object : Matter
            The object to apply the force to.
        force : Force
            The force to apply to the object.
        """
        object.velocity = object.velocity + force


class SecondLaw:
    """The acceleration of an object is directly proportional to the net force acting on it and inversely proportional to its mass."""

    @classmethod
    def apply(cls, object: "Matter") -> None:
        """
        Updates the position of the object based on the velocity.

        Parameters
        ----------
        object : Matter
            The object to apply the force to.
        """
        object.position = object.position + object.velocity


class ThirdLaw:
    """For every action, there is an equal and opposite reaction."""

    @classmethod
    def apply(cls, object: "Matter") -> None:
        """
        Updates the acceleration of the object based on the velocity and mass.

        Parameters
        ----------
        object : Matter
            The object to apply the force to.
        """
        object.acceleration = object.velocity / object.mass


class Motion:
    """
    The motion of an object is determined by the sum of its forces and the net force acting on it.

    Motion process:
    1. Check for collisions with objects or boundaries.
    2. Apply the forces to the object.
    3. Update the object's state based on the forces applied and its current state.
    """

    @classmethod
    def update(cls, object: Any, universe: "Universe") -> None:
        """
        Updates the object based on the forces applied and its current state.

        Parameters
        ----------
        object : Any
            The object to update.
        universe : Universe
            The universe to update the object in.
        """
        # Check for collisions with the universe
        if Collision.detect(object, universe):
            Collision.resolve(object, universe)

        # Check for collisions with other objects
        for other_object in universe.objects:
            if other_object is not object and Collision.detect(object, other_object):
                Collision.resolve(object, other_object)

        # Apply the forces of motion
        if object.debt:
            for debt in object.debt:
                FirstLaw.apply(object, debt)
        SecondLaw.apply(object)
        ThirdLaw.apply(object)
