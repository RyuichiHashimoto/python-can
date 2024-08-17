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

class DID():

    def __init__(self, number: str, name: str, description: str):
        self._number = number
        self._name = name
        self._description = description

    @property
    def is_range_did(self):
        return  "-" in self._number
    
    @property
    def number(self) -> str:
        return self._number
    
    @property
    def number_as_listint(self) -> list[int]:
        hex_str = self._number[2:]
        if len(hex_str) %2 != 0:
            hex_str = "0" + hex_str

        byte_list = [int(hex_str[i:i+2], 16) for i in range(0, len(hex_str), 2)]
        return byte_list
        
    @property
    def name(self):
        return self._name
    
    @property
    def description(self):
        return self._name


class ISOSAE_Reserved(DID):
    def __init__(self):
        super().__init__("0x0000–0x00FF", "ISO SAE Reserved", "This range of values shall be reserved by this document for future definition.")

class VehicleManufacturerSpecific1(DID):
    def __init__(self):
        super().__init__("0x0100–0xA5FF", "Vehicle Manufacturer Specific", "This range of values shall be used to reference vehicle manufacturer specific record data identifiers and input/output identifiers within the server.requirements.")

class ReservedForLegislativeUse1(DID):
    def __init__(self):
        super().__init__("0xA600–0xA7FF", "Reserved For Legislative Use", "This range of values is reserved for future legislative requirements.")

class VehicleManufacturerSpecific2(DID):
    def __init__(self):
        super().__init__("0xA800–0xACFF", "Vehicle Manufacturer Specific", "This range of values shall be used to reference vehicle manufacturer specific record data identifiers and input/output identifiers within the server.")

class ReservedForLegislativeUse2(DID):
    def __init__(self):
        super().__init__("0xAD00–0xAFFF", "Reserved For Legislative Use", "This range of values is reserved for future legislative requirements.")

class VehicleManufacturerSpecific3(DID):
    def __init__(self):
        super().__init__("0xB000–0xB1FF", "Vehicle Manufacturer Specific", "This range of values shall be used to reference vehicle manufacturer specific record data identifiers and input/output identifiers within the server.")

class ReservedForLegislativeUse3(DID):
    def __init__(self):
        super().__init__("0xB200–0xBFFF", "Reserved For Legislative Use", "This range of values is reserved for future legislative requirements.")

class VehicleManufacturerSpecific4(DID):
    def __init__(self):
        super().__init__("0xC000–0xC2FF", "Vehicle Manufacturer Specific", "This range of values shall be used to reference vehicle manufacturer specific record data identifiers and input/output identifiers within the server.")

class ReservedForLegislativeUse4(DID):
    def __init__(self):
        super().__init__("0xC300–0xCEFF", "Reserved For Legislative Use", "This range of values is reserved for future legislative requirements.")

class VehicleManufacturerSpecific5(DID):
    def __init__(self):
        super().__init__("0xCF00–0xEFFF", "Vehicle Manufacturer Specific", "This range of values shall be used to reference vehicle manufacturer specific record data identifiers and input/output identifiers within the server.")

class NetworkConfigurationDataForTractorTrailer(DID):
    def __init__(self):
        super().__init__("0xF000–0xF00F", "Network Configuration Data For Tractor Trailer Application Data Identifier", "This value shall be used to request the remote addresses of all trailer systems independent of their functionality.")

class VehicleManufacturerSpecific6(DID):
    def __init__(self):
        super().__init__("0xF010–0xF0FF", "Vehicle Manufacturer Specific", "This range of values shall be used to reference vehicle manufacturer specific record data identifiers and input/output identifiers within the server.")

class IdentificationOptionVehicleManufacturerSpecific(DID):
    def __init__(self):
        super().__init__("0xF100–0xF17F", "Identification Option Vehicle Manufacturer Specific Data Identifier", "This range of values shall be used for vehicle manufacturer specific server/vehicle identification options.")

class BootSoftwareIdentification(DID):
    def __init__(self):
        super().__init__("0xF180", "Boot Software Identification Data Identifier", 
                         "The vehicle manufacturer’s specific ECU boot software identification record will be referenced using this value. The record data’s first byte will indicate the number of reported modules. The boot software identification(s) will be listed after the number of modules. The ECU-specific format of the boot software identification structure is determined by the vehicle manufacturer.")

