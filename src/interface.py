from abc import ABC, abstractmethod
from enum import Enum, auto
import can

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
    def receive_message(self, timeout: int = 5) -> bytes:
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
        return super().__init__(interface, NICTypeEnum.CAN)

    def send_message(self, can_id: int, data: list[int]) -> None:
        print("send")
        pass

    def receive_message(self, timeout: int = 5) -> bytes:
        print("recv")
        pass


if __name__ == "__main__":
    interface = "can0"
    
    ifc = CANInterface(interface)

    with can.Bus(channel=interface, interface='socketcan') as bus:
        message = can.Message(arbitration_id=123, is_extended_id=True, data=[0x11, 0x22, 0x33])
        bus.send(message, timeout=0.2)








