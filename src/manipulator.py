# from math import acos, sqrt
from .axis import Axis
from .pivot import Pivot
from .point import Point

from math import acos, sqrt, sin, cos, degrees, radians
from typing import List



class Manipulator:

    def __init__(self) -> None:
        self.rotation_joint = Axis(length=0, rotation=0, pivot=Pivot.Z)
        self.base_joint = Axis(length=20, rotation=90, pivot=Pivot.Y, anchor=self.rotation_joint)
        self.elbow_joint = Axis(length=15, rotation=120, pivot=Pivot.Y, anchor=self.base_joint)
        self.wrist_joint = Axis(length=8, rotation=90 + 30, pivot=Pivot.Y, anchor=self.elbow_joint)
        self.arm_structure = [
            self.rotation_joint,
            self.base_joint,
            self.elbow_joint,
            self.wrist_joint
        ]
        self.effector = Axis(0, rotation=90, pivot=Pivot.X, anchor=self.wrist_joint)
        self.approach_angle = 30

    def get_joints_coords(self) -> List[Point]:
        return [it.apex for it in self.arm_structure if it.apex]

    def __repr__(self) -> str:
        new_line = '\n\t'
        return f"Manipulator: {new_line}{new_line.join([str(it) for it in self.arm_structure])}"

    def move_effector(self, dx: float, dy: float, dz: float) -> bool:
        self.effector.move_by(dx, dy, dz)
        possible_settinges = [
            round(it - int(it/360) * 360) 
            for it in self.calculate_potential_joints_settinges(self.effector.apex)
        ]
        if not possible_settinges:
            self.effector.move_by(-dx, -dy, -dz)
            return False
        else:
            self.rotation_joint.rotation = possible_settinges[0]
            self.base_joint.rotation = possible_settinges[1]
            self.elbow_joint.rotation = possible_settinges[2]
            self.wrist_joint.rotation = possible_settinges[3]
            for joint in self.arm_structure:
                joint.apex = joint.calculate_apex()
        return True

    def calculate_potential_joints_settinges(self, target: Point) -> List[float]:
        h1 = self.base_joint.length
        h2 = self.elbow_joint.length
        h3 = self.wrist_joint.length
        x = target.x
        y = target.y
        z = target.z
        alpha2 = radians(self.approach_angle)

        alpha1 = acos(x/sqrt(x**2 + y**2))
        A = sqrt(x**2 + y**2)
        f = A - h3 * cos(alpha2)
        e = z - h3 * sin(alpha2)
        alpha3 = acos((e**2 + f**2 - h1**2 - h2**2) / (2 * h1 * h2))
        gamma = acos((e**2 + f**2 + h1**2 - h2 ** 2) / (2 * h1 * sqrt(e**2 + f**2)))
        beta =  acos(f / sqrt(e**2 + f**2))
        alpha4 =  beta + gamma
        alpha5 = 90 + alpha4 - alpha2 - alpha3
        return [
            self.reduce_radians(alpha1),
            self.reduce_radians(alpha4),
            180 - self.reduce_radians(alpha3),
            270 - self.reduce_radians(alpha5)
        ]

    def reduce_radians(self, alpha_rad: float) -> float:
        alpha = degrees(alpha_rad)
        return alpha - int(alpha/360) * 360

    def change_approach_angle(self, delta: float) -> None:
        self.wrist_joint.rotation += delta