class ApplicationSoftwareIdentification2(DID):
    def __init__(self):
        super().__init__("0xF181", "Application Software Identification Data Identifier", 
                         "The vehicle manufacturer’s specific ECU application software numbers will be referenced using this value. The record data’s first byte will indicate the number of reported modules. The application software identification(s) will be listed after the number of modules. The ECU-specific format of the application software identification structure is determined by the vehicle manufacturer.")

class ApplicationDataIdentification(DID):
    def __init__(self):
        super().__init__("0xF182", "Application Data Identification Data Identifier", 
                         "The vehicle manufacturer’s specific ECU application data identification record will be referenced using this value. The record data’s first byte will indicate the number of reported modules. The application data identification(s) will be listed after the number of modules. The ECU-specific format of the application data identification structure is determined by the vehicle manufacturer.")

class BootSoftwareFingerprint(DID):
    def __init__(self):
        super().__init__("0xF183", "Boot Software Finger-print Data Identifier", 
                         "This value shall be used to reference the vehicle manufacturer-specific ECU boot software fingerprint identification record. The format of the recorded data, which will be specific to the ECU, shall be defined by the vehicle manufacturer.")

class ApplicationSoftwareFingerprint(DID):
    def __init__(self):
        super().__init__("0xF184", "Application Software Fingerprint Data Identifier", 
                         "The vehicle manufacturer’s specific ECU application software fingerprint identification record will be referenced using this value. The record data’s content and format is determined by the vehicle manufacturer and is specific to the ECU.")

class ApplicationDataFingerprint(DID):
    def __init__(self):
        super().__init__("0xF185", "Application Data Fingerprint Data Identifier", 
                         "The vehicle manufacturer’s specific ECU application data fingerprint identification record will be referenced using this value. The record data’s content and format is determined by the vehicle manufacturer and is specific to the ECU.")

class ActiveDiagnosticSession(DID):
    def __init__(self):
        super().__init__("0xF186", "Active Diagnostic Session Data Identifier", 
                         "This value will be used to indicate the current active diagnostic session on the server. The specific session type will be defined by the 'diagnosticSessionType' subfunction parameter in the DiagnosticSessionControl service.")

class VehicleManufacturerSparePartNumber(DID):
    def __init__(self):
        super().__init__("0xF187", "Vehicle Manufacturer Spare Part Number Data Identifier", 
                         "This value will be used to reference the vehicle manufacturer’s specific spare part number. The record data’s content and format is determined by the server and is specific to the vehicle manufacturer.")

class VehicleManufacturerECUSoftwareNumber(DID):
    def __init__(self):
        super().__init__("0xF188", "Vehicle Manufacturer ECU Software Number Data Identifier", 
                         "This value will be used to reference the vehicle manufacturer’s specific spare part number. The record data’s content and format is determined by the server and is specific to the vehicle manufacturer.")

class VehicleManufacturerECUSoftwareVersionNumber(DID):
    def __init__(self):
        super().__init__("0xF189", "Vehicle Manufacturer ECU Software Version Number Data Identifier", 
                         "This value will be used to reference the vehicle manufacturer’s specific ECU (server) software version number. The record data’s content and format is determined by the server and is specific to the vehicle manufacturer.")

class SystemSupplierIdentifier(DID):
    def __init__(self):
        super().__init__("0xF18A", "System Supplier Identifier Data Identifier", 
                         "This value will be used to reference the system supplier’s name and address information. The record data’s content and format is determined by the server and is specific to the system supplier.")

class ECUMfgDate(DID):
    def __init__(self):
        super().__init__("0xF18B", "ECU Manufacturing Date Data Identifier", 
                         "This value will be used to reference the ECU (server) manufacturing date. The record data will be in the form of an unsigned numeric, ASCII or BCD format, and will be arranged in the order of Year, Month, Day.")

class ECUSerialNumber(DID):
    def __init__(self):
        super().__init__("0xF18C", "ECU Serial Number Data Identifier", 
                         "This value will be used to reference the ECU (server) serial number. The record data’s content and format is determined by the server.")

class SupportedFunctionalUnits(DID):
    def __init__(self):
        super().__init__("0xF18D", "Supported Functional Units Data Identifier", 
                         "This value will be used to request the functional units that are implemented in a server.")

class VehicleIdentifierKitAssemblyPartNumber(DID):
    def __init__(self):
        super().__init__("0xF18E", "Vehicle Identifier Manufacturer Kit Assembly Part Number Data", 
                         "This value will be used to reference the vehicle manufacturer’s order number for a kit, which is a collection of assembled parts purchased as a whole for production, such as a cockpit. The spare part number only designates the server, as in the case of after-sales. The record data’s content and format is determined by the server and is specific to the vehicle manufacturer.")

