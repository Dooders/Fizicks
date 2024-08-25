import unittest

from fizicks.collision import Collision
from fizicks.data import Position, Vector
from fizicks.matter import Matter
from fizicks.universe import Universe


class TestCollision(unittest.TestCase):
    def setUp(self):
        self.universe = Universe(toroidal=True)
        self.object1 = Matter(Vector(10, 10), Vector(1, 0), 5, 10)
        self.object2 = Matter(Vector(20, 10), Vector(-1, 0), 5, 10)

    def test_detect_objects_collision(self):
        self.assertTrue(Collision.detect(self.object1, self.object2))

    def test_detect_objects_no_collision(self):
        self.object2.position = Position(50, 50, 0)
        self.assertFalse(Collision.detect(self.object1, self.object2))

    def test_detect_border_collision(self):
        self.universe.toroidal = False
        self.object1.position = Position(-1, 10, 0)
        self.assertTrue(Collision.detect(self.object1, self.universe))

    def test_detect_no_border_collision(self):
        self.assertFalse(Collision.detect(self.object1, self.universe))

    def test_resolve_objects_collision(self):
        initial_v1 = self.object1.velocity.copy()
        initial_v2 = self.object2.velocity.copy()
        self.assertTrue(Collision.detect(self.object1, self.object2))
        Collision.resolve(self.object1, self.object2)
        self.object1.update(self.universe)
        self.object2.update(self.universe)
        self.assertNotEqual(initial_v1, self.object1.velocity)
        self.assertNotEqual(initial_v2, self.object2.velocity)

    def test_resolve_border_collision_toroidal(self):
        self.object1.position = Position(-1, 10, 0)
        Collision.resolve(self.object1, self.universe)
        self.object1.update(self.universe)
        self.assertEqual(self.object1.position, Position(0, 10, 0))

    def test_resolve_border_collision_non_toroidal(self):
        self.universe.toroidal = False
        self.object1.position = Position(101, 10, 0)
        Collision.resolve(self.object1, self.universe)
        self.object1.update(self.universe)
        self.assertEqual(self.object1.position, Position(89, 10, 0))

    def test_detect_objects_private(self):
        self.assertTrue(Collision._detect_objects(self.object1, self.object2))

    def test_detect_border_private(self):
        self.object1.position = Position(-1, 10, 0)
        self.universe.toroidal = False
        self.assertTrue(Collision._detect_border(self.object1, self.universe))

    def test_resolve_border_private(self):
        self.object1.position = Position(101, 10, 0)
        Collision._resolve_border(self.object1, self.universe)
        self.assertEqual(self.object1.position, Position(0, 10, 0))


if __name__ == "__main__":
    unittest.main()
