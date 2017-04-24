# -*- coding:utf-8 -*-
# __author__ = 'L'

from threading import Thread, Lock
import sys
import time


class ProgressBar:
    def __init__(self, *, total, size=50, graph='>-', hide=False):
        self.size = size
        self.graph = graph
        self.time = time.time()
        self._time = time.time()
        self.time_left = 0
        self.progress = 0
        self._current = 0
        self.total = total
        self._thread = None
        self._tickstarted = False
        self._lock = Lock()
        self._kill = False
        self.fps = 2
        self.hide = hide

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
            if not self.hide:
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
        self._tickstarted = False

    def stop(self, show=True):
        self._lock.acquire()
        try:
            if self._tickstarted:
                self._kill = True
        finally:
            self._lock.release()
        if self._tickstarted:
            self._thread.join()
        self._tickstarted = False
        self._kill = False
        if show and self._current < self.total:
            print('Terminated')
            time.sleep(1)

    def tick(self, current=-1):
        if not self._tickstarted:
            self._thread = Thread(target=self._tick)
            self._thread.start()
            self._tickstarted = True
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
        self.__init__(size=self.size, graph=self.graph,
                      total=self.total, hide=self.hide)


def _timestr(sec: int):
    if sec > 60:
        return f'{int(sec // 60)}m{int(sec % 60):0>2}s'
    else:
        return f'{int(sec)}s'

if __name__ == '__main__':
    process = ProgressBar(total=50)
    for i in range(50):
        process.tick()
        time.sleep(0.1)