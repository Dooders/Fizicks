import pytest

from fizicks.data import Force, Position, Velocity
from fizicks.matter import Matter
from fizicks.universe import Universe


class TestMatter:
    def test_matter_creation(self):
        matter = Matter(Position(0, 0, 0), Velocity(0, 0, 0), 1, 1)
        assert matter.position == Position(0, 0, 0)
        assert matter.velocity == Velocity(0, 0, 0)
        assert matter.mass == 1
        assert matter.radius == 1
        assert matter.debt == []

    def test_matter_apply_force(self):
        matter = Matter(Position(0, 0, 0), Velocity(0, 0, 0), 1, 1)
        force = Force(1, 2, 3)
        matter.add_debt(force)
        matter.update(Universe())
        assert matter.velocity == Velocity(1, 2, 3)

        # Apply another force
        second_force = Force(2, 1, -1)
        matter.add_debt(second_force)
        matter.update(Universe())
        assert matter.velocity == Velocity(3, 3, 2)

        # Check the position
        assert matter.position == Position(5, 6, 5)

        # Check that mass and radius remain unchanged
        assert matter.mass == 1
        assert matter.radius == 1

    def test_matter_apply_force_with_debt(self):
        matter = Matter(Position(0, 0, 0), Velocity(0, 0, 0), 1, 1)
        force = Force(1, 1, 1)
        matter.add_debt(force)
        matter.update(Universe())
        assert matter.velocity == Velocity(1, 1, 1)

    def test_matter_update(self):
        matter = Matter(Position(0, 0, 0), Velocity(0, 0, 0), 1, 1)
        matter.update(Universe())
        assert matter.position == Position(1, 1, 0)

    def test_matter_update_with_debt(self):
        matter = Matter(Position(0, 0, 0), Velocity(0, 0, 0), 1, 1)
        force = Force(1, 1, 1)
        matter.add_debt(force)
        matter.update(Universe())
        assert matter.position == Position(2, 2, 1)
