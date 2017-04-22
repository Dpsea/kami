# -*- coding:utf-8 -*-
# __author__ = 'L'

from io import StringIO
from typing import Tuple, Union

Point = Tuple[int, int]


class Block:
    def __init__(self, color: int=0, id: Union[int, Point]=-1, *, selection: str= '0123456789'):
        self.color = color
        self.selection = selection
        self.id = id
        self.linked = set()
        self.clone = None

    def link(self, *blocks):
        for block in blocks:
            if block is not self:
                self.linked.add(block)
                block.linked.add(self)

    def merge(self):
        merge_ = set()
        extensional = set()
        for block in self.linked:
            if block.color is self.color:
                merge_.add(block)
        self.linked -= merge_
        for block in merge_:
            extensional |= block.linked
            block.linked = set()
        extensional -= merge_
        for block in extensional:
            block.linked -= merge_
            block.link(self)
        return merge_

    @property
    def copy(self):
        if self.clone is None:
            self.clone = Block(self.color, self.id, selection=self.selection)
            for block in self.linked:
                self.clone.link(block.copy)
        return self.clone

    @property
    def link_(self) -> str:
        _str = StringIO()
        print(f'({self.id:0>2})', end='', file=_str)
        print(self, end='', file=_str)
        for i in range(len(self.linked)):
            print('─────┐ ', end='', file=_str)
        print('\n      ', end='', file=_str)
        for block in self.linked:
            print(f'({block.id:0>2})', end='', file=_str)
            print(block, end='  ', file=_str)
        return _str.getvalue()

    def __str__(self):
        return self.selection[self.color]


if __name__ == '__main__':
    from IPython import embed as e
    e()
