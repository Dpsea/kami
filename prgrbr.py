# -*- coding:utf-8 -*-
# __author__ = 'L'

from multiprocessing import Queue, Process
from threading import Thread
from typing import Union
from queue import Empty
import sys
import time
import os


class ProgressBar:
    def __init__(self, *, total: int, size: int=50,
                 graph: str='=-', hide: bool=False):
        self.size = size
        self.graph = str(graph)
        self.hide = hide
        self.total = total
        self._time = time.time()
        self._starttime = time.time()
        self._updatetime = 0
        self._lefttime = 0
        self._progress = 0
        self._bar = '...'
        self._percent = ''
        self._processing = False
        self._kill = False
        self.fps = 4
        self._update_interval = 0.1
        self.q: Queue = Queue()
        self.p: Process = None
        self.t: Thread = None

    def _update(self):
        bar_size = int(self._progress * self.size // self.total)
        self._time = time.time()
        try:
            self._lefttime = (self._time - self._starttime) * (self.total - self._progress) // self._progress
        except ZeroDivisionError:
            self._lefttime = 99 * 60
        self._bar = self.graph[0] * bar_size + self.graph[1] * (self.size - bar_size)
        self._percent = f'{self._progress / self.total:.2%}'

    def __call__(self, current, total=-1):
        if total is not -1:
            self.total = total
        self._progress = current
        self._update()
        sys.stderr.write('\r')
        sys.stderr.write(f'[{self._bar}][{self._percent:^8}][{_timestr(self._lefttime):^7}]')
        sys.stderr.flush()
        if self._progress >= self.total:
            self._processing = False
            time.sleep(1 / self.fps)
            print(f'\n{_timestr(time.time() - self._starttime)}\n')

    def tick(self, current: Union[int, float] = -1):
        if not self._kill:
            if current is -1:
                self._progress += 1
            else:
                self._progress = current
            if not self._processing:
                self._processing = True
                self._starttime = time.time()
                self.q.put((self._bar, self._percent, self._lefttime))
                if not self.hide:
                    self.p = Process(target=self._tick, args=(self.q, False))
                    self.p.start()
            if time.time() - self._updatetime > self._update_interval:
                self._update()
                self._updatetime = time.time()
                try:
                    self.q.get(False)
                except Empty:
                    pass
                self.q.put((self._bar, self._percent, self._lefttime))
            if self._progress >= self.total:
                self._processing = False
                if not self.hide:
                    try:
                        self.p.terminate()
                    except AttributeError:
                        pass
                    time.sleep(1 / self.fps)
                    self.__call__(self.total)

    def start(self, *, proggetter=None):
        self._processing = True
        if proggetter is None and not self.hide:
            self.p = Process(target=self._tick, args=(None, True))
            self.p.start()
        else:
            self._starttime = time.time()
            self.q.put((self._bar, self._percent, self._lefttime))
            if not self.hide:
                self.p = Process(target=self._tick, args=(self.q, False))
                self.p.start()
            self.t = Thread(target=self._tack, args=(proggetter,))
            self.t.start()

    def _tack(self, proggetter):
        while not self._kill and self._processing:
            _progress = proggetter()
            self.tick(_progress)

    def _tick(self, q: Queue, stopwatch=False):
        if not stopwatch:
            print(f'\rPID: {os.getpid()}')
            time.sleep(1 / self.fps)
            _time = time.time()
            _lefttime = 0
            _bar = '...'
            _percent = ''
            while True:
                _signal = ' '
                try:
                    _bar, _percent, _lefttime = q.get(False)
                    _time = time.time()
                    _signal = '.'
                except Empty:
                    _lefttime -= time.time() - _time
                    _time = time.time()
                sys.stderr.write('\r')
                sys.stderr.write(f'[{_bar}][{_percent:^8}][{_timestr(_lefttime):^7}]{_signal}')
                sys.stderr.flush()
                time.sleep(1 / self.fps)
        else:
            _time = time.time()
            _neon = ['>   ',
                     '>>  ',
                     ' >> ',
                     '  >>',
                     '   >',
                     '    ',
                     '   <',
                     '  <<',
                     ' << ',
                     '<<  ',
                     '<   ',
                     '    ']
            _passedtime = 0
            while _passedtime < 6000:
                _passedtime = time.time() - _time
                _index = int(_passedtime) % len(_neon)
                sys.stderr.write('\r')
                sys.stderr.write(f'[{_neon[_index]}][{_timestr(_passedtime):^7}]')
                sys.stderr.flush()
                time.sleep(1 / self.fps)

    def stop(self, msg: str=''):
        if msg is not '':
            msg = ': ' + msg
        time.sleep(1 / self.fps)
        self._kill = True
        try:
            self.t.join()
            self.t = None
        except AttributeError:
            pass
        try:
            self.p.terminate()
            self.p = None
            if self._processing:
                self._processing = False
                print(f'\n{_timestr(time.time() - self._starttime)}')
                print(f'Terminated{msg}\n')
        except AttributeError:
            pass
        finally:
            self._kill = False
            time.sleep(1 / self.fps)

    def refresh(self):
        self.stop()
        self.__init__(size=self.size, graph=self.graph,
                      total=self.total, hide=self.hide)


def _timestr(sec: int):
    if sec > 60:
        return f'{int(sec // 60)}m{int(sec % 60):0>2}s'
    else:
        return f'{int(sec)}s'


if __name__ == '__main__':
    import random
    progressbar = ProgressBar(total=100)
    s = 0

    def getter():
        global s
        return s
    progressbar.start(proggetter=getter)
    for i in range(100):
        s = i + 1
        # progressbar.tick()
        time.sleep(random.uniform(0.01, 0.1))
        # if i is 50:
        #     progressbar.stop()
        #     break
    progressbar.stop()
