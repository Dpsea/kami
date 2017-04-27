# -*- coding:utf-8 -*-
# __author__ = 'L'

import unittest
from kami_class import Block, Field
from map_oneway import oneway


class KamiTest(unittest.TestCase):
    def _str(self, _name):
        return f'{_name:-^20}'

    def test_crossover(self):
        print(self._str('crossover'))
        from genetics import order_base
        a = (1, 2, 3, 4, 5, 6, 7)
        b = (2, 3, 5, 6, 7, 1, 4)
        print(a, b, sep='\n')
        c, d = order_base([a, b])
        print(c, d, sep='\n')

    def test_evolve(self):
        print(self._str('evolve'))
        from genetics import evolve
        
        def f(nlist):
            s = 0
            for n in nlist:
                s = s * 10 + n
            return s
        print(evolve(evaluate=f, size=15, generation=20, showprogress=False))
        
    def test_pick(self):
        print(self._str('pick'))
        from genetics import pick
        selection = [[1, 2, 3], [2, 3, 4], [3, 4, 5], [1, 2, 4, 4]]
        weight = [0.6, 0.1, 0.2, 0.1]
        print(pick(selection, weight))
        print(sorted(pick(range(15), n=7)))

    def test_link(self):
        print(self._str('link'))
        blocks = []
        for i in range(4):
            blocks.append(Block(i))
        blocks[0].link(*blocks[1:])
        blocks[1].link(blocks[2])
        blocks[1].link(blocks[0])  # 重复添加

        # for block in blocks:
        #     print(block.link_)

    def test_merge(self):
        print(self._str('merge'))
        blocks = [Block(0), Block(0), Block(0),
                  Block(1), Block(2), Block(1),
                  Block(1), Block(2), Block(1),
                  Block(0), Block(0)]
        blocks[0].link(blocks[1], blocks[4], blocks[3])
        blocks[1].link(blocks[0], blocks[4], blocks[2])
        blocks[2].link(blocks[1], blocks[4], blocks[5])
        blocks[3].link(blocks[0], blocks[4], blocks[6])
        blocks[4].link(blocks[0], blocks[1], blocks[2], blocks[3], blocks[5], blocks[7])
        blocks[5].link(blocks[2], blocks[4], blocks[8])
        blocks[6].link(blocks[3], blocks[7], blocks[9])
        blocks[7].link(blocks[4], blocks[6], blocks[8], blocks[9], blocks[10])
        blocks[8].link(blocks[5], blocks[7], blocks[10])
        blocks[9].link(blocks[6], blocks[7], blocks[10])
        blocks[10].link(blocks[7], blocks[8], blocks[9])

        for block in blocks:
            print(block.link_)

        for block in blocks:
            block.merge()

        print('    merge >>')
        for block in blocks:
            if len(block.linked) > 0:
                print(block.link_)

    def test_copy(self):
        print(self._str('copy'))
        blocks = [Block(i, selection='ABCD') for i in range(4)]
        blocks[0].link(blocks[1], blocks[2])
        blocks[1].link(blocks[0], blocks[2])
        blocks[2].link(blocks[0], blocks[1], blocks[3])
        f = Field(*blocks, updateid=True)
        fcopy = f.copy
        for block in f:
            if len(block.linked) > 0:
                print(block.link_)
        print('    copy >>')
        for block in fcopy:
            if len(block.linked) > 0:
                print(block.link_)

    def test_map(self):
        print(self._str('map'))
        blocks = [Block(2),
                  Block(0),
                  Block(1), Block(1),
                  Block(2), Block(3), Block(2),
                  Block(1), Block(1),
                  Block(0),
                  Block(2)]
        blocks[5].link(*(blocks[1: 5] + blocks[6: 10]))
        blocks[0].link(*blocks[1: 4])
        blocks[10].link(*blocks[7: 10])
        for block in blocks:
            print(block.link_)
        f0 = Field(*blocks)
        print(oneway(*f0, ga=True, population=50, generation=20, showprogress=False))
        f1 = f0.color_(5, 1)
        print(oneway(*f1))
        f2 = f1.color_(3, 2)
        print(oneway(*f2))
        f3 = f2.color_(1, 0)
        print(oneway(*f3))


if __name__ == '__main__':
    unittest.main()
