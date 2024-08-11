from typing import TYPE_CHECKING

from fizicks.data import Force, Position, Velocity
from fizicks.main import Fizicks

if TYPE_CHECKING:
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
    apply_force(force)
        Apply a force to the object.
    update(universe)
        Update the object's state based on accumulated forces and current state.
    """

    def __init__(
        self, position: "Position", velocity: "Velocity", mass: float, radius: float
    ) -> None:
        self.position: Position = position
        self.velocity: Velocity = velocity
        self.mass: float = mass
        self.radius: float = radius
        self.debt: list[Force] = []

    def apply_force(self, force: "Force") -> None:
        """
        Apply a force to the object.

        Parameters
        ----------
        force : Force
            The force to apply to the object.
        """
        self.velocity = Velocity(
            self.velocity.x + force.x,
            self.velocity.y + force.y,
            self.velocity.z + force.z,
        )

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
