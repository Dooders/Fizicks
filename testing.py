from fizicks.data import Vector
from fizicks.matter import Matter
from fizicks.universe import Universe
from fizicks.visual import VisualDebugger

# Example usage
universe = Universe(dimensions=Vector(800, 600), toroidal=False)
objects = [
    Matter(
        position=Vector(100, 300),
        velocity=Vector(3, 1),
        mass=1,
        radius=15,
        color=(255, 0, 0),
    ),
    Matter(
        position=Vector(700, 300),
        velocity=Vector(-3, 0),
        mass=1,
        radius=15,
        color=(0, 255, 0),
    ),
    Matter(
        position=Vector(300, 300),
        velocity=Vector(3, 2),
        mass=1,
        radius=15,
        color=(0, 0, 255),
    ),
]
universe.objects = objects

debugger = VisualDebugger(universe, objects)
debugger.run()
