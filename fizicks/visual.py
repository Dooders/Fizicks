from typing import Any, List

import pygame

from fizicks.collision import Collision


class VisualDebugger:
    """
    A class for visualizing the universe and objects for debugging purposes.

    Uses Pygame to visualize the universe and objects.

    Parameters
    ----------
    universe: Universe
        The universe to visualize.
    objects: List[Matter]
        The objects to visualize.
    """

    def __init__(self, universe: "Universe", objects: List["Matter"]):
        self.universe = universe
        self.objects = objects

        # Pygame initialization
        pygame.init()
        self.screen = pygame.display.set_mode(
            (int(universe.dimensions.x), int(universe.dimensions.y))
        )
        pygame.display.set_caption("Fizicks Visual Debugger")
        self.clock = pygame.time.Clock()

    def draw_object(self, obj: "Matter") -> None:
        """
        Draws an object on the screen.

        Parameters
        ----------
        obj: Matter
            The object to draw.
        """
        pygame.draw.circle(
            self.screen,
            obj.color,
            (int(obj.position.x), int(obj.position.y)),
            int(obj.radius),
        )

    def draw_border(self) -> None:
        """
        Draws the border of the universe on the screen.
        """
        pygame.draw.rect(
            self.screen,
            (255, 255, 255),
            pygame.Rect(
                0, 0, int(self.universe.dimensions.x), int(self.universe.dimensions.y)
            ),
            1,
        )

    def run(self) -> None:
        """
        Runs the simulation and visualizes the universe and objects.
        """
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill((0, 0, 0))  # Clear screen with black

            self.draw_border()

            # Identify collisions
            for i, obj in enumerate(self.objects):
                for other_obj in self.objects[i + 1 :]:
                    if obj.collides_with(other_obj):
                        Collision.resolve(obj, other_obj)

            for obj in self.objects:
                obj.update(self.universe)
                self.draw_object(obj)

            self.universe.time += 1

            pygame.display.flip()
            self.clock.tick(60)  # Cap the frame rate at 60 FPS

        pygame.quit()
