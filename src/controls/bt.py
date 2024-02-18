import serial
import time
from src.controls.base import ControlsHandler
from src.manipulator import Manipulator


class BtControlsHandler(ControlsHandler):

    def __init__(self, manipulator: Manipulator) -> None:
        self._manipulator = manipulator
        self._serial = serial.Serial(
            port='/dev/ttyAMA0',
            baudrate=9600,
            # parity=serial.PARITY_ODD,
            # stopbits=serial.STOPBITS_TWO,
            # bytesize=serial.SEVENBITS
        )
        self._run = True

    def listen_for_input(self) -> None:
        while self._run:
            recv = self._serial.readline()
            if recv:
                self.handle_input(recv.decode())
            


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