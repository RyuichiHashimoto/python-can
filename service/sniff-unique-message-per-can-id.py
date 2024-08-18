import can
from can import Message
from collections import defaultdict

def int_to_hex_string(value):
    return f"0x{value:03x}".upper()

if __name__ == "__main__":
    
    can_interface = "can0"

    print("sniffing...")
    message_dict: dict[int, set[list[int]]] = defaultdict(set[list[int]])
    with can.interface.Bus(can_interface, bustype='socketcan') as bus:
        try:
            while True:
                message: can.Message = bus.recv()
                
                can_id = message.arbitration_id
                
                message_dict[can_id].append(message.data)

        except KeyboardInterrupt:
            pass

    
    for key,item in message_dict.items():        
        canid = int_to_hex_string(key)
        
        print(f"can id: {canid}  unique message: {int(len(item))}")
