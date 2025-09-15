import pyvisa
import time

rm = pyvisa.ResourceManager()

# print(rm.list_resources())

# IP_ADDRESS = "172.18.8.39"
IP_ADDRESS = "169.254.209.0"
IP_ADDRESS_CONNECT_STRING = f"TCPIP0::{IP_ADDRESS}::INSTR"

inst = rm.open_resource(f"{IP_ADDRESS_CONNECT_STRING}")
# Query if instrument is present
# Prints e.g. "RIGOL TECHNOLOGIES,DL3021,DL3A204800938,00.01.05.00.01"
print(inst.query("*IDN?"))
