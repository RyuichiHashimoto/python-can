import can

def receive_messages(bus, can_id: int) -> tuple[set, set]:
    valid_set = set(["-1"])
    valid_with_security_set = set(["-1"])
    invalid_set = set(["-1"])
    unknown_set = set([hex(i) for i in range(0x00, 0xFF)])

    try:
        while True:
            message = bus.recv()  # メッセージを受信
            if message is None:
                continue
            
            if message.arbitration_id == can_id:
                
                
                response = int(message.data[1])
                sid = int(message.data[2])
                error_code = None
                if response == 0x7F:
                    error_code = int(message.data[3])
                                
                if response == 0x50:
                    valid_set.add(hex(sid))
                elif (response == 0x7F) and (error_code == 0x33):
                    valid_with_security_set.add(hex(sid))
                elif (response == 0x7F) and (error_code == 0x12):
                    invalid_set.add(hex(sid))
                else:
                    unknown_set.add(hex(sid))

    
    except KeyboardInterrupt:
        rest_set = unknown_set - (valid_set | invalid_set | valid_with_security_set)
        invalid_set = invalid_set - valid_set
        invalid_set = invalid_set - valid_with_security_set
        print("-----------[valid sid]---------")
        print(", ".join(sorted(list(valid_set))))
        print("-----------[valid with security sid]---------")
        print(", ".join(sorted(list(valid_with_security_set))))
        print("-----------[invalid sid]---------")
        print(", ".join(sorted(list(invalid_set))))
        print("-----------[unknown sid]---------")
        print(", ".join(sorted(list(rest_set))))

        bus.shutdown()

                
if __name__ == "__main__":
    # CANインターフェースを設定
# コマンドライン引数を解析
    can_interface = 'vcan0'
    sender_send_target_device_canid = 0x7E0
    reciever_send_target_device_canid = 0x7E8
    interval = 0.1
    bus = can.interface.Bus(can_interface, bustype='socketcan')

    receive_messages(bus, reciever_send_target_device_canid)


    