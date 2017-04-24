# -*- coding:utf-8 -*-
# __author__ = 'L'

from kami_class import Block
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
                _blocks[i][j] = Block(color, (i, j), selection=selection)
                if j is not 0:
                    _blocks[i][j].link(_blocks[i][j - 1])
                if i is not 0 and (j - i) % 2 is 0:
                    _blocks[i][j].link(_blocks[i - 1][j])
    return _blocks


def main(*, _in, selection):
    question = fileinput(_in, selection)
    _blocks: List[List[Block]] = [[None] * 29 for _ in range(10)]
    for i in range(10):
        for j in range(29):
            _blocks[i][j] = question[i][j].copy
            
    flag = True
    while flag:
        flag = False
        for i in range(10):
            for j in range(29):
                if _blocks[i][j] is not None:
                    _merge = _blocks[i][j].merge()
                    if len(_merge) > 0:
                        # print(_blocks[i][j], end=' ')
                        for block in _merge:
                            # print(f'{block.id}', end=' ')
                            _blocks[block.id[0]][block.id[1]] = None
                        # print()
                        flag = True
    blocks = []
    for j in range(29):
        for i in range(10):
            # print(_blocks[i][j], end=' ')
            if _blocks[i][j] is not None:
                if len(_blocks[i][j].linked) > 0:
                    print(_blocks[i][j], end=' ')
                    blocks.append(_blocks[i][j])
                    blocks[-1].id = len(blocks) - 1
            else:
                print(end='  ')
        print()
 
    print('\n    map >>')
    print(oneway(*blocks))
    
    # print('\n   link >>')
    # for block in blocks:
    #     print(block.link_)

if __name__ == '__main__':
    c = 4
    selection = '_ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    main(_in=f'kami_in{c}.txt', selection=selection)
