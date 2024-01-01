from ..manipulator import Manipulator
from ..point import Point
from typing import List
from matplotlib import pyplot as plt
from math import floor
import numpy as np


class Preview:

    def visualize_in_3d(self, manipulator: Manipulator):
        fig = plt.figure()
        ax = plt.axes(projection='3d')

        points: List[Point] = manipulator.get_joints_coords()
        x_values = [point.x for point in points]
        y_values = [point.y for point in points]
        z_values = [point.z for point in points]
        ax.scatter3D(x_values, y_values, z_values)
        ax.plot3D(x_values, y_values, z_values, 'b-')
        
        min_val = floor(min(*x_values, *y_values, *z_values))
        max_val = round(max(*x_values, *y_values, *z_values))

        plt.xticks(np.arange(min_val - 1, max_val + 1, 2))
        plt.yticks(np.arange(min_val - 1, max_val + 1, 2))

        fig.add_axes(ax)
        plt.show()
