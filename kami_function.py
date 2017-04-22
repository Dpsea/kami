# -*- coding:utf-8 -*-
# __author__ = 'L'

from io import StringIO
from typing import List, Tuple, Set
from kami_class import Block, Point
from genetic import evolve, Gene
    

def oneway(*blocks: Tuple[Block, ...], show=False, seperate=False, fold=False, stretch=2) -> str:
    _str = StringIO()
    _len = len(blocks)
    if _len > 0:
        if seperate:
            parameter = 2
        else:
            parameter = 1

        def intersect(sequence: Gene):
            linkset = set()
            stack_in: List[Set[int]] = [set() for _ in range(len(sequence) + 1)]
            stack_out: List[Set[int]] = [set() for _ in range(len(sequence) + 1)]
            c = 0
            bonus = 0
            for i in range(len(sequence)):
                _i = sequence[i]
                for block in blocks[_i].linked:
                    try:
                        j = sequence.index(blocks.index(block))
                    except ValueError:
                        j = _len
                    # print(i, j)
                    if j > i:
                        linkset.add((i, j))
                        stack_in[i].add(c)
                        stack_out[j].add(c)
                        c += 1
                        bonus += (j - i) / _len
            # print()
            # print(linkset)
            _intersect = 0
            for i in range(len(stack_out)):
                _i = i - 1
                while len(stack_out[i]) > 0:
                    # print(stack_out[i], stack_in[_i])
                    intercetion = stack_out[i] & stack_in[_i]
                    stack_out[i] -= intercetion
                    stack_in[_i] -= intercetion
                    if len(stack_out[i]) > 0:
                        _intersect += len(stack_in[_i])
                    # print(stack_out[i], stack_in[_i])
                    _i -= 1
            return _intersect * (1 + bonus / len(linkset))
        
        _sequence = tuple(sorted([i for i in range(_len)], key=lambda x: len(blocks[x].linked), reverse=True))
        _sequence = evolve(_sequence, evaluate=intersect, size=_len, elite=0.4, population=50, generation=100)
        print(intersect(_sequence))
        
        blocks = [blocks[i] for i in _sequence]
        _map = [[' '] for _ in range(_len * parameter)]

        for b in range(_len):
            _map[parameter * b][0] = blocks[b].__str__()
            if b < _len - 1:
                if blocks[b + 1] in blocks[b].linked:
                    _map[parameter * b + 1][0] = '│'

        linklist: List[Point] = []

        for b in range(_len - 1):
            _linked = blocks[b].linked - set(blocks[: b + parameter])
            for block in _linked:
                try:
                    d = blocks.index(block, b + parameter)
                except ValueError:
                    d = _len
                linklist.append((b * parameter, d * parameter))

        # order
        linklist = sorted(linklist, key=lambda x: x[1] - x[0])
        linkaddr = []
        flag = True
        _flag = True
        _b, _d, _l, _coverage = -1, -1, -1, -1
        while flag:
            try:
                if _flag:
                    linkaddr.append([])
                    _l = 0
                    _flag = False
                else:
                    _flag = True
                    linkaddr[-1].append(linklist.pop(_l))
                    _b, _d = min(linkaddr[-1], key=lambda x: x[0])[0], max(linkaddr[-1], key=lambda x: x[1])[1]
                    _l, _coverage = -1, -1

                    for l in range(len(linklist)):
                        b, d = linklist[l]
                        coverage = 0
                        if _d < b:
                            coverage = d - _b
                        elif d < _b:
                            coverage = _d - b
                        if coverage > 0:
                            if _l is -1 or coverage < _coverage:
                                _l, _coverage = l, coverage
                                _flag = False
            except IndexError:
                flag = False

        # draw
        if not fold:
            _len = len(linkaddr)
            origin = (_len // 2) * stretch
            for i in range(len(_map)):
                _map[i] = [' '] * origin + _map[i] + [' '] * (_len * stretch - origin)
            for l in range(_len):
                j = (l // 2 + 1) * stretch
                if l % 2 is 0:
                    j += origin
                    _tuple = (-1, '┐', '┘')
                else:
                    j = origin - j
                    _tuple = (+1, '┌', '└')

                if show:
                    print(linkaddr[l])
                for b, d in linkaddr[l]:
                    for i in range(b, min(d + 1, len(_map))):
                        if i is b or i is d:
                            if i is b:
                                _map[i][j] = _tuple[1]
                            else:
                                _map[i][j] = _tuple[2]
                            _j = j + _tuple[0]
                            while _j is not origin:
                                if _map[i][_j] is ' ':
                                    _map[i][_j] = '─'
                                _j += _tuple[0]
                        else:
                            _map[i][j] = '│'

        else:
            for i in range(len(_map)):
                _map[i] += [' '] * len(linkaddr) * stretch
            for l in range(len(linkaddr)):
                j = (l + 1) * stretch
                if show:
                    print(linkaddr[l])
                for b, d in linkaddr[l]:
                    for i in range(b, min(d + 1, len(_map))):
                        if i is b or i is d:
                            if i is b:
                                _map[i][j] = '┐'
                            else:
                                _map[i][j] = '┘'
                            _j = j - 1
                            while _j > 0:
                                if _map[i][_j] is ' ':
                                    _map[i][_j] = '─'
                                _j -= 1
                        else:
                            _map[i][j] = '│'

        for row in _map:
            print(file=_str)
            for p in row:
                print(p, end='', file=_str)
    return _str.getvalue()
