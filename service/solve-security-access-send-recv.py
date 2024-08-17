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


def uds_challenge_response(session_mode: int, security_level: int, target_operator):
    change_session_mode(session_mode=session_mode, send_canid=SENDER_CANID, recv_canid=RECIEVER_CANID)
    time.sleep(INTERVAL)
    seed = send_and_recv_seed(security_level=security_level, send_canid=SENDER_CANID, recv_canid=RECIEVER_CANID)    
    time.sleep(INTERVAL)
    message = target_operator(seed)
    is_success = send_and_recv_key(security_level=security_level + 1, packet = message, send_canid=SENDER_CANID, recv_canid=RECIEVER_CANID)
    
    return is_success


def msg_to_listint(msg: str) -> list[int]:
    return [ int(key, base=16) for key in msg.split(" ")]

def dummy_operator(seed: str) -> list[int]:
    return [0x00, 0x00]

def bit_inverse(seed: str) -> list[int]:
    return xor_operator_each_bytes(seed, 0xFF)

def xor_operator_each_bytes(seed: str, xor_operand: int):
    splited_seed = msg_to_listint(seed)
    return [xor_operand ^ key for key in splited_seed]

def xor_operator_each_bytes(seed: str, xor_operand: int):
    splited_seed = msg_to_listint(seed)
    return [xor_operand ^ key for key in splited_seed]

def xor_operator_all_bytes(seed: str, xor_operand_list: list[int]):
    splited_seed = msg_to_listint(seed)
    return [xor_operand ^ key for xor_operand, key in zip(xor_operand_list, splited_seed)]

def xor_operator_parts_bytes(seed: str, xor_operand_list: list[int]):
    splited_seed = msg_to_listint(seed)

    ret = []
    for idx,key in enumerate(splited_seed):
        ret.append(key ^ xor_operand_list[ idx % len(xor_operand_list)])

    return ret


if __name__ == "__main__":
    session_mode = 2
    security_level = 1

    basic_operator_list = [bit_inverse]
    
    for target_operator in basic_operator_list:
        if uds_challenge_response(session_mode, security_level, target_operator):
            print(target_operator.__name__)
            os._exit(0)

    xor_operand_list = []
    xor_operand_list = list([ i  for i in range(0x00, 0xFF+1)])
    for operand in xor_operand_list:
        if uds_challenge_response(session_mode, security_level, lambda x: xor_operator_each_bytes(x, operand)):
            print(xor_operator_each_bytes.__name__, operand)
            os._exit(0)
    
    
