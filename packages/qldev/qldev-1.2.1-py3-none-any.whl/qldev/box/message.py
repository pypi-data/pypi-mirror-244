
from time import time
from loguru import logger

from qldev.utils import TCPCommand, UDPCommand
from qldev.utils import check_crc, crc16, get_ip


class UDPMessage(object):
    START = "SHQuanLan"
    MAC = 'mac'
    DEV_TYPE = "dev_type"
    VERSION_CODE = "version_code"
    VERSION_NAME = "version_name"

    def __init__(self) -> None:
        self._base = None
        self._message = None

    @staticmethod
    def parse(packet, address = None):
        plen = len(packet)
        if plen < 10:
            logger.trace("message length too short.")
            return

        start = packet[:9].decode("utf-8")
        # quanlan udp message
        if start != UDPMessage.START:
            return

        if not check_crc(packet):
            logger.warn(f"数据CRC校验失败，丢弃！")
            return
        
        # message command
        cmd = int.from_bytes(packet[10:12], 'little')

        return UDPMessage._parse(cmd, packet[12:])

    @staticmethod
    def _parse(cmd, data):
        # 只解析0x09
        if cmd == UDPCommand.NOTIFY.value:
            return UDPMessage.parseDeviceInfo(data)
        else:
            logger.trace(f'不支持的消息. cmd: {hex(cmd)} dlen: {len(data)} data: {data}')
            return None
        
    @staticmethod
    def parseDeviceInfo(data):
        devinfo = {}
        try:
            devinfo[UDPMessage.DEV_TYPE] = hex(int.from_bytes(data[:2], 'little'))
            devinfo[UDPMessage.MAC] = hex(int.from_bytes(data[2:10], 'little'))
            devinfo[UDPMessage.VERSION_CODE] = int.from_bytes(data[42:46], 'little')
            devinfo[UDPMessage.VERSION_NAME] = str(data[10:42],'utf-8').split('\x00')[0]
        except Exception as e:
            logger.error(f"parseDeviceInfo异常：{e}")

        return devinfo

    #devno是hex字符串
    @staticmethod
    def get_message(devno, tcp_port=19128):
        message = bytearray(28)
        message[:10] = UDPMessage.START.encode('utf-8')
        cmd = UDPCommand.CONNECT.value
        devtype = 0x0        
        # 本机ip
        ip = get_ip().split(".")
        
        message[10:12] = cmd.to_bytes(2, 'little')
        message[12:14] = devtype.to_bytes(2, 'little')
        message[14:22] = int(devno, 16).to_bytes(8, 'little')
        message[22] = (int)(ip[0])
        message[23] = (int)(ip[1])
        message[24] = (int)(ip[2])
        message[25] = (int)(ip[3])
        message[26:28] = tcp_port.to_bytes(2, 'little')
        checksum = crc16(message)

        return message + checksum.to_bytes(2, 'little')

