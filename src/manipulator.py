
from src.axis import Axis
from src.performers.base import Performer
from src.pivot import Pivot
from src.point import Point

from math import acos, sqrt, sin, cos, degrees, radians
from typing import List


class Manipulator:

    def __init__(self, performer: Performer) -> None:
        self.performer = performer
        self.approach_angle = 20
        self.rotation_joint = Axis(length=0, rotation=0, pivot=Pivot.Z)
        self.base_joint = Axis(length=20, rotation=90, pivot=Pivot.Y, anchor=self.rotation_joint)
        self.elbow_joint = Axis(length=15, rotation=120, pivot=Pivot.Y, anchor=self.base_joint)
        self.wrist_joint = Axis(length=8, rotation=150 + self.approach_angle, pivot=Pivot.Y, anchor=self.elbow_joint)
        self.effector = Axis(0, rotation=90, pivot=Pivot.X, anchor=self.wrist_joint)
        self.arm_structure = [
            self.rotation_joint,
            self.base_joint,
            self.elbow_joint,
            self.wrist_joint
        ]

    def get_joints_coords(self) -> List[Point]:
        return [it.apex for it in self.arm_structure if it.apex]

    def __repr__(self) -> str:
        new_line = '\n\t'
        return f"Manipulator: {new_line}{new_line.join([str(it) for it in self.arm_structure])}"

    def move_effector(self, dx: float, dy: float, dz: float) -> bool:
        print(f"Moving effector by: {dx}, {dy}, {dz}")
        self.effector.move_by(dx, dy, dz)
        possible_settings = self.calculate_potential_joints_settings(self.effector.apex)
        if not possible_settings:
            self.effector.move_by(-dx, -dy, -dz)
            return False
        else:
            self.rotation_joint.rotation = possible_settings[0]
            self.base_joint.rotation = possible_settings[1]
            self.elbow_joint.rotation = possible_settings[2]
            self.wrist_joint.rotation = possible_settings[3]
            self.performer.update(points=[it.apex for it in self.arm_structure])
        return True

    def calculate_potential_joints_settings(self, target: Point) -> List[float]:
        h1 = self.base_joint.length
        h2 = self.elbow_joint.length
        h3 = self.wrist_joint.length
        x = target.x
        y = target.y
        z = target.z
        alpha2 = self.approach_angle
        alpha_2_rad = radians(alpha2)

        A = sqrt(x**2 + y**2) # I need La instead of A
        alpha1 = acos(x/A)
        f = A - h3 * cos(alpha_2_rad)
        e = z - h3 * sin(alpha_2_rad)
        alpha3 = acos((h1**2 + h2**2 - e**2 - f**2) / (2 * h1 * h2))
        gamma = acos((e**2 + f**2 + h1**2 - h2 ** 2) / (2 * h1 * sqrt(e**2 + f**2)))
        beta =  acos(f / sqrt(e**2 + f**2))
        alpha4 =  beta + gamma
        alpha1 = self.reduce_radians(alpha1)
        alpha3 = self.reduce_radians(alpha3)
        alpha4 = self.reduce_radians(alpha4)
        alpha5 = 360 - alpha4 - alpha3 + alpha2
        return [
            alpha1,
            alpha4,
            alpha3,
            alpha5
        ]

    def reduce_radians(self, alpha_rad: float) -> float:
        alpha = degrees(alpha_rad)
        return alpha - int(alpha/360) * 360

    def change_approach_angle(self, delta: float) -> None:
        self.wrist_joint.rotation += delta
