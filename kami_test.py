# -*- coding:utf-8 -*-
# __author__ = 'L'

import unittest
from kami_class import Block


class KamiTest(unittest.TestCase):
    

    def test_link(self):
        _name = 'test_link'
        print(f'{_name:-^20}')
        blocks = []
        for i in range(4):
            blocks.append(Block(i))
        blocks[0].link(*blocks[1:])
        blocks[1].link(blocks[2])
        blocks[1].link(blocks[0])  # 重复添加

        for block in blocks:
            print(block.link_)

    def test_merge_unit(self):
        _name = 'test_merge_unit'
        print(f'{_name:-^20}')
        blocks = [Block(0), Block(0), Block(1)]
        blocks[0].link(blocks[1])
        for block in blocks:
            print(block.link_)

        for block in blocks:
            block.merge()

        print('    ---->')
        for block in blocks:
            print(block.link_)

    def test_merge(self):
        _name = 'test_merge'
        print(f'{_name:-^20}')
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

        print('    ---->')
        for block in blocks:
            if len(block.linked) > 0:
                print(block.link_)
    
    def test_del(self):
        blocks = [Block(0), Block(0), Block(1)]


if __name__ == '__main__':
    unittest.main()
