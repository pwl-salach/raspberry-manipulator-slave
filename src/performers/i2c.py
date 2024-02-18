import busio

from adafruit_motor.servo import Servo
from adafruit_pca9685 import PCA9685
from board import SCL, SDA

from src.performers.base import Performer


class I2C(Performer):
    
    def __init__(self):
        self.pca = PCA9685(busio.I2C(SCL, SDA))
        self.pca.frequency = 50
        self.servos = []


    def __enter__(self):
        ...

    def __exit__(self, exc_type, exc_value, traceback):
        ...

    def configure(self, **kwargs) -> None:
        for index in range(len(kwargs.get("servos", []))):
            channel = self.pca.channels[index]
            self.servos.append(Servo(channel))  # type: ignore
        if len(self.servos) < 1:
            raise ValueError("Empty structure. Nothing to operate.")

    def update(self, **kwargs):
        angles = kwargs.get("angles", [])
        for servo, angle in zip(self.servos, angles):
            servo.angle = angle
