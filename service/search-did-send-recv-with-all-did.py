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

INTERFACE = "vcan0"
SENDER_CANID = "7E0"
RECIEVER_CANID = "7E8"
INTERVAL = 0.1
RETRY = 2
if __name__ == "__main__":
    
    for f in range(0x00, 0xFF + 1):
        for s in range(0x00, 0xFF + 1):
            
            is_break = False
            packet = [0x10, 0x01]
            send_packet(packet, send_canid=SENDER_CANID, recv_canid=RECIEVER_CANID)

            process = create_background_recv_process(send_canid = SENDER_CANID, recv_canid= RECIEVER_CANID)
            time.sleep(INTERVAL)
            
            packet = [0x22, s, f]

            for i in range(RETRY):
                send_packet(packet, send_canid=SENDER_CANID, recv_canid=RECIEVER_CANID)
                time.sleep(INTERVAL)
            
            if process.poll() is not None:
                stdout, stderr = process.communicate()
                msg = stdout.decode("utf-8")
                if stderr:
                    raise Exception(f"error has occured in {i}")
                
                response_msg = msg.split("\n")[0].strip()
                
                target_msg = response_msg.split(" ")

                if target_msg[0] == "62":
                    print(packet)
                    print(" ".join(target_msg))
                else:
                    pass
                
                is_break = True
                break

        if not is_break:
            raise Exception("not capture")
