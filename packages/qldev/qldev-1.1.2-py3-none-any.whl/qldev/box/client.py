import hashlib
from signal import raise_signal, signal
from threading import Lock, Thread
from typing import Literal
from loguru import logger
from time import time, sleep

from qldev.box.message import TCPMessage
from qldev.box.model import BoxMessageQueue, BoxPacket, BoxSignalPacket, BoxStagePacket, BoxStimPacket
from qldev.device import MessageHandler, QLDevice
from qldev.utils import TCPCommand


class BoxClient(QLDevice):
    ID = 'mac'
    def __init__(self, socket, address = None, handler: MessageHandler = None, auto_save = False) -> None:
        super().__init__(handler)
        self.__auto_save = auto_save
        self.__socket = socket
        self.__address = address
        self.__parser = BoxClientMessage(self)
        self.__create_time = int(time())
        self.__listening = False
        self.__info = None
        self.__channels = {'signal' : {}, 'stim' : {}, "stage" : {}}

    @property
    def mac(self):
        if self.__info and BoxClient.ID in self.__info.keys():
            return self.__info[BoxClient.ID]
        return None

    @property
    def address(self):
        return self.__address

    @property
    def key(self):
        if self.__address and len(self.__address) == 2:
            return f'{self.__address[0]}_{self.__address[1]}'
        return None

    def subscribe(self, consumer:BoxMessageQueue, key = 'default', type:Literal['signal', 'stim', 'stage'] = 'signal'):
        if key is None:
            key = 'default'

        key = f'{self.mac}_{type}_{key}'
        
        if key in self.__channels[type].keys():
            logger.error(f'subscribe({key}) already exists in device({self.__address}). ')
            return 

        if consumer:
            consumer.set_uid(key)
            self.__channels[type][key] = consumer
        logger.info(f'已添加设备device({self.mac} - {self.__address}的消息订阅（{key}），当前{type}的订阅任务共有{len(self.__channels[type])}个。')

    def listen(self, buffersize = 1024):
        if self.__listening:
            logger.warning(f"BoxClient({self.mac}-{self.__address}) is listening.")
            return

        # 启动客户端消息监听
        t = Thread(target=self.__accept, args=(buffersize, ))
        t.setDaemon(True)
        t.start()

        if self.__auto_save:
            self.__save_to_edf()

        return self

    def __save_to_edf(self):
        q = BoxMessageQueue()
        self.subscribe(q, key = "save_to_edf")
        t = Thread(target=self.__save, args=(q,))
        # t.setDaemon(True)
        t.start()

    def __save(self, data : BoxMessageQueue):
        edf_fname = ""
        with open(edf_fname, ) as tmp:
            while True:
                if data.empty():
                    time.sleep(1)



    def update(self, devinfo):
        logger.trace(devinfo)
        if devinfo :
            self.__info = devinfo
            if self.mac:
                self.handler.add_client(self)

    # 信号数据
    def signals(self, data):
        if self.mac is None or len(self.__channels['signal']) == 0:
            logger.trace('Mac is none or no subscribe for signal message.')
            return

        logger.trace(data)
        for key in self.__channels['signal'].keys():
            try:
                self.__channels['signal'][key].put(data)
            except Exception as e:
                logger.error(f"BoxClient({self.mac} - {self.__address}) 添加消息到订阅（{key}）异常: {e}")

    # 信号数据
    def stim(self, data):
        if self.mac is None or len(self.__channels['stim']) == 0:
            logger.trace('Mac is none or no subscribe for stim message.')
            return

        logger.trace(data)
        for key in self.__channels['stim'].keys():
            try:
                self.__channels['stim'][key].put(data)
            except Exception as e:
                logger.error(f"BoxClient({self.mac} - {self.__address}) 添加消息到订阅（{key}）异常: {e}")

    # 信号数据
    def sleep_stage(self, data):
        if self.mac is None or len(self.__channels['stage']) == 0:
            logger.trace('Mac is none or no subscribe for stage message.')
            return

        logger.trace(data)
        for key in self.__channels['stage'].keys():
            try:
                self.__channels['stage'][key].put(data)
            except Exception as e:
                logger.error(f"BoxClient({self.mac} - {self.__address}) 添加消息到订阅（{key}）异常: {e}")

    # 启动信号采集
    def start_acquire(self):
        self._send(TCPMessage.start_acquire())
        
        return self
    
    # 停止信号采集
    def stop_acquire(self):
        self._send(TCPMessage.stop_acquire())
        
        return self
    
    # 设置范式
    def set_paradigm(self, paradigm:dict):
        self._send(TCPMessage.set_paradigm(paradigm))
        
        return self


    def ask(self):
        self._send(TCPMessage.get_device_info())
        
        return self
        
    def trigger(self, type=0):
        self._send(TCPMessage.trigger(type))

    def wav_update_ready(self, id, len):
        self._send(TCPMessage.wav_update_ready(id, len))

    def wav_update(self, id, offset, len, data):
        self._send(TCPMessage.wav_update(id, offset, len, data))

    def wav_update_stop(self, id, checksum):
        self._send(TCPMessage.wav_update_stop(id, checksum))

    def wav_trigger(self, id, volumn):
        self._send(TCPMessage.wav_trigger(id, volumn))
       
    # id是音频编号，取值范围为[0-7]，表示第1-8个音频位置
    # fname是本地音频文件的存储路径  
    def update_wav(self, id, fname, buffer=3072):    

        with open(fname, 'rb') as f:
            flen = f.seek(0, 2)
            logger.debug(f"file{fname} len is {flen}")
            self.wav_update_ready(id, flen)
            time.sleep(0.1)

            f.seek(0)
            offset = 0
            buf = f.read(buffer)
            md5 = hashlib.md5()
            while buf:
                blen = len(buf)
                logger.debug(f"update(id:{id}, offset:{offset}/{flen}, llen:{blen})")
                self.wav_update(id, offset, blen, buf)
                md5.update(buf)
                # 指令发送间隔，避免数据处理异常
                time.sleep(0.01)
                offset += blen
                buf = f.read(buffer)
            logger.debug(f"file{fname} offset is {offset} md5 is {md5.hexdigest()}")

            self.wav_update_stop(id, md5.hexdigest())
            logger.debug(f'file{fname} update finished.')    

    def __accept(self, buffersize = 1024):
        self.__listening = True
        while self.__listening:
            try:
                # 接收对方发送过来的数据
                recv_data = self.__socket.recv(buffersize)  
                if recv_data:                    
                    logger.trace(f'receive len is {len(recv_data)}')
                    self.__parser.extend(recv_data)
                    self.__parser.parse()
                else:
                    break
            except Exception as e:
                logger.error(f"BoxClient({self.mac}-{self.__address})接收消息出现异常：{e}")
                break

        self.__socket.close()
        logger.info(f"BoxClient({self.mac}-{self.__address})连接已断开")

        # 释放当前实例
        self.__release()

    def _send(self, message):
        try:
            self.__socket.send(message)
        except Exception as e:
            logger.warning(f"发送TCP消息异常:{e}")

    def __release(self):
        self.__parser = None
        self.handler.remove_client(self)


