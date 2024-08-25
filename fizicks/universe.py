import uuid
from abc import ABC, abstractmethod

from fizicks.data import Vector


class FizicksObject(ABC):
    def __init__(self, **kwargs) -> None:
        self.id = uuid.uuid4()
        self.time = 0
        self.debug = kwargs.get("debug", False)

    @abstractmethod
    def description(self, short: bool = True) -> str:
        raise NotImplementedError("Subclass must implement a description method")


class Universe(FizicksObject):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.id = "Universe"
        self.dimensions = kwargs.get("dimensions", Vector(100, 100, 100))
        self.toroidal = kwargs.get("toroidal", False)
        self.gravity = kwargs.get("gravity", Vector(0, 0, 0))
        self.c = kwargs.get("c", 1)
        self.viscosity = kwargs.get("viscosity", 0)
        self.restitution = kwargs.get("restitution", 1)
        self.friction = kwargs.get("friction", 0)
        self.air_resistance = kwargs.get("air_resistance", 0)
        self.air_resistance_coefficient = kwargs.get("air_resistance_coefficient", 0)
        self.air_resistance_area = kwargs.get("air_resistance_area", 0)
        self.air_resistance_density = kwargs.get("air_resistance_density", 0)
        self.objects = []

    def description(self, short: bool = True) -> str:
        if short:
            return f"Universe(id={self.id})"
        else:
            return f"Universe(id={self.id}, time={self.time}, dimensions={self.dimensions}, toroidal={self.toroidal}, gravity={self.gravity})"
