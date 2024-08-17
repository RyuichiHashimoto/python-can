from src.interface import CANInterface

if __name__ == "__main__":
    interface = "can0"
    
    ifc = CANInterface(interface)
    ifc.send_message(0x141, [0x14, 51, 0xFF, 0x21])
