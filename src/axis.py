from .pivot import Pivot
from .point import Point

from math import cos, sin, radians, atan2, sqrt
from typing import Optional, Tuple


class Axis:

    def __init__(self, length: float, rotation: float,
                 pivot: Pivot, anchor: Optional["Axis"] = None)-> None:
        self.length = length
        self._rotation = rotation
        self.pivot = pivot
        self.anchor = anchor
        self.root = anchor.apex if anchor else Point(0, 0, 0)
        # initial calculation of apex
        # later it will be recalculated in setter of rotation
        self.apex: Point = self.calculate_apex()    

    @property
    def rotation(self) -> float:
        return self._rotation
    
    @rotation.setter
    def rotation(self, value: float) -> None:
        self._rotation = value if value < 360 else value - 360
        self.apex = self.calculate_apex()

    def get_anchor_coord(self, axis):
        if self.anchor:
            return getattr(self.anchor.apex, axis)
        return 0
    
    def get_anchor_root_coord(self, axis):
        if self.anchor:
            return getattr(self.anchor.root, axis)
        return 0

    def __repr__(self) -> str:
        return f"Apex: {self.apex}, Current rotation: {self.rotation}"

    def get_right_angle_side(self) -> Point:
        xa = self.get_anchor_root_coord('x')
        ya = self.get_anchor_root_coord('y')
        za = self.get_anchor_root_coord('z')

        xb = self.get_anchor_coord('x')
        yb = self.get_anchor_coord('y')
        zb = self.get_anchor_coord('z')

        l = self.length * cos(radians(self.rotation))
        try:
            proportion = l / sqrt((xa - xb)**2 + (ya - yb)**2 + (za - zb)**2)
        except ZeroDivisionError:
            proportion = 0
        return Point(
            xb + (xa - xb) * proportion,
            yb + (ya - yb) * proportion,
            zb + (za - zb) * proportion
        )
    
    def move_by(self, dx: float, dy: float, dz: float) -> None:
        self.apex.x += dx
        self.apex.y += dy
        self.apex.z += dz

    # I am using Point class to represent vectors, as it is convenient
    def normalize_vector(self, vec) -> Point:
        length = sum(v**2 for v in vars(vec).values())**0.5
        return Point(**{k: v / length for k, v in vars(vec).items()})

    def calculate_plane_vector(self, axis_vector: Point, neutral_vector: Point) -> Point:
        return Point(
            axis_vector.y * neutral_vector.z - axis_vector.z * neutral_vector.y,
            axis_vector.z * neutral_vector.x - axis_vector.x * neutral_vector.z,
            axis_vector.x * neutral_vector.y - axis_vector.y * neutral_vector.x
        )

    def calculate_apex(self) -> Point:
        # current expected manipulatr structure makes it constant
        origin = Point(0, 0, 0)
        neutral_vector = Point(0, 0, 1)
        init_point = self.anchor.root if self.anchor else Point(0, 0, 0)
        if init_point == origin and self.root == origin:
            if not self.anchor:
                return Point(0, 0, 0)
            z = self.length * sin(radians(self.rotation))
            xy = self.length * cos(radians(self.rotation))
            x = xy * cos(radians(self.anchor.rotation))
            y = xy * sin(radians(self.anchor.rotation))
            return Point(x, y, z)
        axis_vector = self.normalize_vector(self.root - init_point)
        plane_vector = self.normalize_vector(self.calculate_plane_vector(axis_vector, neutral_vector))
        shift_vector = self.calculate_plane_vector(axis_vector, plane_vector)
        c = self.get_right_angle_side()
        l = self.length * sin(radians(self.rotation))
        # shift_vector might be pointing in wrong direction
        return Point(
            c.x + l * shift_vector.x,
            c.y + l * shift_vector.y,
            c.z + l * shift_vector.z
        )
