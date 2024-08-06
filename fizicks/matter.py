from fizicks.data import Area, Force, Position, Velocity


class Matter:
    def __init__(
        self, position: "Position", velocity: "Velocity", mass: float, radius: float
    ) -> None:
        self.position = position
        self.velocity = velocity
        self.mass = mass
        self.radius = radius
        self.debt = []

    def apply_force(self, force: "Force") -> None:
        """
        Apply a force to the object.

        Parameters
        ----------
        force : Force
            The force to apply to the object.
        """
        self.debt.append(force / self.mass)  # Accumulate acceleration (force / mass)

    def update(self, area: "Area") -> None:
        """
        Update the object's state based on accumulated forces and current state.

        Parameters
        ----------
        area : Area
            The area to update the object in.
        """
        for force in self.debt:
            self.velocity = self.velocity + force
        self.position = self.position + self.velocity
        if area.has_boundaries:
            self.position = self.position % area.dimensions
        self.debt = []  # Clear forces after applying

    def detect_collision_with_border(self, area: "Area") -> bool:
        """
        Detect if the object has collided with the borders of the area.

        Parameters
        ----------
        area : Area
            The area to detect collisions in.

        Returns
        -------
        bool
            True if the object has collided with the borders of the area, False otherwise.
        """
        for i in range(len(self.position)):
            if (
                self.position[i] - self.radius < 0
                or self.position[i] + self.radius > area.dimensions[i]
            ):
                return True
        return False

    def resolve_collision_with_border(
        self, area: "Area", restitution: float = 1.0
    ) -> None:
        """
        Resolve the collision with the borders of the space.

        Parameters
        ----------
        area : Area
            The area to resolve collisions in.
        restitution : float, optional
            The coefficient of restitution (default is 1.0).
            Used to determine the amount of energy lost in the collision.
            1.0 means no energy is lost.
        """
        for i in range(len(self.position)):
            if self.position[i] - self.radius < 0:
                self.position[i] = self.radius
                self.velocity[i] = -self.velocity[i] * restitution
            elif self.position[i] + self.radius > area.dimensions[i]:
                self.position[i] = area.dimensions[i] - self.radius
                self.velocity[i] = -self.velocity[i] * restitution
