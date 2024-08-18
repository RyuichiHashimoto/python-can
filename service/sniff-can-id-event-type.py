import can
from can import Message
from collections import defaultdict
import numpy as np

def int_to_hex_string(value):
    return f"0x{value:03x}".upper()

if __name__ == "__main__":
    
    can_interface = "can0"

    print("first sniffing...")
    canid_set1 = set()
    with can.interface.Bus(can_interface, bustype='socketcan') as bus:
        try:
            while True:
                message: can.Message = bus.recv()
                can_id = int_to_hex_string(message.arbitration_id)
                canid_set1.add(can_id)
        
        except KeyboardInterrupt:
            pass

    print("second sniffing...")
    canid_set2 = set()
    with can.interface.Bus(can_interface, bustype='socketcan') as bus:
        try:
            while True:
                message: can.Message = bus.recv()
                can_id = int_to_hex_string(message.arbitration_id)
                canid_set2.add(can_id)
        
        except KeyboardInterrupt:
            pass
    

    print(f'----------[can_id list in first interval]-------------')
    print( ", ".join(sorted(list(canid_set1))))

    print(f'----------[can_id list in second interval]-------------')
    print( ", ".join(sorted(list(canid_set2))))

    print(f'----------[cCAN ID set confirmed only in the first interval]-------------')
    ret_set1 = canid_set1 - canid_set2
    print( ", ".join(sorted(list(ret_set1))))

    print(f'----------[cCAN ID set confirmed only in the second interval]-------------')
    ret_set2 = canid_set2 - canid_set1
    print( ", ".join((list(ret_set2))))
