from src.manipulator import Manipulator
from .base import ControlsHandler

from sys import exit


class CliControlsHandler(ControlsHandler):
    
    def __init__(self, manipulator: Manipulator) -> None:
        self._manipulator = manipulator
    
    def listen_for_input(self):
        print("Control robot by using inputs:")
        print("\t- w - forward")
        print("\t- s - backward")
        print("\t- a - left")
        print("\t- d - right")
        print("\t- r - up")
        print("\t- f - down")
        try:
            while True:
                self.handle_input(input())
        except KeyboardInterrupt:
            exit(0)
    
    def handle_input(self, control: str):
        dx = 0
        dy = 0
        dz = 0
        speed = 1
        if len(control) != 1:
            return
        elif control == 'w':
            dx = speed
        elif control == 's':
            dx = -speed
        elif control == 'a':
            dy = speed
        elif control == 'd':
            dy = -speed
        elif control == 'r':
            dz = speed
        elif control == 'f':
            dz = -speed
        self._manipulator.move_effector(dx, dy, dz)
        print(self._manipulator)
