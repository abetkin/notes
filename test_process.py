import pytest

from proc.points import make_points
from proc.process import Iterator


@pytest.fixture()
def points():
    text = '''\
X23 Z-5 R.5 F400
X.3 X.4 some text
X1 Z-2 R1 F100
'''
    return make_points(text)

def test_0_point(points):
    p = points[0]
    print(p.__dict__)

def test(points):
    it = Iterator(points)