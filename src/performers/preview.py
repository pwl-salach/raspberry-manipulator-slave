from src.performers.base import Performer

import numpy as np
from matplotlib import pyplot as plt


class Preview(Performer):

    def __init__(self):
        self.max_length = 0

    def __enter__(self):
        plt.xticks(np.arange(self.max_length - 1, self.max_length + 1, 2))
        plt.yticks(np.arange(self.max_length, self.max_length + 1, 2))
        plt.ion()
        plt.show()

    def __exit__(self, exc_type, exc_value, traceback):
        plt.ioff() 
        plt.close()

    def update(self, **kwargs):
        points = kwargs['points']
        ax = plt.axes(projection='3d')

        x_values = [point.x for point in points]
        y_values = [point.y for point in points]
        z_values = [point.z for point in points]
        ax.scatter3D(x_values, y_values, z_values)
        ax.plot3D(x_values, y_values, z_values, 'b-')
        plt.draw()
        plt.pause(0.01)