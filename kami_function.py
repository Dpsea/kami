# -*- coding:utf-8 -*-
# __author__ = 'L'

from io import StringIO
from typing import Tuple, List
from kami_class import Block, Point


def map_(*blocks: Tuple[Block], seperate=False, fold=False, stretch=2) -> str:
    _str = StringIO()
    _len = len(blocks)
    if _len > 0:
        if seperate:
            parameter = 2
        else:
            parameter = 1

        # blocks = sorted(blocks, key=lambda x: len(x.linked))
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
                d = blocks.index(block, b + parameter)
                linklist.append((b * parameter, d * parameter))
        
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
                
                print(linkaddr[l])
                for b, d in linkaddr[l]:
                    for i in range(b, d + 1):
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
                print(linkaddr[l])
                for b, d in linkaddr[l]:
                    for i in range(b, d + 1):
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
