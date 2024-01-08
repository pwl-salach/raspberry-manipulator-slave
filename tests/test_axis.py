from src.axis import Axis
from src.pivot import Pivot
from src.point import Point
import pytest


def assert_point_equal(actual: Point, expected: Point):
    assert actual.x ==  pytest.approx(expected.x, abs=0.005)
    assert actual.y ==  pytest.approx(expected.y, abs=0.005)
    assert actual.z ==  pytest.approx(expected.z, abs=0.005)


def test_Axis():
    a = Axis(length=0, rotation=45, pivot=Pivot.Z)
    assert_point_equal(a.apex, Point(0, 0, 0))
    
    b = Axis(length=5.5, rotation=45, pivot=Pivot.Y, anchor=a)
    assert_point_equal(b.apex, Point(2.75, 2.75, 3.89))

    c = Axis(length=1.9, rotation=55, pivot=Pivot.Y, anchor=b)
    assert_point_equal(c.apex, Point(2.98, 2.98, 2.02))
