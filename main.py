from src.manipulator import Manipulator
from src.controls.cli import CliControlsHandler
from src.preview import Preview


robot = Manipulator()
control = CliControlsHandler(robot)
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
