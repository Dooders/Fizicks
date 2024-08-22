import uuid
from typing import TYPE_CHECKING

from fizicks.data import Force, Position, Velocity
from fizicks.main import Fizicks

if TYPE_CHECKING:
    from fizicks.data import Vector
    from fizicks.universe import Universe


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
    color : tuple[int, int, int]
        The color of the object.
    debt : list[Force]
        The list of forces to apply to the object.

    Methods
    -------
    add_debt(force)
        Add a force to the object's debt. Will be applied in the next update.
    update(universe)
        Update the object's state based on accumulated forces and current state.
    collides_with(other)
        Check if the object collides with another object.
    description(short=True)
        A short description of the object.
    description(short=False)
        A long description of the object.

    Properties
    ----------
    position : Position
        The position of the object in the universe.
    velocity : Velocity
        The velocity of the object in the universe.
    """

    def __init__(
        self,
        position: "Position",
        velocity: "Velocity",
        mass: float,
        radius: float,
        color: tuple[int, int, int] = (255, 255, 255),
    ) -> None:
        self.id = uuid.uuid4()
        self.time = 0
        self._position: Position = position
        self._velocity: Velocity = velocity
        self.mass: float = mass
        self.radius: float = radius
        self.color: tuple[int, int, int] = color
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

    def update(self, universe: "Universe", debug: bool = False) -> None:
        """
        Update the object's state based on accumulated forces and current state.

        Parameters
        ----------
        universe : Universe
            The universe to update the object in.
        """
        Fizicks.update(self, universe, debug=debug)
        self.debt = []  # Clear forces after applying
        self.time += 1

    def collides_with(self, other: "Matter") -> bool:
        """
        Check if the object collides with another object.

        Parameters
        ----------
        other : Matter
            The object to check for collision with.
        """
        return self.position.distance(other.position) <= self.radius + other.radius

    def description(self, short: bool = True) -> str:
        if short:
            return f"Matter(id={self.id})"
        else:
            return f"Matter(id={self.id}, position={self.position}, velocity={self.velocity}, mass={self.mass}, radius={self.radius}, color={self.color})"

    def __repr__(self) -> str:
        return f"Matter(id={self.id}, position={self.position}, velocity={self.velocity}, mass={self.mass}, radius={self.radius}, color={self.color})"

    def __str__(self) -> str:
        return f"Matter(id={self.id}, position={self.position}, velocity={self.velocity}, mass={self.mass}, radius={self.radius}, color={self.color})"

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
