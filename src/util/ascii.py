def hex_to_ascii(hex_string):
    # 16進数文字列をスペースで分割してリストにする
    hex_values = hex_string.split()
    
    # 16進数リストをアスキー文字列に変換
    ascii_string = ''.join([chr(int(h, 16)) for h in hex_values])
    
    return ascii_string.encode("utf-8")