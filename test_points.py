
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
    parser.parse()
    print('1.', parser.dia_points)
    print('2.', parser.regular_points)