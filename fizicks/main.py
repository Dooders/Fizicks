from typing import Any, Tuple

from fizicks.motion import Motion


class Space:
    #! call it World? or PhysicalSpace? or Map?
    def __init__(
        self,
        dimensions: Tuple[int, int, int] = (100, 100, 100),
        toroidal: bool = False,
        boundaries: bool = False,
    ) -> None:
        self.dimensions = dimensions
        self.toroidal = toroidal
        self.boundaries = boundaries


class Fizicks:
    """
    Physics are applied with a debt system. When a force is applied to an object,
    the object is given a debt. The object will then be updated in its next step,
    and the debt will be resolved.

    Parameters
    ----------
    object : Any
        The object to apply the physics to. When initialized, the object
        is given a list that tracks its debts.
    space : Space
        The space to apply the physics to. By default, the space is a 3D space
        with dimensions (100, 100, 100) with no boundaries.

    Methods
    -------
    update()
        Updates the object's state by applying rigid motion physics.
    """

    def __init__(self, object: Any, space: Space = Space()) -> None:
        object.debt = []
        self.motion = Motion()
        self.space = space

    def update(self) -> None:
        """
        Updates the object's state by applying rigid motion physics.
        """
        self.motion.update(self.object, self.space)
