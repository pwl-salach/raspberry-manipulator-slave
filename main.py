from src.manipulator import Manipulator
from src.controls.cli import CliControlsHandler
from src.performers.preview import Preview


preview = Preview()
robot = Manipulator(preview)
robot.move_effector(0, 0, 0)
preview.max_length = sum([it.length for it in robot.arm_structure])

control = CliControlsHandler(robot)
with preview as ctx:
    control.listen_for_input()
