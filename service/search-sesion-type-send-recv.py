import subprocess
import time

interface = "vcan0"

def send_packet(input_bytes_int: list[int], send_canid, recv_canid):
    input_bytes_str = [(hex(by)[2:]).zfill(2) for by in input_bytes_int]
    input_data = " ".join(input_bytes_str)
    
    # subprocess.callで標準入力を渡す
    subprocess.run(['isotpsend', '-s', send_canid, '-d', recv_canid, interface], input=input_data.encode())

def create_background_recv_process(send_canid, recv_canid):
    return subprocess.Popen(
        ['isotprecv', '-s', send_canid, '-d', recv_canid, interface],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
def hex_to_ascii(hex_string):
    # 16進数文字列をスペースで分割してリストにする
    hex_values = hex_string.split()
    
    # 16進数リストをアスキー文字列に変換
    ascii_string = ''.join([chr(int(h, 16)) for h in hex_values])
    
    return ascii_string.encode("utf-8")

if __name__ == "__main__":
    
    time.sleep(0.5)

    sender_canid = "7E0"
    reciever_canid = "7E8"

    start_byte = 0x00
    end_byte = 0xFF
    trial = 2
    interval = 0.05

    valid_set = set(["-1"])
    invalid_set = set(["-1"])
    unknown_set = set([hex(i) for i in range(0x00, 0xFF)])

    activate_list = []
    activate_but_security = []
    inactivate_list = []
    unknown_list = []
    
    for byt in range(start_byte, end_byte + 1):
        process = create_background_recv_process(send_canid = sender_canid, recv_canid= reciever_canid)
        time.sleep(interval)
        if (byt%0x10)==0:
            print(f"The {hex(byt)} trial starts")
    
        # ISO TP
        packet = [0x10, byt]

        for i in range(trial):
            send_packet(packet, send_canid = sender_canid, recv_canid= reciever_canid)
            time.sleep(interval)

        if process.poll() is not None:
            stdout, stderr = process.communicate()
            msg = stdout.decode("utf-8")
            if stderr:
                raise Exception(f"error has occured in {i}")
            
            response_msg = msg.split("\n")[0].strip()
            
            target_msg = response_msg.split(" ")

            if target_msg[0] == "50":
                activate_list.append(hex(byt))
            elif (target_msg[0] == "7F") and (target_msg[2] == "33"):
                activate_but_security.append(hex(byt))
            elif (target_msg[0] == "7F") and (target_msg[2] == "12"):
                inactivate_list.append(hex(byt))
            else:
                unknown_list.append(hex(byt))
                                
        process.kill()
        time.sleep(interval)

    print("-----------[activate session]---------")
    print(", ".join(activate_list))
    print("-----------[activate session with security]---------")
    print(", ".join(activate_but_security))
    print("-----------[inactivate_list sesison]---------")
    print(", ".join(inactivate_list))
    print("-----------[unknown_list sesison]---------")
    print(", ".join(unknown_list))
    
            
            