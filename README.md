# rigol-ds1054z

Python VISA (USB and Ethernet) library to control Rigol DS1000z series oscilloscopes. Continuation of https://github.com/jeanyvesb9/Rigol1000z (as of 2025-09-15, that repo is no longer maintained).

# IP Address Setup for Ethernet Connection

The Rigol DS1054z oscilloscope can be connected via Ethernet using a static IP address. To set up the IP address on the oscilloscope, follow these steps:

1. Power on the oscilloscope.
2. Press the "Utility" button on the front panel.
3. Navigate to the "IO Setting" tab using the arrow keys.
4. Select "LAN Conf" and press the "Enter" button.
5. Set the "IP Mode" to "Static".
6. Enter the desired static IP address, subnet mask, and gateway.
7. Press the "Save" button to apply the settings.
8. Restart the oscilloscope to ensure the new settings take effect.
9. Verify the connection by pinging the oscilloscope's IP address from your computer.
10. Use the IP address in your Python VISA library to connect to the oscilloscope.

Ensure the RemoteIO setting is enabled on the oscilloscope to allow remote connections.

1. Press the "Utility" button on the front panel.
2. Navigate to the "IO Setting" tab using the arrow keys.
3. Select "RemoteIO" and press the "Enter" button.
4. Set "LAN" to "ON".
5. Restart the oscilloscope to ensure the new settings take effect.

## Example IP Address:

```python
import pyvisa
import time

rm = pyvisa.ResourceManager()

IP_ADDRESS = "169.254.209.1"
IP_ADDRESS_CONNECT_STRING = f"TCPIP0::{IP_ADDRESS}::INSTR"

inst = rm.open_resource(f"{IP_ADDRESS_CONNECT_STRING}")
# Query if instrument is present
# Prints e.g. "RIGOL TECHNOLOGIES,DS1104Z,DS1ZA266M00140,00.04.05.SP2"
print(inst.query("*IDN?"))
```

## Example USB Address:

```python
# We are connecting the oscilloscope through USB here.
# Only one VISA-compatible instrument is connected to our computer,
# thus the first resource on the list is our oscilloscope.
# You can see all connected and available local devices calling
#
print(rm.list_resources())
# #

USB_ADDRESS_CONNECT_STRING = rm.list_resources()[0]
# USB_ADDRESS_CONNECT_STRING = "USB0::0x1AB1::0x4CE::DS1Z00000001::INSTR"
print(f"Connecting to oscilloscope at address {USB_ADDRESS_CONNECT_STRING}")

inst = rm.open_resource(f"{USB_ADDRESS_CONNECT_STRING}")
# Query if instrument is present
# Prints e.g. "RIGOL TECHNOLOGIES,DS1104Z,DS1ZA266M00140,00.04.05.SP2"
print(inst.query("*IDN?"))
```
