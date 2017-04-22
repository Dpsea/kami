# -*- coding:utf-8 -*-
# __author__ = 'L'

from typing import List, Tuple
import random

Gene = Tuple[int, ...]


def order_base(parents: List[Gene]) -> List[Gene]:  # Order-Based Crossover (OBX)
    size = len(parents[0])
    n = random.randint(size//2, size)
    index = sorted(pick(range(size), n=n))
    offsprings = [None, None]
    for one in [0, 1]:
        other = 1 - one
        _index = sorted([parents[one].index(parents[other][i]) for i in index])
        offsprings[one] = [parents[one][i] for i in range(size)]
        for _i in range(len(_index)):
            offsprings[one][_index[_i]] = parents[other][index[_i]]
    return [tuple(offsprings[i]) for i in [0, 1]]


def mutate(gene: Gene):
    b, o, d = sorted(pick(range(len(gene)), n=3))
    _gene = gene[:b] + gene[o:d] + gene[b:o] + gene[d:]
    return _gene


def pick(selection, weight=(), *, n=1):
    selection = list(selection)
    _len = len(selection)
    if weight is ():
        weight = [1] * _len
        _sum = _len
    else:
        weight = list(weight)
        _sum = sum(weight)
    x = 0
    while x == 0:
        x = random.uniform(0, _sum)
    _sum, i = 0, -1
    while _sum < x:
        i += 1
        _sum += weight[i]
    if n is 1:
        return selection[i]
    else:
        _one = selection.pop(i)
        weight.pop(i)
        _others = pick(selection, weight, n=n - 1)
        if n is 2:
            return [_others, _one]
        else:
            return _others + [_one]


def evolve(*ancestors: Tuple[Gene, ...], evaluate, crossover=order_base,
           size: int, population: int=100, generation: int=100,
           mutation: float=0.05, elite: float=0.2, target=0):
    _elite = int(population * elite)
    herd: List[Gene] = []
    if ancestors is not ():
        for gene in ancestors:
            herd.append(tuple(gene))

    for _ in range(population - len(herd)):
        gene = [i for i in range(size)]
        random.shuffle(gene)
        herd.append(tuple(gene))

    # x, y = 0, 0
    for _ in range(generation):
        _evaluate = [evaluate(gene) for gene in herd]
        _zip = sorted(zip(_evaluate, herd), key=lambda x: x[0])
        while _zip[0][0] is -1:
            _zip.pop(0)
        if _zip[0][0] == target:
            return _zip[0][1]
        print(_zip[0][0], _zip[0][1])
        herd, parents, weight = set(), [], []
        for p in _zip:
            weight.append(1 / p[0])
            parents.append(p[1])
        for i in range(_elite):
            herd.add(parents[i])
        while len(herd) < population:
            offsprings = crossover(pick(parents, weight, n=2))
            herd |= set(offsprings)
        herd = list(herd)
        for i in range(len(herd)):
            if pick([True, False], [mutation, 1 - mutation]):
                herd[i] = mutate(herd[i])
        
    #             x += 1
    #         else:
    #             y += 1
    # print(x, y)
    # print(herd)
    print([evaluate(gene) for gene in herd])
    return min(herd, key=evaluate)
