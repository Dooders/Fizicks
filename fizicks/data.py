class Vector:
    """
    A vector is a quantity in three-dimensional space that has both magnitude and direction.

    Methods
    -------
    magnitude():
        Returns the magnitude of the vector.
    normalize():
        Returns the normalized vector.
    dot(other: "Vector") -> float:
        Returns the dot product of two vectors.
    copy():
        Returns a copy of the vector.
    distance(other: "Vector") -> float:
        Returns the distance between two vectors.
    """

    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0) -> None:
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

    def __eq__(self, other: "Vector") -> bool:
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __ne__(self, other: "Vector") -> bool:
        return not self == other

    def __repr__(self):
        return f"{self.__class__.__name__}({self.x}, {self.y}, {self.z})"

    def __str__(self):
        return f"{self.__class__.__name__}({self.x}, {self.y}, {self.z})"

    def __mod__(self, other):
        return Vector(
            self.x % other.x if other.x != 0 else self.x,
            self.y % other.y if other.y != 0 else self.y,
            self.z % other.z if other.z != 0 else self.z,
        )

    def __iter__(self):
        """Returns an iterator over the vector."""
        return iter((self.x, self.y, self.z))

    def __call__(self):
        """Returns the vector as a tuple."""
        return (self.x, self.y, self.z)

    def magnitude(self) -> float:
        """Returns the magnitude of the vector."""
        return (self.x**2 + self.y**2 + self.z**2) ** 0.5

    def normalize(self) -> "Vector":
        """Returns the normalized vector."""
        mag = self.magnitude()
        if mag == 0:
            return Vector(0, 0, 0)  # Return a zero vector if magnitude is zero
        return self / mag

    def dot(self, other: "Vector") -> float:
        """Returns the dot product of two vectors."""
        return self.x * other.x + self.y * other.y + self.z * other.z

    def copy(self) -> "Vector":
        """Returns a copy of the vector."""
        return self.__class__(self.x, self.y, self.z)

    def distance(self, other: "Vector") -> float:
        """Returns the distance between two vectors."""
        return (self - other).magnitude()


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
        super().__init__(x, y, z)
