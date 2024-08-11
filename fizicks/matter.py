from typing import TYPE_CHECKING

from fizicks.data import Force, Position, Velocity
from fizicks.main import Fizicks

if TYPE_CHECKING:
    from fizicks.data import Vector
    from fizicks.main import Universe


class Matter:
    """
    Matter is a class that represents a physical object in the universe.

    Parameters
    ----------
    position : Position
        The position of the object in the universe.
    velocity : Velocity
        The velocity of the object in the universe.
    mass : float
        The mass of the object.
    radius : float
        The radius of the object.
    debt : list[Force]
        The list of forces to apply to the object.

    Methods
    -------
    add_debt(force)
        Add a force to the object's debt. Will be applied in the next update.
    update(universe)
        Update the object's state based on accumulated forces and current state.

    Properties
    ----------
    position : Position
        The position of the object in the universe.
    velocity : Velocity
        The velocity of the object in the universe.
    """

    def __init__(
        self, position: "Position", velocity: "Velocity", mass: float, radius: float
    ) -> None:
        self._position: Position = position
        self._velocity: Velocity = velocity
        self.mass: float = mass
        self.radius: float = radius
        self.debt: list[Force] = []

    def add_debt(self, force: "Force") -> None:
        """
        Add a force to the object's debt.

        Parameters
        ----------
        force : Force
            The force to apply to the object.
        """
        self.debt.append(force)

    def update(self, universe: "Universe") -> None:
        """
        Update the object's state based on accumulated forces and current state.

        Parameters
        ----------
        universe : Universe
            The universe to update the object in.
        """
        Fizicks.update(self, universe)
        self.debt = []  # Clear forces after applying

    @property
    def position(self) -> "Position":
        return self._position

    @position.setter
    def position(self, value: "Vector") -> None:
        self._position = Position(*value)

    @property
    def velocity(self) -> "Velocity":
        return self._velocity

    @velocity.setter
    def velocity(self, value: "Vector") -> None:
        self._velocity = Velocity(*value)
