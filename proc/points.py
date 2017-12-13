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
        text = self.text
        #
        include_chars = list(range(len(text)))
        for m in li:
            for i in range(m['start'], m['end']):
                include_chars[i] = 0
        text = ''.join(
            text[i] for i in include_chars if i
        )
        # now find all simple points
        li = self.regular_points = []
        for m in re.finditer(self.SIMPLE_REG, text):
            li.append(self.to_simple_point(m))


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
        }
        # getting full info:
        # split by spaces
        after_text = self.text[dic['end']:dic['end']+20]
        chunks = after_text.split()
        # find 1st non-match
        last_match = None
        reg = r'([RF])(-?[\d.]+)'
        for chunk in chunks:
            m = re.match(reg, chunk)
            if m:
                last_match = m
                dic[m.group(1)] = m.group(2)
        if last_match:
            dic['end'] += last_match.end()
        return dic


def adjust_dia_point(p):
    # test impl
    p['R'] *= 0.5
    p['F'] *= 2
    return p