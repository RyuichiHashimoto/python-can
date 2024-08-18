import can
from can import Message
from collections import defaultdict

if __name__ == "__main__":
    
    can_interface = "can0"


    timestamp_dict: dict[int, list[int]][dict,] = defaultdict(list[int])
    with can.interface.Bus(can_interface, bustype='socketcan') as bus:
        try:
            while True:
                message: can.Message = bus.recv()
                # dd = 
               
                can_id = message.arbitration_id
                timestamp = message.timestamp

                timestamp_dict[can_id].append(timestamp)

        except KeyboardInterrupt:
            pass

    
    for key,item in timestamp_dict.items():
        print(hex(key), item)


    
