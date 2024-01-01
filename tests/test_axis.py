from src.axis import Axis
from src.pivot import Pivot

import  pytest 


def test_Axis_get_d():
    a = Axis(length=5, rotation=20, pivot=Pivot.Z)
    b = Axis(length=2, rotation=45, pivot=Pivot.Z, anchor=a)
    b.get_right_angle_side()


def test_Axis_calc_c():
    a = Axis(length=5, rotation=20, pivot=Pivot.Z)
    b = Axis(length=2, rotation=45, pivot=Pivot.Z, anchor=a)
    x, y = b.calculate_action_plane_coords()
    
    assert x ==  pytest.approx(3.85, abs=0.005)
    assert y == pytest.approx(-0.1, abs=0.005)


def test_Axis_calc_c2():
    a = Axis(length=5, rotation=20, pivot=Pivot.Z)
    b = Axis(length=10, rotation=70, pivot=Pivot.Z, anchor=a)
    x, y = b.calculate_action_plane_coords()
    
    assert x ==  pytest.approx(4.7, abs=0.005)
    assert y == pytest.approx(-8.29, abs=0.005)