class BoxClientMessage(object):
    # 包头
    HEADER = 42330

    def __init__(self, client : BoxClient) -> None:
        self.__client = client
        self.__messages = bytearray()
        self.__lock = Lock()

    def extend(self, message):
        if len(message) > 0:
            self.__lock.acquire()
            self.__messages.extend(message)
            self.__lock.release()

    def parse(self):        

        while len(self.__messages) > 12:
            self.__lock.acquire()
            while len(self.__messages) > 12 and int.from_bytes(self.__messages[:2], "little") != BoxClientMessage.HEADER:
                self.__messages.pop(0)
            self.__lock.release()

            # 包长度
            mlen = int.from_bytes(self.__messages[8:12], "little")
            logger.trace(f'The current packet length is {mlen}, message length is {len(self.__messages)}')

            if mlen == 0:
                logger.warning("数据包中的长度值为0")
                break

            if len(self.__messages) == mlen:
                packet = self.__messages.copy()
                self.__lock.acquire()
                self.__messages = bytearray()
                self.__lock.release()
                self.__parse(packet)
            elif len(self.__messages) > mlen:
                packet = self.__messages[:mlen]
                self.__lock.acquire()
                self.__messages = self.__messages[mlen:]
                self.__lock.release()
                self.__parse(packet)
            else:
                logger.warning("消息长度小于数据包中的长度值")
                break
        
    def __parse(self, packet):
        plen = len(packet)
        # 最小有效包长度
        if plen < 16:
            logger.warning(f"不支持的消息长度: {len}")
            return
        
        cmd = int.from_bytes(packet[12:14], 'little')
        data = packet[14:-2]
        result = (int)(data[8])
        if result != 0:
            logger.warning(f"cmd {hex(cmd)} result is {result}(0: success others: failed)")
            return

        # logger.info(f"cmd is {hex(cmd)}")
        if cmd == TCPCommand.GET_DEVICE_INFO.value:
            devinfo = self.get_device_info(data)
            self.__client.update(devinfo)
            return
            
        if cmd == TCPCommand.SIGNALS.value:
            self.__client.signals(self.signals(data))
            return

        if cmd == TCPCommand.STIM.value:
            self.__client.stim(self.stim(data))
            return 

        if cmd == TCPCommand.SLEEP_STAGE.value:
            self.__client.sleep_stage(self.sleep_stage(data))
            return 
            
        if cmd == TCPCommand.TRIGGER.value:
            self.trigger(data)
            return
            
        if cmd == TCPCommand.WAV_UPDATE_READY.value:
            self.wav_update_ready(data)
            return
            
        if cmd == TCPCommand.WAV_UPDATE.value:
            self.wav_update(data)
            return
            
        if cmd == TCPCommand.WAV_UPDATE_FINISH.value:
            self.wav_update_stop(data)
            return
            
        if cmd == TCPCommand.WAV_TRIGGER.value:
            self.wav_trigger(data)
            return
            
        if cmd == TCPCommand.SET_PARADIGM.value:
            logger.info('Set paradigm success.')
            return
            
        if cmd == TCPCommand.START_ACQUIRE.value:
            logger.info('Acquire signals start success.')
            return
            
        if cmd == TCPCommand.STOP_ACQUIRE.value:
            logger.info('Acquire signals stop success.')
            return

        self.not_support(cmd, data)

    def get_device_info(self, data):
        info = {}
        info["mac"] = hex(int.from_bytes(data[9:17], 'little'))
        info["dev_type"] = int.from_bytes(data[17:21], 'little')
        info["sw_version"] = int.from_bytes(data[21:25], 'little')
        info["hw_version"] = int.from_bytes(data[25:29], 'little')
        logger.debug(f"get_device_info->{info}")
        return info

    def signals(self, data):
        logger.trace(f"The signal data length is {len(data)}")
        # packet = {}
        # packet["packet_id"] = int.from_bytes(data[9:17], 'little')
        # packet["channels"] = data[17:49]
        # packet["origin_rate"] = int.from_bytes(data[49:53], 'little')
        # packet["sample_rate"] = int.from_bytes(data[53:57], 'little')
        # packet["sample_len"] = int.from_bytes(data[57:61], 'little')
        # packet["resolution"] = int.from_bytes(data[61:63], 'little')
        # packet["filter"] = int(data[63])
        # packet["data_len"] = int.from_bytes(data[64:68], 'little')
        # packet["data"] = data[68:]
        time = int.from_bytes(data[0:8], 'little')
        id = int.from_bytes(data[9:17], 'little')
        points = data[68:]

        return BoxSignalPacket(id, time, points)
        
    def stim(self, data):
        time = int.from_bytes(data[0:8], 'little')
        id = int.from_bytes(data[9:17], 'little')
        points = data[17:]

        return BoxStimPacket(id, time, points)
        
    def sleep_stage(self, data):
        time = int.from_bytes(data[0:8], 'little')
        id = int.from_bytes(data[9:17], 'little')
        points = data[17:]
        return BoxStagePacket(id, time, points)
        
    def trigger(self, data):
        logger.debug("trigger success.")
        return
        
    def wav_update_ready(self, data):
        logger.debug("wav_update_ready success.")
        return
        
    def wav_update(self, data):
        logger.debug("wav_update success.")
        return
        
    def wav_update_stop(self, data):
        logger.debug("wav_update_finsih success.")
        return
        
    def wav_trigger(self, data):
        logger.debug("wav_trigger success.")
        return
        
    def not_support(self, cmd, data):
        logger.warning(f"cmd({hex(cmd)})not support.")
        return
