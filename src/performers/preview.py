from src.performers.base import Performer

import numpy as np
from matplotlib import pyplot as plt


class Preview(Performer):

    def __init__(self):
        self.max_length = 0

    def __enter__(self):
        plt.ion()
        plt.show()

    def __exit__(self, exc_type, exc_value, traceback):
        plt.ioff() 
        plt.close()

    def update(self, **kwargs):
        points = kwargs['points']
        x_values = [point.x for point in points]
        y_values = [point.y for point in points]
        z_values = [point.z for point in points]

        ax = plt.axes(projection='3d')
        ax.scatter3D(x_values, y_values, z_values)
        ax.plot3D(x_values, y_values, z_values, 'b-')

        ax.set_xticks(np.arange(-self.max_length, self.max_length + 1, 10))
        ax.set_yticks(np.arange(-self.max_length, self.max_length + 1, 10))
        ax.set_zticks(np.arange(0, self.max_length + 1, 10))
        ax.view_init(elev=0, azim=90)

        for x, y, z in zip(x_values, y_values, z_values):
            text = str(round(x, 1)) + ', ' + str(round(y, 1)) + ', ' + str(round(z, 1))
            ax.text(x, y, z, text, zdir=(1, 1, 1))
        plt.draw()
        plt.pause(0.01)