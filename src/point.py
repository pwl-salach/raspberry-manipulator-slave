from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float
    z: float

    def __add__(self, other):
        return Point(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z
        )

    def __sub__(self, other):
        return Point(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z
        )
