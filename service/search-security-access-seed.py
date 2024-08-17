import os
import subprocess
import time

INTERFACE = "vcan0"
SENDER_CANID = "7E0"
RECIEVER_CANID = "7E8"
INTERVAL = 0.05

def send_packet(input_bytes_int: list[int], send_canid, recv_canid):
    input_bytes_str = [(hex(by)[2:]).zfill(2) for by in input_bytes_int]
    input_data = " ".join(input_bytes_str)
    subprocess.run(['isotpsend', '-s', send_canid, '-d', recv_canid, INTERFACE], input=input_data.encode())

def create_background_recv_process(send_canid, recv_canid):
    return subprocess.Popen(
        ['isotprecv', '-s', send_canid, '-d', recv_canid, INTERFACE],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
def hex_to_ascii(hex_string):
    # 16進数文字列をスペースで分割してリストにする
    hex_values = hex_string.split()
    
   # 16進数リストをアスキー文字列に変換
    ascii_string = ''.join([chr(int(h, 16)) for h in hex_values])
    
    return ascii_string.encode("utf-8")

def operator(message: str) -> list[int]:
    pass

def change_session_mode(session_mode: int, send_canid: str, recv_canid: str) -> bool:
    """ 
    ECUに問い合わて、チャレンジレスポンス用SEEDを取得する。

    parameter
    ---------
        security_level: int
        send_canid: str 送信側(i.e., テスター側)のcan_id
        recv_canid: str 受信側(i.e., 診断対象ECU側)のcan_id
    
    return 
    ------
        成功有無bool: 
            True: セッション変更に成功した。
            False: セッション変更に失敗した。
    """
        
    process = create_background_recv_process(send_canid = send_canid, recv_canid= recv_canid)
    time.sleep(INTERVAL)
    
    query_message = [0x10, session_mode]
    send_packet(query_message, send_canid = send_canid, recv_canid= recv_canid)
    
    time.sleep(INTERVAL)

    if process.poll() is not None:
        stdout, stderr = process.communicate()
        msg = stdout.decode("utf-8")
        if stderr:
            raise Exception(f"error has occured")
        
        response_msg = msg.split("\n")[0].strip()
        target_msg = response_msg.split(" ")

        if (target_msg[0] == "50") and (int(target_msg[1], base=16) == session_mode):
            return True
        else:
            raise Exception(f"error has occured: {' '.join(target_msg)}")
        
    else:
        return False

def send_and_recv_seed(security_level: int, send_canid: str, recv_canid: str) -> str:
    """ 
    ECUに問い合わせて、チャレンジレスポンスを実行する。

    parameter
    ---------
        security_level: int
        send_canid: str 送信側(i.e., テスター側)のcan_id
        recv_canid: str 受信側(i.e., 診断対象ECU側)のcan_id
    
    return 
    ------
        seed値    
    """
        
    process = create_background_recv_process(send_canid = send_canid, recv_canid= recv_canid)
    time.sleep(INTERVAL)
    
    query_message = [0x27, security_level]
    send_packet(query_message, send_canid = send_canid, recv_canid= recv_canid)
    
    time.sleep(INTERVAL)

    if process.poll() is not None:
        stdout, stderr = process.communicate()
        msg = stdout.decode("utf-8")
        if stderr:
            raise Exception(f"error has occured")
        
        response_msg = msg.split("\n")[0].strip()
        target_msg = response_msg.split(" ")

        if target_msg[0] == "7F":
            raise Exception(f"error has occured: {target_msg}")
        
        if (target_msg[0] == "67") and  (int(target_msg[1],base=16) == security_level):
            return " ".join(target_msg[2:])
        
    else:
        return "not_finish"


def send_and_recv_key(security_level: int, packet: list[int], send_canid: str, recv_canid: str) -> bool:
    """ 
    チャレンジレスポンス応答メッセージを送信して、応答に成功したか判定する。
    
    parameter
    ---------
        security_level: int
        send_canid: str 送信側(i.e., テスター側)のcan_id
        recv_canid: str 受信側(i.e., 診断対象ECU側)のcan_id
    
    return 
    ------
        False: 認証に失敗した。
        True: 認証に成功した。
    
    Exception
    -------
        想定外のエラーが出たため。
    """
    process = create_background_recv_process(send_canid = send_canid, recv_canid= recv_canid)    
    time.sleep(INTERVAL)
    
    query_message = [0x27, security_level] + packet
    send_packet(query_message, send_canid = send_canid, recv_canid= recv_canid)
    
    time.sleep(INTERVAL)

    if process.poll() is not None:
        stdout, stderr = process.communicate()
        msg = stdout.decode("utf-8")
        if stderr:
           raise Exception(f"error has occured")
       
        response_msg = msg.split("\n")[0].strip()
        target_msg = response_msg.split(" ")

        is_negative_response = target_msg[0] == "7F"
        
        if is_negative_response:
           if target_msg[2] == "35":
            return False
       
        is_target_sid = target_msg[0] == "67"
        is_target_security_level = int(target_msg[1],base=16) == security_level
        
        if is_target_sid and is_target_security_level:
            return True
        
        raise Exception(response_msg)
    
    else:
        return False

def hex_to_binary(hex_string):
    return ''.join(f'{int(hex_string[i:i+2], 16):08b}' for i in range(0, len(hex_string), 2))

def uds_challenge_response(session_mode: int, security_level: int, target_operator):
    change_session_mode(session_mode=session_mode, send_canid=SENDER_CANID, recv_canid=RECIEVER_CANID)
    time.sleep(INTERVAL)
    seed = send_and_recv_seed(security_level=security_level, send_canid=SENDER_CANID, recv_canid=RECIEVER_CANID)    
    return seed


if __name__ == "__main__":
    session_mode = 2
    security_level = 1
                    
    with open("result.txt", "a") as fout:
        for i in range(0, 100):
            ret = uds_challenge_response(session_mode, security_level, None)
            
            ret_list = ret.split(" ")
            for a in ret_list:
                print( hex_to_binary(a), end=" ")
            print()
            fout.write(f"{ret}\n")

    
    