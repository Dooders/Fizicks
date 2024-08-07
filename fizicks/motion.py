from typing import TYPE_CHECKING, Any

from fizicks.collision import Collision

if TYPE_CHECKING:
    from fizicks.data import Area, Force
    from fizicks.matter import Matter


class FirstLaw:
    """An object in motion will remain in motion unless acted on by an external force."""

    @classmethod
    def apply(cls, object: "Matter", force: "Force") -> None:
        """
        Updates the velocity of the object based on the force applied.
        """
        object.velocity = object.velocity + force


class SecondLaw:
    @classmethod
    def apply(cls, object: "Matter", area: "Area") -> None:
        """
        Updates the position of the object based on the velocity.
        """
        object.position = object.position + object.velocity
        if area.has_boundaries:
            object.position = object.position % area.dimensions


class ThirdLaw:
    @classmethod
    def apply(cls, object: "Matter") -> None:
        """
        Updates the acceleration of the object based on the velocity and mass.
        """
        object.acceleration = object.velocity / object.mass


class Motion:
    """The motion of an object is determined by the sum of its forces and the net force acting on it."""

    @classmethod
    def update(cls, object: Any, area: "Area") -> None:
        """
        Updates the object based on the forces applied and its current state.
        """
        if object.debt:
            for debt in object.debt:
                FirstLaw.apply(object, debt)
        SecondLaw.apply(object, area)
        ThirdLaw.apply(object)
        object.debt = []
        
        # Check for collisions with other objects
        for other_object in area.objects:
            if other_object is not object and Collision.detect(object, other_object):
                Collision.resolve(object, other_object)




