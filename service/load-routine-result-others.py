import can
import time
import binascii

with can.Bus(interface='socketcan', channel='vcan0') as bus:
    bus.set_filters([{"can_id": 0x7E8, "can_mask": 0xFFF, "extended": False}])
    for i in range(0,0xFF):
        for j in range(0,0xFF):
            time.sleep(0.01)
            message = can.Message(arbitration_id=0x7E0, is_extended_id=False, dlc=8, data=[0x04, 0x31, 0x01, i, j, 0x00, 0x00, 0x00])
            bus.send(message, timeout=0.2)
            msg = bus.recv()
            result = binascii.hexlify(msg.data).decode('utf-8')
            if result == "037f3131":
                pass
            else:
                print("i: ",hex(i),"   j: ",hex(j))
