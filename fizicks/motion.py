from typing import TYPE_CHECKING, Any

from fizicks.collision import Collision

if TYPE_CHECKING:
    from fizicks.data import Force
    from fizicks.matter import Matter
    from fizicks.universe import Universe


class FirstLaw:
    """An object in motion will remain in motion unless acted on by an external force."""

    @classmethod
    def apply(cls, object: "Matter", force: "Force", debug: bool = False) -> None:
        """
        Updates the velocity of the object based on the force applied.

        Parameters
        ----------
        object : Matter
            The object to apply the force to.
        force : Force
            The force to apply to the object.
        debug : bool
            Whether to print debug information.
        """
        if debug:
            debug_log(
                f"Step {object.time}: Applying force: {force} to {object.id}", object
            )
        object.velocity = object.velocity + force
        if debug:
            debug_log(f"Updated velocity: {object.velocity}", object)


class SecondLaw:
    """The acceleration of an object is directly proportional to the net force acting on it and inversely proportional to its mass."""

    @classmethod
    def apply(cls, object: "Matter", universe: "Universe", debug: bool = False) -> None:
        """
        Updates the position of the object based on the velocity.

        Parameters
        ----------
        object : Matter
            The object to apply the force to.
        universe : Universe
            The universe to apply the force to.
        debug : bool
            Whether to print debug information.
        """
        if debug:
            debug_log(
                f"Step {object.time}: Applying force: {object.velocity} to {object.id}",
                object,
            )

        object.position = object.position + object.velocity
        if debug:
            debug_log(f"Updated position: {object.position}", object)

        if Collision.detect(object, universe):
            Collision.resolve(object, universe)


class ThirdLaw:
    """For every action, there is an equal and opposite reaction."""

    @classmethod
    def apply(cls, object: "Matter", debug: bool = False) -> None:
        """
        Updates the acceleration of the object based on the velocity and mass.

        Parameters
        ----------
        object : Matter
            The object to apply the force to.
        debug : bool
            Whether to print debug information.
        """
        if debug:
            debug_log(
                f"Step {object.time}: Applying force: {object.velocity / object.mass} to {object.id}",
                object,
            )
        object.acceleration = object.velocity / object.mass
        if debug:
            debug_log(f"Updated acceleration: {object.acceleration}", object)


class Motion:
    """
    The motion of an object is determined by the sum of its forces and the net force acting on it.

    Motion process:
    1. Check for collisions with objects or boundaries.
    2. Apply the forces to the object.
    3. Update the object's state based on the forces applied and its current state.
    """

    @classmethod
    def update(cls, object: Any, universe: "Universe", debug: bool = False) -> None:
        """
        Updates the object based on the forces applied and its current state.

        Parameters
        ----------
        object : Any
            The object to update.
        universe : Universe
            The universe to update the object in.
        debug : bool
            Whether to print debug information.
        """
        # Check for collisions with the universe
        if Collision.detect(object, universe):
            if debug:
                debug_log(
                    f"Step {object.time}: Collision detected between {object.id} and {universe.id}",
                    object,
                )
            Collision.resolve(object, universe)

        # Apply the forces of motion
        if object.debt:
            if debug:
                debug_log(
                    f"Step {object.time}: Applying forces for {object.id}", object
                )
            for debt in object.debt:
                FirstLaw.apply(object, debt, debug=debug)
        SecondLaw.apply(object, universe, debug=debug)
        ThirdLaw.apply(object, debug=debug)
