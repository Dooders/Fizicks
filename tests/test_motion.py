import pytest

from fizicks.data import Force, Position, Vector, Velocity
from fizicks.matter import Matter
from fizicks.motion import FirstLaw, Motion, SecondLaw, ThirdLaw
from fizicks.universe import Universe


class TestMotion:
    def test_first_law(self):
        obj = Matter(Position(0, 0, 0), Velocity(0, 0, 0), 1.0, 1.0)
        force = Force(1, 1, 1)
        FirstLaw.apply(obj, force)
        assert obj.velocity == Velocity(1, 1, 1)

    def test_second_law(self):
        obj = Matter(Position(0, 0, 0), Velocity(1, 1, 1), 1.0, 1.0)
        SecondLaw.apply(obj, Universe())
        assert obj.position == Position(1, 1, 1)

    def test_third_law(self):
        obj = Matter(Position(0, 0, 0), Velocity(0, 1, 1), 2.0, 1.0)
        ThirdLaw.apply(obj)
        obj.update(Universe())
        assert obj.acceleration == Velocity(0, 0, 0)

    def test_motion_update(self):
        obj = Matter(Velocity(0, 0, 0), Position(0, 0, 0), 1.0, 1.0)
        obj.debt = [Force(1, 1, 1), Force(2, 2, 2)]
        Motion.update(obj, Universe(dimensions=Vector(10, 10, 10), toroidal=True))

        assert obj.velocity == Velocity(3, 3, 3)
        assert obj.position == Position(3, 3, 3)
