# -*- coding:utf-8 -*-
# __author__ = 'L'

from kami_class import Block
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
                _blocks[i][j] = Block(color)
                if j is not 0:
                    _blocks[i][j].link(_blocks[i][j - 1])
                if i is not 0 and (j - i) % 2 is 0:
                    _blocks[i][j].link(_blocks[i - 1][j])
    return _blocks


def main(*, _in, selection):
    question = fileinput(_in, selection)
    blocks = question
    flag = True
    while flag:
        flag = False
        for i in range(10):
            for j in range(29):
                if blocks[i][j] is not None:
                    _merge = blocks[i][j].merge()
                    if len(_merge) > 0:
                        flag = True
    for j in range(29):
        for i in range(10):
            if blocks[i][j] is not None:
                if len(blocks[i][j].linked) > 0:
                    print(blocks[i][j], end=' ')
                else:
                    blocks[i][j] = None
                    print('   ', end=' ')
        print()
    for j in range(29):
        for i in range(10):
            if blocks[i][j] is not None:
                print(blocks[i][j].link_)
                

if __name__ == '__main__':
    c = 6
    selection = '_ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    main(_in=f'kami_in{c}.txt', selection=selection)
