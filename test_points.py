
import pytest

from proc.points import Parser

@pytest.fixture()
def parser():
    text = '''\
X23 Z-5 R.5 F400
X.3 X.4 some text
X1 Z-2 R1 F100
'''
    return Parser(text)


def test_parser(parser):
    points = parser.parse()
    assert len(parser.dia_points) == 2
    assert len(parser.regular_points) == 2
    assert {p['X'] for p in points} == {'23', '.3', '.4', '1'}