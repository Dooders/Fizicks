from typing import Any, List

import pygame

from fizicks.collision import Collision
from fizicks.data import Vector
from fizicks.motion import Motion


class Object:
    def __init__(
        self,
        position: Vector,
        velocity: Vector,
        mass: float,
        radius: float,
        color: tuple,
    ):
        self.position = position
        self.velocity = velocity
        self.mass = mass
        self.radius = radius
        self.color = color
        self.debt = []


class SpatialPartitioning:
    """Handles spatial partitioning to optimize collision detection."""

    def __init__(self, space: "Space", cell_size: float):
        self.space = space
        self.cell_size = cell_size
        self.grid = {}

    def add_object(self, obj: "Object"):
        cell = self._get_cell(obj.position)
        if cell not in self.grid:
            self.grid[cell] = []
        self.grid[cell].append(obj)

    def _get_cell(self, position: "Vector"):
        return (int(position.x / self.cell_size), int(position.y / self.cell_size))

    def get_nearby_objects(self, obj: "Object"):
        cell = self._get_cell(obj.position)
        nearby_objects = []
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                neighbor_cell = (cell[0] + dx, cell[1] + dy)
                if neighbor_cell in self.grid:
                    nearby_objects.extend(self.grid[neighbor_cell])
        return nearby_objects

    def clear(self):
        self.grid.clear()


class ImprovedMotionWithCollision(Motion):
    """Extends Motion to include optimized collision detection and resolution using spatial partitioning."""

    @classmethod
    def update(
        cls, object: Any, space: "Space", partitioning: SpatialPartitioning
    ) -> None:
        """
        Updates the object based on the forces applied, its current state, and resolves collisions.
        """
        super().update(object, space)

        # Check for collisions with other objects in nearby cells
        nearby_objects = partitioning.get_nearby_objects(object)
        for other_object in nearby_objects:
            if other_object is not object and Collision.detect_objects(
                object, other_object
            ):
                Collision.resolve_objects(object, other_object)

        # Check for collisions with the borders of the space
        if Collision.detect_border(object, space):
            Collision.resolve_border(object, space)


class Space:
    def __init__(self, dimensions: Vector, toroidal: bool = False):
        self.dimensions = dimensions
        self.toroidal = toroidal
        self.has_boundaries = not toroidal  # Add this line
        self.objects = []


class SimulationConfig:
    def __init__(
        self, restitution: float = 1.0, friction: float = 0.0, cell_size: float = 50.0
    ):
        self.restitution = restitution
        self.friction = friction
        self.cell_size = cell_size


class VisualDebugger:
    def __init__(self, space: Space, objects: List[Object], config: SimulationConfig):
        self.space = space
        self.objects = objects
        self.config = config

        # Pygame initialization
        pygame.init()
        self.screen = pygame.display.set_mode(
            (int(space.dimensions.x), int(space.dimensions.y))
        )
        pygame.display.set_caption("Physics Simulation Debugger")
        self.clock = pygame.time.Clock()

    def draw_object(self, obj: Object):
        pygame.draw.circle(
            self.screen,
            obj.color,
            (int(obj.position.x), int(obj.position.y)),
            int(obj.radius),
        )

    def draw_border(self):
        pygame.draw.rect(
            self.screen,
            (255, 255, 255),
            pygame.Rect(
                0, 0, int(self.space.dimensions.x), int(self.space.dimensions.y)
            ),
            1,
        )

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill((0, 0, 0))  # Clear screen with black

            # Update simulation
            partitioning = SpatialPartitioning(self.space, self.config.cell_size)
            for obj in self.objects:
                partitioning.add_object(obj)
            for obj in self.objects:
                ImprovedMotionWithCollision.update(obj, self.space, partitioning)
            partitioning.clear()

            # Draw borders and objects
            self.draw_border()
            for obj in self.objects:
                self.draw_object(obj)

            pygame.display.flip()
            self.clock.tick(60)  # Cap the frame rate at 60 FPS

        pygame.quit()


# Example usage
space = Space(Vector(800, 600))  # Create a space of 800x600
objects = [
    Object(Vector(100, 100), Vector(2, 3), mass=1, radius=15, color=(255, 0, 0)),
    Object(Vector(200, 200), Vector(-2, -3), mass=1, radius=15, color=(0, 255, 0)),
    Object(Vector(300, 300), Vector(3, 2), mass=1, radius=15, color=(0, 0, 255)),
]

config = SimulationConfig(restitution=0.8, friction=0.1, cell_size=50.0)

debugger = VisualDebugger(space, objects, config)
debugger.run()
