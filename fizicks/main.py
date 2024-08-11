from typing import TYPE_CHECKING

from fizicks.motion import Motion

if TYPE_CHECKING:
    from fizicks.data import Universe
    from fizicks.matter import Matter


class Fizicks:
    """
    Physics are applied with a debt system. When a force is applied to an object,
    the object is given a debt. The object will then be updated in its next step,
    and the debt will be resolved.

    Methods
    -------
    update(object, universe)
        Updates the object's state by applying rigid motion physics.
    """

    @classmethod
    def update(cls, object: "Matter", universe: "Universe") -> None:
        """
        Updates the object's state by applying rigid motion physics.

        Parameters
        ----------
        object : Any
            The object to apply the physics to.
        universe : Universe
            The space to apply the physics to.
        """
        Motion.update(object, universe)
