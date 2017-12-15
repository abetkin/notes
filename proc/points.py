import re


class Parser:

    SIMPLE_REG = r'([XZ])(-?[\d.]+)'
    DIA_REG = r'X(-?[\d.]+) Z(-?[\d.]+)'

    def __init__(self, text):
        self.text = text

    def parse(self):
        li = self.dia_points = []
        for m in re.finditer(self.DIA_REG, self.text):
            li.append(self.to_dia_point(m))
        # cut dia points from source
        # i.e. replace them with space
        text = self.text
        #
        include_chars = list(range(len(text)))
        for m in li:
            for i in range(m['start'], m['end']):
                include_chars[i] = -1
        text = ''.join(
            text[i] if i != -1 else ' '
            for i in include_chars 
        )
        # now find all simple points
        li = self.regular_points = []
        for m in re.finditer(self.SIMPLE_REG, text):
            li.append(self.to_simple_point(m))

        self.points = sorted(
            self.dia_points + self.regular_points,
            key=lambda p: p['start']
        )
        return self.points

    def to_simple_point(self, match):
        return {
            match.group(1): match.group(2),
            "start": match.start(),
            "end": match.end(),
        }

    def to_dia_point(self, match):
        dic = {
            'X': match.group(1),
            'Z': match.group(2),
            "start": match.start(),
            "end": match.end(),
            "is_dia": True,
        }
        # getting full info:
        # split by spaces
        after_text = self.text[dic['end']:dic['end']+20]
        # chunks = after_text.split()
        # find 1st non-match
        # last_match = None
        reg = r'([RF])(-?[\d.]+)'
        # for i, chunk in enumerate(chunks):
        #     m = re.match(reg, chunk)
        #     if not m:
        #         break
        #     prev = chunks[i-1]
        #     ''.join(chunks[:i]
        #     dic[m.group(1)] = m.group(2)
        # if last_match:
        #     dic['end'] += last_match.end()
        # return dic

        prev_m = None
        for m in re.finditer(reg, after_text):
            if prev_m and after_text[prev_m.end():m.start()].strip():
                break
            prev_m = m
        if prev_m is not None:
            dic['end'] += prev_m.end()
        return dic

    # def _():
    #     reg = r""

    def render(self):
        points = [p for p in self.points if p.get('is_dia')]
        upper = len(self.text)
        intervals = inverse_intervals(points, upper)
        def _render(p):
            return f"X{p['X']} Z{p['Z']} R{p['R']} F{p['F']}"
        li = []
        for (start, end), p in zip(
            intervals,
            points + [None]
        ):
            li.append(self.text[start:end])
            if p is None:
                continue
            li.append(_render(p))
        return ''.join(li)


class DiaCalculator:

    def __init__(self, points):
        self.points = points
        self.state = {}

    def run(self):
        for i, p in enumerate(self.points):

            if not p.get('is_dia'):
                self.state.update(p)
            else:
                self.handle_dia(p, dict(self.state))

    
    def handle_dia(self, p, prev):
        import math
        d = math.sqrt(
            (p['X'] - prev['X']) ** 2 + (p['Z'] - prev['Z']) ** 2
        )
        if d > 1:
            p['X'] //= 2


def inverse_intervals(points, upper_bound):
    li = [0]
    for p in points:
        li.append(p['start'])
        li.append(p['end'])
    li.append(upper_bound - 1)
    def pairwise(li):
        from itertools import tee
        a, b = tee(li)
        next(b, None)
        return zip(a, b)
    pairs = []
    for i, p in enumerate(pairwise(li)):
        if i % 2 == 0:
            pairs.append(p)
    return pairs