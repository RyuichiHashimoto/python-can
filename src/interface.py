from abc import ABC, abstractmethod
from enum import Enum, auto
import can
import time

class NICTypeEnum(Enum):
    IP = auto()
    CAN = auto()
    FlexRay = auto()    

class NetworkInterface(ABC):
    
    def __init__(self, interface: str, nic_type: NICTypeEnum):
        self.__interface = interface
        self.__nic_type = nic_type

    @property
    def interface(self) -> str:
        return self.__interface    
    
    @property
    def nic_type(self) -> NICTypeEnum:
        return self.__nic_type
    
    @abstractmethod
    def send_message(self, can_id: int, data: list[int]) -> None:
        """
        指定インターフェースからメッセージを送信する。
        
        parameter
        --------
            data: bytes
                送信予定のデータ                
        """
        raise NotImplementedError
        
    @abstractmethod
    def receive_message(self, timeout: int = 5) -> bytes | None:
        """
        指定インターフェースからメッセージを送信する。
        
        parameter
        ---------
            timeout: int
                タイムアウト（秒）
        
        return
        -------
            受信したデータ
        
        raise 
        -----
            タイムアウトが発生した場合
        """
        raise NotImplementedError


class CANInterface(NetworkInterface):

    def __init__(self, interface: str):       
        super().__init__(interface, NICTypeEnum.CAN)
        self.__already_shutdownd = False
        self.__bus = can.Bus(channel=self.interface, interface='socketcan') 
        
    def __del__(self):
        if self.__already_shutdownd:
            return
        
        self.shutdown()

    def shutdown(self):
        self.__bus.shutdown()
        self.__already_shutdownd = True
        

    def send_message(self, can_id: int, data: list[int]) -> None:
        timeout = 1.0
        message = can.Message(arbitration_id=can_id, is_extended_id=True, data=data)
        self.__bus.send(message, timeout=timeout)

    def receive_message(self, can_id: int = None, timeout: int = 10) -> can.Message | None:
        start_time = time.time()
            
        rest_timeout = timeout
        while True:
            message = self.__bus.recv(rest_timeout)
            if message is None:
                return None
                        
            if can_id is None:
                return message
            
            if message.arbitration_id == can_id:
                return message
            
            elapsed_time = time.time() - start_time
            if elapsed_time > timeout:
                return None
            rest_timeout = timeout - elapsed_time

if __name__ == "__main__":
    interface = "can0"
    
    ifc = CANInterface(interface)

    # ifc.send_message(0x13, [0x14, 0xFF, 0x14])
    ifc.receive_message(timeout=3)









