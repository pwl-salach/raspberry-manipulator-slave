from src.manipulator import Manipulator
from src.controls.cli import CliControlsHandler
from src.performers.preview import Preview


preview = Preview()
robot = Manipulator(preview)

preview.max_length = sum([it.length for it in robot.arm_structure])

control = CliControlsHandler(robot)
with preview as ctx:
    control.listen_for_input()

# print(robot)
# Preview().visualize_in_3d(robot)
# robot.move_effector(0, 0, 0)
# print(robot)
# Preview().visualize_in_3d(robot)
# robot.move_effector(0, 0, 5)
# Preview().visualize_in_3d(robot)
# robot.move_effector(5, 0, 0)
# Preview().visualize_in_3d(robot)