class ISOSAE_ReservedStandardized(DID):
    def __init__(self):
        super().__init__("0xF18F", "ISO SAE Reserved Standardized", 
                         "This range of values shall be reserved by this document for future definition of standardized server/vehicleIdentification options.")

class VIN(DID):
    def __init__(self):
        super().__init__("0xF190", "VIN Data Identifier", 
                         "This value shall be used to reference the VIN number. Record data content and format shall be specified by the vehicle manufacturer.")

class VehicleManufacturerECUHardwareNumber(DID):
    def __init__(self):
        super().__init__("0xF191", "Vehicle Manufacturer ECU Hardware Number Data Identifier", 
                         "This value will be used by reading services to reference the vehicle manufacturer’s specific ECU (server) hardware number. The record data’s content and format is determined by the server and is specific to the vehicle manufacturer.")

class SystemSupplierECUHardwareNumber(DID):
    def __init__(self):
        super().__init__("0xF192", "System Supplier ECU Hardware Number Data Identifier", 
                         "This value shall be used to reference the system supplier specific ECU (server) hardware number. Record data content and format shall be server specific and defined by the system supplier.")

class SystemSupplierECUHardwareVersionNumber(DID):
    def __init__(self):
        super().__init__("0xF193", "System Supplier ECU Hardware Version Number Data Identifier", 
                         "This value shall be used to reference the system supplier specific ECU (server) hardware version number. Record data content and format shall be server specific and defined by the system supplier.")

class SystemSupplierECUSoftwareNumber(DID):
    def __init__(self):
        super().__init__("0xF194", "System Supplier ECU Software Number Data Identifier", 
                         "This value will be used to reference the system supplier’s specific ECU (server) software number. The record data’s content and format is determined by the server and is specific to the system supplier.")

class SystemSupplierECUSoftwareVersionNumber(DID):
    def __init__(self):
        super().__init__("0xF195", "System Supplier ECU Software Version Number Data Identifier", 
                         "This value shall be used to reference the system supplier specific ECU (server) software version number. Record data content and format shall be server specific and defined by the system supplier.")

class ExhaustRegulationOrTypeApprovalNumber(DID):
    def __init__(self):
        super().__init__("0xF196", "Exhaust Regulation Or Type Approval Number Data Identifier", 
                         "This value shall be used to reference the exhaust regulation or type approval number (valid for those systems which require type approval). Record data content and format shall be server specific and defined by the vehicle manufacturer. Refer to the relevant legislation for any applicable requirements.")

class SystemNameOrEngineType(DID):
    def __init__(self):
        super().__init__("0xF197", "System Name Or Engine Type Data Identifier", 
                         "This value will be used to reference the system name or engine type. The record data’s content and format is determined by the server and is specific to the vehicle manufacturer.")

class RepairShopCodeOrTesterSerialNumber(DID):
    def __init__(self):
        super().__init__("0xF198", "Repair Shop Code Or Tester Serial Number Data Identifier", 
                         "This value shall be used to reference the repair shop code or tester (client) serial number (e.g., to indicate the most recent service client used re-program server memory). Record data content and format shall be server specific and defined by the vehicle manufacturer.")

class ProgrammingDate(DID):
    def __init__(self):
        super().__init__("0xF199", "Programming Date Data Identifier", 
                         "The date of the last programming of the server shall be referenced using this value. The format of the recorded data shall be unsigned numeric, ASCII or BCD, and the order shall be Year, Month, Day.")

class CalibrationRepairShopCodeOrCalibrationEquipmentSerialNumber(DID):
    def __init__(self):
        super().__init__("0xF19A", "Calibration Repair Shop Code Or Calibration Equipment Serial Number", 
                         "The repair shop code or client serial number for the most recent calibration service shall be referenced using this value. The format of the recorded data, which will be specific to the server, shall be defined by the vehicle manufacturer.")

class CalibrationDate(DID):
    def __init__(self):
        super().__init__("0xF19B", "Calibration Date Data Identifier", 
                         "The date of the last calibration of the server shall be referenced using this value. The format of the recorded data shall be unsigned numeric, ASCII or BCD, and the order shall be Year, Month, Day.")

class CalibrationEquipmentSoftwareNumber(DID):
    def __init__(self):
        super().__init__("0xF19C", "Calibration Equipment Software Number Data Identifier", 
                         "The software version used by the client to calibrate the server shall be referenced using this value. The format of the recorded data, which will be specific to the server, shall be defined by the vehicle manufacturer.")

