# -*- coding:utf-8 -*-
# __author__ = 'L'

from io import StringIO
from typing import Tuple, Union

Point = Tuple[int, int]


class Block:
    def __init__(self, color: int=0, ident: Union[int, Point]=-1, *, selection: str= '0123456789'):
        self.color = color
        self.selection = selection
        self.ident = ident
        self.linked = set()
        self.clone = None

    def link(self, *blocks):
        for block in blocks:
            if block is not self:
                self.linked.add(block)
                block.linked.add(self)

    def merge(self):
        _merge = set()
        extensional = set()
        for block in self.linked:
            if block.color == self.color:
                _merge.add(block)
        self.linked -= _merge
        for block in _merge:
            extensional |= block.linked
            block.linked = set()
        extensional -= _merge
        for block in extensional:
            block.linked -= _merge
            block.link(self)
        # if len(_merge) > 0:
        #     self.ident = min(_merge, key=lambda block: block.ident).ident
        return _merge

    @property
    def copy(self):
        if self.clone is None:
            self.clone = Block(self.color, self.ident, selection=self.selection)
            for block in self.linked:
                self.clone.link(block.copy)
        return self.clone

    @property
    def link_(self) -> str:
        _str = StringIO()
        _ident = f'{self.ident:>3}'
        if self.ident is -1:
            _ident = '   '
        print(_ident, end='', file=_str)
        print(self, end='', file=_str)
        for i in range(len(self.linked)):
            print('────┐ ', end='', file=_str)
        print('\n     ', end='', file=_str)
        for block in self.linked:
            _ident = f'{block.ident:>3}'
            if block.ident is -1:
                _ident = '   '
            print(_ident, block, end='  ', sep='', file=_str)
        return _str.getvalue()

    def __str__(self):
        return self.selection[self.color]


class Field:
    def __init__(self, *blocks):
        for block in blocks:
            if not isinstance(block, Block):
                raise TypeError
        self._tuple = blocks
        self._len = len(self._tuple)
        self._setid()
        colortable = [tuple(sorted([_b.color for _b in b.linked])) for b in self._tuple]
        decimal = [b.color for b in self._tuple]
        for i in range(self._len):
            for color in colortable[i]:
                decimal[i] = decimal[i] * 10 + color
        colortable = tuple([y[0] for y in sorted(zip(colortable, decimal), key=lambda x: x[1])])
        self._hash = hash(colortable)

    def __len__(self):
        return self._len

    def __iter__(self):
        return iter(self._tuple)

    def __eq__(self, other):
        return self._hash == other

    def __hash__(self):
        return self._hash

    def __add__(self, other):
        if isinstance(other, Block):
            _block = set(self._tuple)
            _block.add(other)
            self.__init__(*_block)
        else:
            try:
                other = set(other)
            finally:
                _block = set(self._tuple) | other
                self.__init__(*_block)
        return self

    def __getitem__(self, item):
        return self._tuple[item]

    def __call__(self):
        return self._tuple

    def merge(self):
        _set = set()
        for block in self._tuple:
            _set.add(block.copy)
        for _block in _set:
            _merge = _block.merge()
            _set -= set(_merge)
        return Field(*_set)

    @property
    def copy(self):
        _blocks = [block.copy for block in self._tuple]
        return Field(*_blocks)

    def reorderby(self, sequence):
        if len(sequence) == self._len:
            self._tuple = tuple([self._tuple[i] for i in sequence])
            self._setid()
        else:
            raise IndexError

    def _setid(self):
        for i in range(self._len):
            self[i].ident = i


def matrixstr(matrix):
    _str = StringIO()
    for i in range(len(matrix)):
        print(file=_str)
        for j in range(len(matrix[i])):
            if matrix[i][j]:
                print(matrix[i][j], end=' ', file=_str)
            else:
                print('-', end=' ', file=_str)
    print(file=_str)
    return _str.getvalue()


if __name__ == '__main__':
    from IPython import embed as e
    e()
