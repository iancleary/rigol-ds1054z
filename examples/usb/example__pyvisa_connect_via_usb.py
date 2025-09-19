import pyvisa

rm = pyvisa.ResourceManager()

# We are connecting the oscilloscope through USB here.

USB_ADDRESS_CONNECT_STRING = rm.list_resources()[0]
# Only one VISA-compatible instrument is connected to our computer,
# thus the first resource on the list is our oscilloscope.
# You can see all connected and available local devices calling
print(rm.list_resources())

print(f"Connecting to oscilloscope at address {USB_ADDRESS_CONNECT_STRING}")

print("\nexamples/usb.py\n")
print(
    f"Attempting connection to oscilloscope via USB address {USB_ADDRESS_CONNECT_STRING}"
)

inst = rm.open_resource(f"{USB_ADDRESS_CONNECT_STRING}")

# Query if instrument is present
# Prints e.g. "RIGOL TECHNOLOGIES,DL3021,DL3A204800938,00.01.05.00.01"
print(inst.query("*IDN?"))

print(f"Success connecting to oscilloscope at USB address {USB_ADDRESS_CONNECT_STRING}")
