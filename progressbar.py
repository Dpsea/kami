# -*- coding:utf-8 -*-
# __author__ = 'L'

from threading import Thread, Lock
import sys
import time


class ProgressBar:
    def __init__(self, *, size=50, graph='>-', total=1):
        self.size = size
        self.graph = graph
        self.time = time.time()
        self._time = time.time()
        self.time_left = 0
        self.progress = 0
        self._current = 0
        self.total = total
        self._thread = None
        self._lock = Lock()
        self._kill = False
        self.fps = 10

    def __call__(self, current, total=0):
        if total is 0:
            total = self.total
        if current > total:
            current = total
        else:
            bar_size = int(current * self.size // total)
            percent = f'{current / total:.2%}'
            bar = self.graph[0] * bar_size + self.graph[1] * (self.size - bar_size)
            time_past = time.time() - self.time
            self.time = time.time()
            if current - self.progress != 0:
                self.time_left = (self.time - self._time) * (total - current) // current
            else:
                self.time_left -= time_past
            self.progress = current
            sys.stdout.write('\r')
            sys.stdout.write(f'{bar} {percent:>8} {_timestr(self.time_left):>7}')
            sys.stdout.flush()
        if current == total:
            print(f'\n{_timestr(time.time() - self._time)}')
            return False
        else:
            return True

    def _tick(self):
        flag = True
        while flag:
            self._lock.acquire()
            try:
                flag = self.__call__(self._current) and not self._kill
            finally:
                self._lock.release()
            time.sleep(1 / self.fps)

    def stop(self, show=True):
        self._lock.acquire()
        try:
            if self._current < self.total:
                self._kill = True
        finally:
            self._lock.release()
            if self._thread is not None:
                self._thread.join()
                self._thread = None
            self._kill = False
            if show:
                print('Terminated')
                time.sleep(1)

    def tick(self, current=-1):
        if self._thread is None:
            self._thread = Thread(target=self._tick)
            self._thread.start()
        self._lock.acquire()
        try:
            if current == -1:
                self._current += 1
            else:
                self._current = current
        finally:
            self._lock.release()

    def refresh(self):
        self.stop(False)
        self.__init__(size=self.size, graph=self.graph, total=self.total)


def _timestr(sec: int):
    if sec > 60:
        return f'{int(sec // 60)}m{int(sec % 60):0>2}s'
    else:
        return f'{int(sec)}s'
