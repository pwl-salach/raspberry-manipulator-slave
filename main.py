from sys import argv
from src.manipulator import Manipulator
from src.controls.cli import CliControlsHandler
from src.controls.bt import BtControlsHandler


def main():
    if len(argv) and argv[0] == "--preview":
        from src.performers.preview import Preview
        preview = Preview()
    else:
        from src.performers.i2c import I2C
        preview = I2C()
    robot = Manipulator(preview)
    robot.move_effector(0, 0, 0)
    preview.max_length = sum([it.length for it in robot.arm_structure])

    control = BtControlsHandler(robot)
    with preview as ctx:
        control.listen_for_input()


if __name__ == '__main__':
    main()
