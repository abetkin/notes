
import pytest

from proc.points import Parser, inverse_intervals

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

def test_inverse():
    points = [
        {'start': 1, 'end': 2},
        {'start': 3, 'end': 4},
    ]
    upper = 6
    r = inverse_intervals(points, upper)
    assert r == [(0, 1), (2, 3), (4, 5)]

def test_no_change(parser):
    points = parser.parse()
    text = parser.render()
    print(text)
    print()
    print()
    assert parser.text == text

def test_cut(parser):
    text = parser.text
    li = []
    points = [
        p for p in parser.parse()
        if p.get('is_dia')
    ]
    for start, end in inverse_intervals(points, len(text)):
        li.append(
            text[start:end]
        )
    new_text = ''.join(li)
    assert new_text.strip() == "X.3 X.4 some text"