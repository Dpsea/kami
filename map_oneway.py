# -*- coding:utf-8 -*-
# __author__ = 'L'

from io import StringIO
from typing import List, Set
from genetics import evolve, Gene


_blocks, _stretch, _unfold = (), 2, True


def draw(blocks, links, link_map, *, showid=False, stretch=2):
    _len = len(blocks)
    _map = [[] for _ in range(_len)]
    wide = [max([len(link_map[which][i]) for i in range(_len)]) for which in (0, 1)]
    print(wide)
    if not showid:
        for i in range(_len):
            _map[i].append(blocks[i].__str__())
    else:
        for i in range(_len):
            _map[i].append(f'{blocks[i].id:0>3}' + blocks[i].__str__())
    
    if stretch < 2:
        empty = ''
        line = ''
    else:
        empty = ' ' * (stretch - 1 - (stretch + 1) // 2)
        line = '─' * ((stretch + 1) // 2)
    for i in range(_len):
        _map[i] = [' '] * wide[0] + _map[i] + [' '] * wide[1]
        for j in reversed(range(0, wide[0])):
            _j = wide[0] - j - 1
            try:
                c = link_map[0][i][_j]
                if c is not ' ':
                    b, d = links[c]
                    if i is b:
                        _map[i][j] = '┌'
                    elif i is d:
                        _map[i][j] = '└'
                    else:
                        _map[i][j] = '│'
            except IndexError:
                break
        flag, interv = False, ' ' * (stretch - 1)
        for j in range(0, wide[0] + 1):
            if flag and _map[i][j] is ' ':
                _map[i][j] = '─' * stretch
            elif not flag and (_map[i][j] is '┌' or _map[i][j] is '└'):
                _map[i][j] = interv + _map[i][j]
                flag, interv = True, line + empty
            else:
                _map[i][j] = interv + _map[i][j]
        
        for j in range(wide[0] + 1, wide[0] + wide[1] + 1):
            _j = j - wide[0] - 1
            try:
                c = link_map[1][i][_j]
                if c is not ' ':
                    b, d = links[c]
                    if i is b:
                        _map[i][j] = '┐'
                    elif i is d:
                        _map[i][j] = '┘'
                    else:
                        _map[i][j] = '│'
            except IndexError:
                break
        flag, interv = False, ' ' * (stretch - 1)
        for j in reversed(range(wide[0], wide[0] + wide[1] + 1)):
            if flag and _map[i][j] is ' ':
                _map[i][j] = '─' * stretch
            elif not flag and (_map[i][j] is '┐' or _map[i][j] is '┘'):
                _map[i][j] += interv
                flag, interv = True, empty + line
            else:
                _map[i][j] += interv
    return _map


def intersect(sequence: Gene, *, output=False):
    global _blocks, _unfold
    unfold = _unfold
    blocks = _blocks
    _len = len(blocks)
    links = []
    stack_in: List[Set[int]] = [set() for _ in range(_len + 1)]
    stack_out: List[Set[int]] = [set() for _ in range(_len + 1)]
    c = 0
    bonus = 0
    for b in range(len(sequence)):
        i = sequence[b]
        for block in blocks[i].linked:
            try:
                d = sequence.index(blocks.index(block))
            except ValueError:
                d = _len
            if b < d:
                links.append((b, d))
                stack_in[b].add(c)
                stack_out[d].add(c)
                c += 1
                bonus += (d - b) ** 2
    
    _intersect = []
    link_map = [[[] for _ in range(_len + 1)] for _ in range(2)]
    needle = [0, 0]
    side = [set(), set()]
    for d in range(_len + 1):
        b = d
        while len(stack_out[d]) > 0:
            b -= 1
            intersetion = stack_out[d] & stack_in[b]
            stack_out[d] -= intersetion
            stack_in[b] -= intersetion
            if output:
                for c in intersetion:
                    choice = (0, 1)
                    if not unfold:
                        choice = (1,)
                    else:
                        for which in (0, 1):
                            if c in side[which]:
                                choice = (which,)
                    needle = [-1, -1]
                    for which in choice:
                        i = b - 1
                        while i != d:
                            needle[which] += 1
                            i = b - 1
                            something = ' '
                            while something is ' ' and i < d:
                                i += 1
                                try:
                                    something = link_map[which][i][needle[which]]
                                except IndexError:
                                    distance = needle[which] - len(link_map[which][i])
                                    link_map[which][i] += [' '] * (distance + 1)
                                    something = ' '
                    which = min(choice, key=lambda x: needle[x])
                    for i in range(b, d + 1):
                        link_map[which][i][needle[which]] = c
            
            if unfold:
                for c_in in stack_in[b]:
                    for c_out in stack_out[d]:
                        which_in, which_out = -1, -1
                        for which in (0, 1):
                            if c_in in side[which]:
                                which_in = which
                            if c_out in side[which]:
                                which_out = which
                            if which_in + which_out == -2:
                                side[0].add(c_in)
                                side[1].add(c_out)
                            elif which_in == which_out:
                                _intersect.append((c_in, c_out))
                            elif which_in == -1:
                                side[1 - which_out].add(c_in)
                            elif which_out == -1:
                                side[1 - which_in].add(c_out)
            else:
                _intersect += [(c_in, c_out) for c_in in stack_in[b] for c_out in stack_out[d]]
                # print(stack_out[d], stack_in[b])
    if output:
        for which in (0, 1):
            print()
            for row in link_map[which]:
                for p in row:
                    print(f'{p:<3}', end='')
                print()
        return len(_intersect), links, link_map,
    else:
        return len(_intersect) + (bonus / len(links)) ** 0.5


def oneway(*blocks, showid=False, unfold=True, stretch=2, ga=True, **gakwargs) -> str:
    global _blocks, _unfold
    _str = StringIO()
    _stretch, _unfold = stretch, unfold
    _blocks = blocks
    _len = len(blocks)
    if _len > 0:
        _sequence = tuple([i for i in range(_len)])
        if ga:
            gakw_local = dict(evaluate=intersect, size=_len, elite=0.2,
                              population=100, generation=300, showprogress=True)
            gakw_local.update(**gakwargs)
            _sequence = evolve(_sequence, **gakw_local)
        
        _inters = intersect(_sequence, output=True)
        print(_inters[0])
        _blocks = tuple([_blocks[i] for i in _sequence])
        _map = draw(_blocks, *_inters[1:], showid=showid, stretch=2)
        
        for row in _map:
            print('\n', end='', file=_str)
            for p in row:
                print(p, end='', file=_str)
    return _str.getvalue()
