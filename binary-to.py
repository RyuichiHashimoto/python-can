

def binaryTxt2bin(input_file: str, outputfile: str):

    # hex_to_bin.py
    with open(input_file, 'r') as f:
        hex_data = f.read().strip()

    # print()
    hex_data = hex_data.replace(" ", "")
    # 16進数の文字列をバイトデータに変換
    bin_data = bytes.fromhex(hex_data)

    # バイナリファイルに書き出し
    with open(outputfile, 'wb') as f:
        f.write(bin_data)

if __name__ == "__main__":
    binaryTxt2bin("binary-hexdump.txt", "binary.bin")