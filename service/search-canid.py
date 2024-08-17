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
    
if __name__ == "__main__":
    
    time.sleep(0.5)

    start_can_id = 0x7E0
    finish_can_id = 0x7FF
    trial = 3
    interval = 0.1

    for send in range(start_can_id, finish_can_id):
        for recv in range(start_can_id, finish_can_id):
            if send == recv:
                continue
            send_canid = hex(send)[2:]
            recv_canid = hex(recv)[2:]
            
            process = create_background_recv_process(send_canid = send_canid, recv_canid= recv_canid)
            if (send%0x10)==0:
                print(f"The {hex(send)} trial starts")
        
            # ISO TP
            packet = [0x10, 0x00]

            for i in range(3):
                send_packet(packet, send_canid = send_canid, recv_canid= recv_canid)
                time.sleep(interval)

            if process.poll() is not None:
                stdout, stderr = process.communicate()
                print(f"{send_canid} and {recv_canid} is activated")

            process.kill()
            time.sleep(0.1)
                
                