class ECUInstallationDate(DID):
    def __init__(self):
        super().__init__("0xF19D", "ECU Installation Date Data Identifier", 
                         "The date of the ECU (server) installation in the vehicle shall be referenced using this value. The format of the recorded data shall be either unsigned numeric, ASCII or BCD, and the order shall be Year, Month, Day.")

class ODXFile(DID):
    def __init__(self):
        super().__init__("0xF19E", "ODX File Data Identifier", 
                         "This value shall be used to reference the ODX (Open Diagnostic Data Exchange) file that will be used to interpret and scale the server data.")

class Entity(DID):
    def __init__(self):
        super().__init__("0xF19F", "Entity Data Identifier", 
                         "This value shall be used to reference the entity data identifier for a secured data transmission.")

class IdentificationOptionVehicleManufacturerSpecific2(DID):
    def __init__(self):
        super().__init__("0xF1A0–0xF1EF", "Identification Option Vehicle Manufacturer Specific", 
                         "This range of values shall be used to identify the server/vehicle options that are specific to the vehicle manufacturer.")

class IdentificationOptionSystemSupplierSpecific(DID):
    def __init__(self):
        super().__init__("0xF1F0–0xF1FF", "Identification Option System Supplier Specific", 
                         "This range of values shall be used to identify the server/vehicle system options that are specific to the system supplier.")

class Periodic(DID):
    def __init__(self):
        super().__init__("0xF200–0xF2FF", "Periodic Data Identifier", 
                         "This range of values shall be used to reference periodic record data identifiers. Those can either be statically or dynamically defined.")

class DynamicallyDefined(DID):
    def __init__(self):
        super().__init__("0xF300–0xF3FF", "Dynamically Defined Data Identifier", 
                         "This range of values shall be used for dynamically defined data identifiers.")

class OBDData1(DID):
    def __init__(self):
        super().__init__("0xF400–0xF4FF", "OBD Data Identifier", 
                         "This range of values is reserved for OBD/EOBD PIDs as defined in ISO 15031-5.")

class OBDData2(DID):
    def __init__(self):
        super().__init__("0xF500–0xF5FF", "OBD Data Identifier", 
                         "This range of values is reserved to represent future defined OBD/EOBD PIDs.")

class OBDMonitorData1(DID):
    def __init__(self):
        super().__init__("0xF600–0xF6FF", "OBD Monitor Data Identifier", 
                         "This range of values is reserved for the result values of OBD/EOBD on-board monitoring as defined in ISO 15031-5.")

class OBDMonitorData2(DID):
    def __init__(self):
        super().__init__("0xF700–0xF7FF", "OBD Monitor Data Identifier", 
                         "This range of values is reserved to represent future defined result values of OBD/EOBD on-board monitoring.")

class OBDInfoType(DID):
    def __init__(self):
        super().__init__("0xF800–0xF8FF", "OBD Info Type Data Identifier", 
                         "This range of values is reserved for OBD/EOBD info type values as defined in ISO 15031-5.")

class Tachograph(DID):
    def __init__(self):
        super().__init__("0xF900–0xF9FF", "Tachograph Data Identifier", 
                         "This range of values is reserved for Tachograph Data Identifiers (DIDs) as defined in ISO 16844-7.")

class AirbagDeployment(DID):
    def __init__(self):
        super().__init__("0xFA00–0xFA0F", "Airbag Deployment Data Identifier", 
                         "This range of values is reserved for end of life activation of on-board pyrotechnic devices as defined in ISO 26021-2.")

class NumberOfEDRDevices(DID):
    def __init__(self):
        super().__init__("0xFA10", "Number Of EDR Devices", 
                         "This value shall be used to report the number of Event Data Recorder (EDR) devices that are capable of reporting EDR data.")

class EDRIdentification(DID):
    def __init__(self):
        super().__init__("0xFA11", "EDR Identification", 
                         "This value shall be used to report the identification data of the Event Data Recorder (EDR).")

class EDRDeviceAddressInformation(DID):
    def __init__(self):
        super().__init__("0xFA12", "EDR Device Address Information", 
                         "This value shall be used to report the EDR device address information according to the format defined in ISO 26021-2 for the dataIdentifier 0xFA02.")

class EDREntries(DID):
    def __init__(self):
        super().__init__("0xFA13–0xFA18", "EDR Entries", 
                         "This range shall be be used to report individual EDR entries. Each DID shall represent a single EDR entry with 0xFA13 representing the latest EDR entry.")

