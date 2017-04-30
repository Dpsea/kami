# -*- coding:utf-8 -*-
# __author__ = 'L'

from io import StringIO
from typing import Tuple

Point = Tuple[int, int]


class Block:
    def __init__(self, color: int=0, ident: int=-1,
                 addr: Point = (-1, -1), selection: str='0123456789'):
        self.color = color
        self.selection = selection
        self.ident = ident
        self.addr = addr
        self.linked = set()
        self.colortable = None

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
    
    @property
    def properties(self):
        return self.color, self.ident, self.addr, self.selection

    def __str__(self):
        return self.selection[self.color]


class Field:
    def __init__(self, *blocks, updateid=False):
        for block in blocks:
            if not isinstance(block, Block):
                raise TypeError
        self._tuple: Tuple[Block] = blocks
        self._len: int = len(self._tuple)
        if updateid:
            self._updateid()
        self._hash = None

    def __len__(self):
        return self._len

    def __iter__(self):
        return iter(self._tuple)

    def __eq__(self, other):
        return hash(self) == other

    def __hash__(self):
        if self._hash is None:
            self._hash = self._gethash
        return self._hash
    
    @property
    def _gethash(self):
        self.colortable = [tuple(sorted([_b.color for _b in b.linked])) for b in self._tuple]
        decimal = [b.color for b in self._tuple]
        for i in range(self._len):
            for color in self.colortable[i]:
                decimal[i] = decimal[i] * 10 + color
        self.colortable = tuple([y[0] for y in sorted(zip(self.colortable, decimal), key=lambda x: x[1])])
        return hash(self.colortable)

    def __add__(self, other):
        if isinstance(other, Block):
            if other not in self._tuple:
                self.__init__(*self._tuple, other)
        else:
            try:
                other = set(other)
            finally:
                other -= set(self._tuple)
                if len(other) > 0:
                    self.__init__(*self._tuple, *other)
        return self
    
    def __sub__(self, other):
        if isinstance(other, Block):
            if other in self._tuple:
                i = self._tuple.index(other)
                self.__init__(*self._tuple[: i], *self._tuple[i + 1:])
        else:
            try:
                other = set(other)
            finally:
                _tuple = []
                for b in self._tuple:
                    if b not in other:
                        _tuple += [b]
                self.__init__(*_tuple)
        return self

    def __getitem__(self, i) -> Block:
        return self._tuple[i]
    
    def __call__(self):
        return self._tuple
    
    @property
    def copy(self):
        blocks = [Block(*b.properties) for b in self._tuple]
        for i in range(self._len):
            for b in self._tuple[i].linked:
                _i = self._tuple.index(b)
                blocks[i].link(blocks[_i])
        return Field(*blocks)
    
    @property
    def colorfulness(self):
        colorset = set()
        for block in self:
            colorset.add(block.color)
        return len(colorset)
    
    def color_(self, i: int, color: int):
        flag = False
        for block in self[i].linked:
            if block.color == color:
                flag = True
                break
        if flag:
            f = self.copy
            f[i].color = color
            f -= f[i].merge()
            return f
        else:
            return None

    def reorderby(self, sequence, *, updateid=False):
        if len(sequence) == self._len:
            self._tuple = tuple([self._tuple[i] for i in sequence])
            if updateid:
                self._updateid()
        else:
            raise IndexError
    
    def _updateid(self):
        for i in range(self._len):
            self[i].ident = i
            
    def index(self, block: Block):
        return self._tuple.index(block)
    
    def search_(self, *, color=None, ident=None, addr=None):
        blocks = list(self._tuple)
        if color is not None:
            i = 0
            while i < len(blocks):
                if blocks[i].color is color:
                    i += 1
                else:
                    blocks.pop(i)
        if ident is not None:
            i = 0
            while i < len(blocks):
                if blocks[i].ident is ident:
                    i += 1
                else:
                    blocks.pop(i)
        if addr is not None:
            i = 0
            while i < len(blocks):
                if blocks[i].addr is addr:
                    i += 1
                else:
                    blocks.pop(i)
        return blocks


if __name__ == '__main__':
    from IPython import embed as e
    e()
