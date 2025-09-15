import pyvisa

rm = pyvisa.ResourceManager()

IP_ADDRESS = "169.254.209.1"
IP_ADDRESS_CONNECT_STRING = f"TCPIP0::{IP_ADDRESS}::INSTR"


print("\nexamples/ip.py\n")
print(
    f"Attempting connection to oscilloscope via IP address {IP_ADDRESS_CONNECT_STRING}"
)

inst = rm.open_resource(f"{IP_ADDRESS_CONNECT_STRING}")

# Query if instrument is present
# Prints e.g. "RIGOL TECHNOLOGIES,DL3021,DL3A204800938,00.01.05.00.01"
print(inst.query("*IDN?"))

print(f"Success connecting to oscilloscope at IP address {IP_ADDRESS_CONNECT_STRING}")
