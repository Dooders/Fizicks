from typing import Any, List


class Vector:
    """A vector is a quantity in three-dimensional space that has both magnitude and direction."""

    def __init__(self, x: float, y: float, z: float) -> None:
        """
        Initializes the vector with the given x, y, and z coordinates.

        Parameters
        ----------
        x : float
            The x coordinate of the vector.
        y : float
            The y coordinate of the vector.
        z : float
            The z coordinate of the vector.
        """
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other: "Vector") -> "Vector":
        return self.__class__(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: "Vector") -> "Vector":
        return self.__class__(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other: float) -> "Vector":
        return self.__class__(self.x * other, self.y * other, self.z * other)

    def __truediv__(self, other: float) -> "Vector":
        return self.__class__(
            int(self.x / other), int(self.y / other), int(self.z / other)
        )

    def __repr__(self):
        return f"{self.__class__.__name__}({self.x}, {self.y}, {self.z})"

    def __str__(self):
        return f"{self.__class__.__name__}({self.x}, {self.y}, {self.z})"


class Force(Vector):
    """A force is a vector that describes the change in momentum of an object over time."""

    def __init__(self, x: float, y: float, z: float):
        super().__init__(x, y, z)


class Position(Vector):
    """The position of an object is a vector that describes its location in space."""

    def __init__(self, x: float, y: float, z: float):
        super().__init__(x, y, z)


class Velocity(Vector):
    """The velocity of an object is a vector that describes its speed and direction in space."""

    def __init__(self, x: float, y: float, z: float):
        self.x = x
        super().__init__(x, y, z)


class FirstLaw:
    """An object in motion will remain in motion unless acted on by an external force."""

    @classmethod
    def apply(cls, object: Any, force: Vector):
        """
        Updates the velocity of the object based on the force applied.
        """
        object.velocity = object.velocity + force


class SecondLaw:
    @classmethod
    def apply(cls, object: Any):
        """
        Updates the position of the object based on the velocity.
        """
        object.position = object.position + object.velocity


class ThirdLaw:
    @classmethod
    def apply(cls, object: Any):
        """
        Updates the velocity of the object based on the acceleration.
        """
        object.acceleration = object.velocity / object.mass
        object.velocity = object.velocity + object.acceleration


class Motion:
    """The motion of an object is determined by the sum of its forces and the net force acting on it."""

    @classmethod
    def update(cls, object: Any, debts: List[Force]) -> None:
        """
        Updates the object based on the forces applied and its current state.
        """
        for debt in debts:
            FirstLaw.apply(object, debt)
        SecondLaw.apply(object)
        ThirdLaw.apply(object)

        object.debt = []