class SafetySystem(DID):
    def __init__(self):
        super().__init__("0xFA19–0xFAFF", "Safety System Data Identifier", 
                         "This range of values is reserved to represent safety system related DIDs.")

class ReservedForFutureLegislativeRequirements(DID):
    def __init__(self):
        super().__init__("0xFB00–0xFCFF", "Reserved For Future Legislative Requirements", 
                         "This range of values is reserved for future legislative requirements.")

class SystemSupplierSpecific(DID):
    def __init__(self):
        super().__init__("0xFD00–0xFEFF", "System Supplier Specific", 
                         "This range of values shall be used to reference the record data identifiers and input/output identifiers within the server that are specific to the system supplier.")

class UDSVersion(DID):
    def __init__(self):
        super().__init__("0xFF00", "UDS Version Data Identifier", 
                         "This value shall be used to reference the version of UDS (Unified Diagn Services) implemented in the server. The scaling of this Data Identifier (DID) can be found in Table C.11.")

class ISOSAE_Reserved1(DID):
    def __init__(self):
        super().__init__("0xFF01–0xFFFF", "ISO SAE Reserved", 
                         "This range of values shall be reserved by this document for future definition.")

DID_LIST = [
    # ISOSAE_Reserved(),
    # VehicleManufacturerSpecific1(),
    # ReservedForLegislativeUse1(),
    # VehicleManufacturerSpecific2(),
    # ReservedForLegislativeUse2(),
    # VehicleManufacturerSpecific3(),
    # ReservedForLegislativeUse3(),
    # VehicleManufacturerSpecific4(),
    # ReservedForLegislativeUse4(),
    # VehicleManufacturerSpecific5(),
    # NetworkConfigurationDataForTractorTrailer(),
    # VehicleManufacturerSpecific6(),
    # IdentificationOptionVehicleManufacturerSpecific(),
    BootSoftwareIdentification(),
    ApplicationSoftwareIdentification2(),
    ApplicationDataIdentification(),
    BootSoftwareFingerprint(),
    ApplicationSoftwareFingerprint(),
    ApplicationDataFingerprint(),
    ActiveDiagnosticSession(),
    VehicleManufacturerSparePartNumber(),
    VehicleManufacturerECUSoftwareNumber(),
    VehicleManufacturerECUSoftwareVersionNumber(),
    SystemSupplierIdentifier(),
    ECUMfgDate(),
    ECUSerialNumber(),
    SupportedFunctionalUnits(),
    VehicleIdentifierKitAssemblyPartNumber(),
    ISOSAE_ReservedStandardized(),
    VIN(),
    VehicleManufacturerECUHardwareNumber(),
    SystemSupplierECUHardwareNumber(),
    SystemSupplierECUHardwareVersionNumber(),
    SystemSupplierECUSoftwareNumber(),
    SystemSupplierECUSoftwareVersionNumber(),
    ExhaustRegulationOrTypeApprovalNumber(),
    SystemNameOrEngineType(),
    RepairShopCodeOrTesterSerialNumber(),
    ProgrammingDate(),
    CalibrationRepairShopCodeOrCalibrationEquipmentSerialNumber(),
    CalibrationDate(),
    CalibrationEquipmentSoftwareNumber(),
    ECUInstallationDate(),
    ODXFile(),
    Entity(),
    # IdentificationOptionVehicleManufacturerSpecific2(),
    # IdentificationOptionSystemSupplierSpecific(),
    # Periodic(),
    # DynamicallyDefined(),
    # OBDData1(),
    # OBDData2(),
    # OBDMonitorData1(),
    # OBDMonitorData2(),
    # OBDInfoType(),
    # Tachograph(),
    # AirbagDeployment(),
    NumberOfEDRDevices(),
    EDRIdentification(),
    EDRDeviceAddressInformation(),
    # EDREntries(),
    # SafetySystem(),
    # ReservedForFutureLegislativeRequirements(),
    # SystemSupplierSpecific(),
    UDSVersion(),
    # ISOSAE_Reserved1()
]

INTERFACE = "vcan0"
SENDER_CANID = "7E0"
RECIEVER_CANID = "7E8"
INTERVAL = 0.1
RETRY = 2
if __name__ == "__main__":
    
    for f in range(0x00, 0xFF):
        for s in range(0x00, 0x9):
            
            process = create_background_recv_process(send_canid = SENDER_CANID, recv_canid= RECIEVER_CANID)
            time.sleep(INTERVAL)
            
            packet = [0x22] + [f] + [s]

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
            else:
                raise Exception("not capture")
