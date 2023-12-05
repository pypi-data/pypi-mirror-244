import enum
from queue import Queue
import time
import numpy as np
from loguru import logger

class Acc(enum.Enum):
    X = 0
    Y = 1
    Z = 2

class BoxPacket(object):
    def __init__(self, id, time, data) -> None:
        self.__id = id
        self.__time = time
        self.__data = data
        
    def __lt__(self, other):
        return self.__id < other.__id

    def __gt__(self, other):
        return self.__id > other.__id

    def __eq__(self, other):
        return self.__id == other.__id

    @property
    def id(self):
        return self.__id

    @property
    def data(self):
        return self.__data

class BoxMessageQueue(Queue):
    def __init__(self, maxsize: int = 0) -> None:
        super().__init__(maxsize)
        self.__uid = int(time.time() * 1000000)
        self.__latest_id = None
        self.__total = 0

    def put(self, v:BoxPacket):
        super().put(v)
        self.__latest_id = v.id
        self.__total += 1
        if self.qsize() >= 300 and self.qsize() % 100 == 0:
            logger.warning(f'队列（{self.__uid}）已有{self.__total}条数据未消费，请关注。')

    def set_uid(self, key):
        self.__uid = key

    @property
    def latest_id(self):
        return self.__latest_id

    @property
    def total(self):
        return self.__total


class BoxSignalPacket(BoxPacket):
    def __init__(self, id, time, points) -> None:
        super().__init__(id, time, points)
        self.__eeg, self.__acc = self.parse()

    # 一维数组
    @property
    def eeg(self):
        return self.__eeg

    # 一维数组/二维数组
    @property
    def acc(self, dim : Acc = None):
        if dim :
            return self.__acc[dim.value]
        
        return self.__acc
        
    def parse(self):
        # 1, 2 数据相同（只有一通道数据)
        eegs = []
        # x, y, z
        acc = [[],[],[]]
        for i in range(0, 200, 4):
            eegs.append(int.from_bytes(self.data[i : i + 2], 'little'))
        for i in range(200, 230, 6):
            acc[0].append(int.from_bytes(self.data[i : i + 2], 'little'))
            acc[1].append(int.from_bytes(self.data[i + 2 : i + 4], 'little'))
            acc[2].append(int.from_bytes(self.data[i + 4 : i + 6], 'little'))

        # 数字信号转换为电压值(mv)
        eegs = (np.array(eegs) -32768) * (2500 / 48 / 4 / 32768)
        return eegs, acc

class BoxStimPacket(BoxPacket):
    def __init__(self, id, time, data) -> None:
        super().__init__(id, time, data)
        self.__stim_id = 0
        self.__parse()

    @property
    def stim_id(self):
        return self.__stim_id

    def __parse(self):
        self.__stim_id = int.from_bytes(self.data, 'little')

class BoxStagePacket(BoxPacket):
    def __init__(self, id, time, data) -> None:
        super().__init__(id, time, data)
        self.__id2 = self.id
        self.__stage = 0
        self.__parse()

    @property
    def id2(self):
        return self.__id2

    @property
    def stage(self):
        return self.__stage

    def __parse(self):
        self.__id2 = int.from_bytes(self.data[:8], 'little')
        self.__stage = int(self.data[8])


class LMParadigm(object):
    def __init__(self, current, duration, waveform: int =0 ,ramp_up: int = 0, ramp_down: int = 0) -> None:
        self.__waveform__ = waveform
        self.__current__ = current
        self.__duration__ = duration
        self.__ramp_up__ = ramp_up
        self.__ramp_down__ = ramp_down
        self.__id__ = id
        self.__extends__ = None

    @property
    def waveform(self):
        return self.__waveform__

    @property
    def current(self):
        return self.__current__

    @property
    def duration(self):
        return self.__duration__

    @property
    def ramp_up(self):
        return self.__ramp_up__

    @property
    def ramp_down(self):
        return self.__ramp_down__




