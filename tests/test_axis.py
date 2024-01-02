from src.axis import Axis
from src.pivot import Pivot

import pytest


@pytest.mark.parametrize(
    "rotation_z, expected_x, expected_y",
    [
        (70, 4.7, -8.29),
        (290, -1.73, 9.37),
        (150, 14.55, -0.03),
        (210, 11.13, 9.37)
    ]
)
def test_Axis_calculate_action_plane_coords(rotation_z, expected_x, expected_y):
    a = Axis(length=5, rotation=20, pivot=Pivot.Z)
    b = Axis(length=10, rotation=rotation_z, pivot=Pivot.Z, anchor=a)
    x, y = b.calculate_action_plane_coords()
    
    assert x ==  pytest.approx(expected_x, abs=0.005)
    assert y == pytest.approx(expected_y, abs=0.005)
