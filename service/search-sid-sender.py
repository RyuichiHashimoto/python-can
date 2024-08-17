import can
import threading
import time
import argparse

# CANインターフェースを設定
# コマンドライン引数を解析


if __name__ == "__main__":
    can_interface = 'vcan0'
    sender_send_target_device_canid = 0x7E0
    reciever_send_target_device_canid = 0x7E8
    interval = 0.1
    bus = can.interface.Bus(can_interface, bustype='socketcan')
    
    retry = 1
    can_id = sender_send_target_device_canid

    
    for _ in range(retry):
        for i in range(0x00, 0xFF + 1):
            data = [0x02, i, 0x00]
            message = can.Message(arbitration_id=can_id, data=data, is_extended_id=False)
            time.sleep(interval)
            bus.send(message)  # メッセージを送信

