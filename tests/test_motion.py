import pytest

from fizicks.main import (
    FirstLaw,
    Force,
    Motion,
    Position,
    SecondLaw,
    ThirdLaw,
    Vector,
    Velocity,
)


class MockObject:
    def __init__(self, velocity: Vector, position: Vector, mass: float):
        self.velocity = velocity
        self.position = position
        self.mass = mass


def test_vector_addition():
    v1 = Vector(1, 2, 3)
    v2 = Vector(4, 5, 6)
    result = v1 + v2
    assert result == Vector(5, 7, 9)


def test_vector_subtraction():
    v1 = Vector(4, 5, 6)
    v2 = Vector(1, 2, 3)
    result = v1 - v2
    assert result == Vector(3, 3, 3)


def test_vector_multiplication():
    v = Vector(1, 2, 3)
    result = v * 3
    assert result == Vector(3, 6, 9)


def test_vector_division():
    v = Vector(3, 6, 9)
    result = v / 3
    assert result == Vector(1, 2, 3)


def test_first_law():
    obj = MockObject(Velocity(1, 2, 3), Position(0, 0, 0), 1.0)
    force = Force(1, 1, 1)
    FirstLaw.apply(obj, force)
    assert obj.velocity == Velocity(2, 3, 4)


def test_second_law():
    obj = MockObject(Velocity(1, 2, 3), Position(0, 0, 0), 1.0)
    SecondLaw.apply(obj)
    assert obj.position == Position(1, 2, 3)


def test_third_law():
    obj = MockObject(Velocity(1, 2, 3), Position(0, 0, 0), 2.0)
    ThirdLaw.apply(obj)
    assert obj.acceleration == Velocity(0, 1, 1)


def test_motion_update():
    obj = MockObject(Velocity(1, 2, 3), Position(0, 0, 0), 1.0)
    obj.debt = [Force(1, 1, 1), Force(2, 2, 2)]
    Motion.update(obj)

    assert obj.velocity == Velocity(4, 5, 6)
    assert obj.position == Position(4, 5, 6)
