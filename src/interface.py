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
        

    def send_message(self, can_id: int, data: list[int]) -> None:
        timeout = 1.0
        with can.Bus(channel=self.interface, interface='socketcan') as bus:
            message = can.Message(arbitration_id=can_id, is_extended_id=True, data=data)
            bus.send(message, timeout=timeout)

    def receive_message(self, timeout: int = 5) -> bytes | None:
        
        try:
            with can.Bus(channel=self.interface, interface='socketcan') as bus:
                message = bus.recv(timeout=10.0)  # 10秒間待機
                return message
        except can.CanError as e:
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    interface = "can0"
    
    ifc = CANInterface(interface)

    # ifc.send_message(0x13, [0x14, 0xFF, 0x14])
    ifc.receive_message(timeout=3)









