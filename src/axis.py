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

    def calculate_apex(self) -> Point:
        if self.pivot == Pivot.X:
            x =  self.get_anchor_coord('x')
            y, z = self.calculate_action_plane_coords('y', 'z')
        elif self.pivot == Pivot.Y:
            y =  self.get_anchor_coord('y')
            x, z = self.calculate_action_plane_coords('x', 'z')
        elif self.pivot == Pivot.Z:
            z =  self.get_anchor_coord('z')
            x, y = self.calculate_action_plane_coords('x', 'y')
        return Point(x, y, z)

    @property
    def rotation(self) -> float:
        return self._rotation
    
    @rotation.setter
    def rotation(self, value: float) -> None:
        self._rotation = value if value < 360 else 360 - value
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
        return str(self.apex)


    def get_right_angle_side(self, first_plane_coord='x', second_plane_coord='y') -> Tuple[float, float, float]:
        xa = self.get_anchor_root_coord(first_plane_coord)
        ya = self.get_anchor_root_coord(second_plane_coord)
        l = self.length * cos(radians(self.rotation))

        xb = self.get_anchor_coord(first_plane_coord)
        yb = self.get_anchor_coord(second_plane_coord)

        try:
            proportion = l / sqrt((xa - xb)**2 + (ya - yb)**2)
        except ZeroDivisionError:
            proportion = 0
        xd = xb + (xa - xb) * proportion
        yd = yb + (ya - yb) * proportion
        return xd, yd, l
    
    def calculate_action_plane_coords(self, first_plane_coord='x', second_plane_coord='y') -> Tuple[float, float]:
        xa, ya, ab = self.get_right_angle_side(first_plane_coord, second_plane_coord)
        xb = self.get_anchor_coord(first_plane_coord)
        yb = self.get_anchor_coord(second_plane_coord)

        ac = sqrt(self.length**2 - ab**2)
        if xa == 0 and ya == 0 and xb == 0 and yb == 0:
            return ab, ac
        if ab == 0:
            return xa, ya
        if self.rotation < 180:
            xc = xa + ac/ab * (yb - ya)
            yc = ya - ac/ab * (xb - xa)
            return xc, yc
        else:
            xc = xa - ac/ab * (yb - ya)
            yc = ya + ac/ab * (xb - xa)
            return xc, yc

    def move_by(self, dx: float, dy: float, dz: float) -> None:
        self.apex.x += dx
        self.apex.y += dy
        self.apex.z += dz
