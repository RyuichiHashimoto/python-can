from src.util.ascii import hex_to_ascii


if __name__ == "__main__":
    ecu_type_enum = ["P", "C", "B", "U"]
    
    byt = "3E 9F 01"

    splited_bytes = [i for i in byt.split(" ")]
    
    first_byte_value = int(splited_bytes[0], base=16)
    ecu_type_id = (first_byte_value & 0b11000000) >> 6 # 上位２ビット抽出
    rest_bit_value1 = (first_byte_value & 0b00110000) >> 4 # 上位２ビット抽出
    rest_bit_value2 = (first_byte_value & 0b00001111)

    rest_bit_value1 = hex(rest_bit_value1)[2:]
    rest_bit_value2 = hex(rest_bit_value2)[2:]
    print(rest_bit_value1, bin(first_byte_value))
        
    # print(bin(byte_list[0]), bin(byte_list[0] and 0b11000000))
    ecu_type = ecu_type_enum[ecu_type_id]
    
    print(f"{ecu_type}{rest_bit_value1}{rest_bit_value2}{splited_bytes[1]}-{splited_bytes[2]}")

    

    # print(hex_to_ascii(byt))
