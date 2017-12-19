
import pytest

from proc.points import Parser, inverse_intervals, IdempTransformer

@pytest.fixture()
def parser():
    text = '''\
X1 text Z1 text X4 Z-3 R.5 F400
'''
    return Parser(text)


class _Transformer(IdempTransformer):

    def handle_dia(self, prev, p):
        d = self.get_diagonal(prev, p)
        assert d == 5


def test_change(parser):
    points = parser.parse()
    tr = _Transformer(points)
    tr.run()
