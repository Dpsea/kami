# -*- coding:utf-8 -*-
# __author__ = 'L'

from multiprocessing import Queue, Process
from typing import Union
from queue import Empty
import sys
import time


class ProgressBar:
    def __init__(self, *, total: int, size: int=50, graph: str='>-', hide: bool=False):
        self.size = size
        self.graph = str(graph)
        self.hide = hide
        self.total = total
        self.time = time.time()
        self.time_start = time.time()
        self.time_update = 0
        self.time_left = 0
        self.progress = 0
        self._current = 0
        self._str = '...'
        self._started = False
        self.fps = 4
        self._update_interval = 0.06
        self.q: Queue = Queue()
        self.p: Process = None

    def __call__(self, current, total=-1):
        if total is not -1:
            self.total = total
        self._current = current
        self._update()
        sys.stdout.write('\r')
        sys.stdout.write(self._str)
        sys.stdout.flush()
        if self._current >= self.total:
            print(f'\n{_timestr(time.time() - self.time_start)}')

    def _update(self):
        bar_size = int(self._current * self.size // self.total)
        self.time = time.time()
        try:
            self.time_left = (self.time - self.time_start) * (self.total - self._current) // self._current
        except ZeroDivisionError:
            self.time_left = 99 * 60
        self.progress = self._current
        bar = self.graph[0] * bar_size + self.graph[1] * (self.size - bar_size)
        percent = f'{self._current / self.total:.2%}'
        self._str = f'{bar}{percent:>9}'

    def tick(self, current: Union[int, float]=-1, subprogress=False):
        _str_subbar = ''
        if current is -1:
            self._current += 1
            _subprogress = 0
        else:
            self._current = current
            _subprogress = current - int(current)
        if not self._started:
            self._started = True
            self.time_start = time.time()
            self.q.put((self._str, self.time_left, _str_subbar))
            if not self.hide:
                self.p = Process(target=_tick, args=(self.q, self.fps))
                self.p.start()
        if self._current >= self.total:
            if not self.hide:
                self.p.terminate()
                time.sleep(1 / self.fps)
                self.__call__(self.total)
            self._started = False
            time.sleep(0.5)
        if _subprogress > 0 and subprogress:
            subbar_size = int(_subprogress * 10)
            _str_subbar = f'{self.graph[0] * subbar_size + self.graph[1] * (10 - subbar_size)}:>12'
        if time.time() - self.time_update > self._update_interval:
            self._update()
            self.time_update = time.time()
            try:
                self.q.get(False)
            except Empty:
                pass
            self.q.put((self._str, self.time_left, _str_subbar))

    def stop(self):
        if self._started:
            try:
                self.p.terminate()
            finally:
                self._started = False
                print('\nTerminated')
                time.sleep(0.5)

    def refresh(self):
        self.stop()
        self.__init__(size=self.size, graph=self.graph,
                      total=self.total, hide=self.hide)


def _tick(q: Queue, fps):
    _time = time.time()
    time_left = 0
    _str = '...'
    _str_subbar = ''
    while True:
        _signal = ' '
        try:
            _str, time_left, _str_subbar = q.get(False)
            _time = time.time()
            _signal = '.'
        except Empty:
            time_left -= time.time() - _time
            _time = time.time()
        sys.stdout.write('\r')
        sys.stdout.write(f'{_str}{_timestr(time_left):>7}{_signal}{_str_subbar}')
        sys.stdout.flush()
        time.sleep(1 / fps)


def _timestr(sec: int):
    if sec > 60:
        return f'{int(sec // 60)}m{int(sec % 60):0>2}s'
    else:
        return f'{int(sec)}s'


if __name__ == '__main__':
    import random
    process = ProgressBar(total=100)
    for i in range(100):
        process.tick()
        time.sleep(random.uniform(0.1, 0.5))
