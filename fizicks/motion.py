from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from fizicks.data import Vector
    from fizicks.main import Space


class FirstLaw:
    """An object in motion will remain in motion unless acted on by an external force."""

    @classmethod
    def apply(cls, object: Any, force: "Vector"):
        """
        Updates the velocity of the object based on the force applied.
        """
        object.velocity = object.velocity + force


class SecondLaw:
    @classmethod
    def apply(cls, object: Any, space: "Space"):
        """
        Updates the position of the object based on the velocity.
        """
        object.position = object.position + object.velocity
        if space.toroidal:
            object.position = object.position % space.dimensions


class ThirdLaw:
    @classmethod
    def apply(cls, object: Any):
        """
        Updates the acceleration of the object based on the velocity and mass.
        """
        object.acceleration = object.velocity / object.mass


class Motion:
    """The motion of an object is determined by the sum of its forces and the net force acting on it."""

    @classmethod
    def update(cls, object: Any, space: "Space") -> None:
        """
        Updates the object based on the forces applied and its current state.
        """
        if object.debt:
            for debt in object.debt:
                FirstLaw.apply(object, debt)
        SecondLaw.apply(object, space)
        ThirdLaw.apply(object)

        object.debt = []
