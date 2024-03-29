# -*- coding:utf-8 -*-
# __author__ = 'L'

from kami_class import Block, Field
from map_oneway import oneway
from typing import List
import codecs


def fileinput(_in: str='', selection=''):
    with codecs.open(_in, 'r', 'utf-8') as f:
        _str = f.read().split()
    _blocks: List[List[Block]] = [[None] * 29 for _ in range(10)]
    for j in range(29):
        for i in range(10):
            color = selection.index(_str[j][i])
            if color is not 0:
                _blocks[i][j] = Block(color, addr=(i, j), selection=selection)
                if j is not 0:
                    _blocks[i][j].link(_blocks[i][j - 1])
                if i is not 0 and (j - i) % 2 is 0:
                    _blocks[i][j].link(_blocks[i - 1][j])
    return _blocks, _str


def main(*, _in, selection):
    _blocks, question = fileinput(_in, selection)
    flag = True
    while flag:
        flag = False
        for i in range(10):
            for j in range(29):
                if _blocks[i][j] is not None:
                    _merge = _blocks[i][j].merge()
                    if len(_merge) > 0:
                        for block in _merge:
                            # print(f'{block.ident}', end=' ')
                            _blocks[block.addr[0]][block.addr[1]] = None
                        # print()
                        flag = True
    blocks = Field()
    for j in range(29):
        for i in range(10):
            if _blocks[i][j] is not None:
                print(_blocks[i][j], end=' ')
                blocks += _blocks[i][j]
            else:
                print(end='  ')
        print()

    print('\n    map >>')
    gakwargs = dict(elite=0.2, population=100, generation=200, mutation=0.1, showprogress=True)
    _str, sequence = oneway(*blocks, unfold=True, output=True, ga=True, **gakwargs)
    print(_str)
    blocks.reorderby(sequence, updateid=True)
    print(hash(blocks))


if __name__ == '__main__':
    c = 6
    selection = '_ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    main(_in=f'kami_in{c}.txt', selection=selection)
