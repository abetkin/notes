text = '''\
X23 Z-5 f
X.3 X.4
'''
import re
reg_any = r'([XZ])-?([.\d]+)\s'



def make_points(text):
    def parse(match):
        return {
            match.group(1): match.group(2),
            "start": match.start(),
            "end": match.end(),
        }
    return [
        parse(m)
        for m in re.finditer(reg_any, text)
    ]

def adjacent(left, right):
    if left['end'] != right['start']:
        return
    X = left.get('X') or right.get('X')
    Z = left.get('Z') or right.get('Z')
    return bool(X and Z)
    

def merge_points(points):
    new_points = []
    prev = None
    for p in points:
        if prev and adjacent(prev, p):
            # assert coords are different
            prev['end'] = p['end']
            prev.setdefault('X', p.get('X'))
            prev.setdefault('Z', p.get('Z'))
        else:
            if prev:
                new_points.append(prev)
            prev = p
    # count the last one
    if prev:
        new_points.append(prev)
    return new_points

def fetch_point(p, text):
    # - split by spaces
    # - stop on 1st non-match
    LEN = 10
    end = p['start'] + LEN
    text = text[p['end']:end]
    reg = r'([RF]-?[\d.]+)+'
    re.match(reg, text)