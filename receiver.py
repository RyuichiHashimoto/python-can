from src.interface import CANInterface

if __name__ == "__main__":
    interface = "can0"
    
    ifc = CANInterface(interface)
    print(ifc.receive_message(timeout=3))

