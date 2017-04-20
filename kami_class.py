# -*- coding:utf-8 -*-
# __author__ = 'L'

from io import StringIO


class Block:
    def __init__(self, color: int=0):
        self.color = color
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
    
    def copy(self, exception=set()):
        self.clone = Block(self.color)
        for block in self.linked:
            block.clone = Block(block.color)
                   

    @property
    def link_(self) -> str:
        _str = StringIO()
        print(self, end='')
        for i in range(len(self.linked)):
            print('─┐ ', end='')
        print('\n   ', end='')
        for block in self.linked:
            print(block, end='')
        return _str.getvalue()

    def __str__(self):
        return f'{self.color:^3}'


if __name__ == '__main__':
    need = False
    if need:
        from IPython import embed as e
        e()
