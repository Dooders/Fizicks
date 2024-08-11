from typing import Any, Tuple

from fizicks.motion import Motion


class Universe:
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
    universe : Universe
        The space to apply the physics to.
    Methods
    -------
    update()
        Updates the object's state by applying rigid motion physics.
    """

    def __init__(self, object: Any, universe: Universe = Universe()) -> None:
        object.debt = []
        self.motion = Motion()
        self.universe = universe

    def update(self) -> None:
        """
        Updates the object's state by applying rigid motion physics.
        """
        self.motion.update(self.object, self.universe)