class TCPMessage(object):
    start = 0xa55a

    @staticmethod
    def header(packet_type=2, dev_type=0, dev_id = 0):
        header = bytearray(12)
        header[:2] = TCPMessage.start.to_bytes(2, 'little')
        header[2] = packet_type
        header[3] = 42
        header[4:8] = dev_id.to_bytes(4, 'little')
        header[8:12] = int(16).to_bytes(4, 'little')

        return header

    @staticmethod
    def wrap(cmd, data=None):
        header = TCPMessage.header()
        if data:
            dlen = len(data) + 16
            header[8:12] = dlen.to_bytes(4, 'little')
            message = header + cmd.to_bytes(2, 'little') + data 
        else: 
            message = header + cmd.to_bytes(2, 'little')
        
        checksum = crc16(message)
        return message + checksum.to_bytes(2, 'little')
    
    @staticmethod
    def get_device_info():
        return TCPMessage.wrap(TCPCommand.GET_DEVICE_INFO.value)

    @staticmethod
    def trigger(type = 0):
        data = type.to_bytes(4, 'little')
        return TCPMessage.wrap(TCPCommand.TRIGGER.value, data)

    @staticmethod
    def wav_update_ready(id, len):
        data = bytearray(8)
        data[:4] = id.to_bytes(4, 'little')
        data[4:] = len.to_bytes(4, 'little')
        return TCPMessage.wrap(TCPCommand.WAV_UPDATE_READY.value, data)

    @staticmethod
    def wav_update(id, offset, len, content):
        data = bytearray(len + 12)
        data[:4] = id.to_bytes(4, 'little')
        data[4:8] = offset.to_bytes(4, 'little')
        data[8:12] = len.to_bytes(4, 'little')
        data[12:] = content
        return TCPMessage.wrap(TCPCommand.WAV_UPDATE.value, data)

    @staticmethod
    def wav_update_stop(id, md5sum):
        data = id.to_bytes(4, 'little')
        data += md5sum.encode("utf-8") + b'0x0' # 结尾符号解析
        return TCPMessage.wrap(TCPCommand.WAV_UPDATE_FINISH.value, data)

    @staticmethod
    def wav_trigger(id = 0, volumn = 2):
        data = bytearray(8)
        data[:4] = id.to_bytes(4, 'little')
        data[4:] = volumn.to_bytes(4, 'little')
        return TCPMessage.wrap(TCPCommand.WAV_TRIGGER.value, data) 

    @staticmethod
    def start_acquire():
        data = bytearray(8)
        data = int(time()).to_bytes(8, 'little')
        return TCPMessage.wrap(TCPCommand.START_ACQUIRE.value)

    @staticmethod
    def stop_acquire():
        return TCPMessage.wrap(TCPCommand.STOP_ACQUIRE.value)

    @staticmethod
    def set_paradigm(paradigm:dict):
        data = bytearray(68)
        logger.debug(paradigm);
        # 电流类型
        if 'waveform' in paradigm.keys():
            data[:4] = int(paradigm['waveform']).to_bytes(4, 'little')
        # 持续时间
        if 'duration' in paradigm.keys():
            data[4:8] = int(paradigm['duration']).to_bytes(4, 'little')
        # 停止时间
        if 'interval' in paradigm.keys():
            data[8:12] = int(paradigm['interval']).to_bytes(4, 'little')
        # 重复次数
        if 'repeat' in paradigm.keys():
            data[12:16] = int(paradigm['repeat']).to_bytes(4, 'little')
        # 最大电流
        if 'max_current' in paradigm.keys():
            data[16:20] = int(paradigm['max_current']).to_bytes(4, 'little')
        # 最小电流
        if 'min_current' in paradigm.keys():
            data[20:24] = int(paradigm['min_current']).to_bytes(4, 'little')
        # 频率
        if 'frequency' in paradigm.keys():
            data[24:28] = int(paradigm['frequency']).to_bytes(4, 'little')
        # 上升沿时间
        if 'ramp_up' in paradigm.keys():
            data[28:32] = int(paradigm['ramp_up']).to_bytes(4, 'little')
        # 下降沿时间
        if 'ramp_down' in paradigm.keys():
            data[32:36] = int(paradigm['ramp_down']).to_bytes(4, 'little')
        # 电刺激通道
        if 'channels' in paradigm.keys():
            data[36:40] = int(paradigm['channels']).to_bytes(4, 'little')
        # 范式类型
        if 'pardigm_type' in paradigm.keys():
            data[40:44] = int(paradigm['pardigm_type']).to_bytes(4, 'little')
        # 电极类型
        if 'electrode_type' in paradigm.keys():
            data[44:48] = int(paradigm['electrode_type']).to_bytes(4, 'little')
        # 扩展字段
        # if kwargs['extends']:
        #     data[20:24] = int(kwargs['extends']).to_bytes(4, 'little')
        # 范式Id
        if 'pardigm_id' in paradigm.keys():
            data[64:68] = int(paradigm['pardigm_id']).to_bytes(4, 'little')
            

        return TCPMessage.wrap(TCPCommand.SET_PARADIGM.value, data)