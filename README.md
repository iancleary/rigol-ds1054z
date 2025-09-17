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

```

## Example USB Address:

```python
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

```

## Example Reference Signal from Channel 1

```python
import pyvisa

import pandas as pd
import matplotlib.pyplot as plt

import time

from Rigol1000z import Oscilloscope as RigolDS1054Z


def main():
    print("\n\n\n")

    print("Hello from rigol!")

    rm = pyvisa.ResourceManager()

    # We are connecting the oscilloscope through USB here.
    # Only one VISA-compatible instrument is connected to our computer,
    # thus the first resource on the list is our oscilloscope.
    # You can see all connected and available local devices calling
    #
    # print(rm.list_resources())
    # #

    # USB_ADDRESS_CONNECT_STRING = rm.list_resources()[0]
    # USB_ADDRESS_CONNECT_STRING = "USB0::0x1AB1::0x4CE::DS1Z00000001::INSTR"
    # print(f"Connecting to oscilloscope at address {USB_ADDRESS_CONNECT_STRING}")

    # IP_ADDRESS = "172.18.8.39"
    IP_ADDRESS = "169.254.209.1"
    IP_ADDRESS_CONNECT_STRING = f"TCPIP0::{IP_ADDRESS}::INSTR"

    print(f"Connecting to oscilloscope at address {IP_ADDRESS_CONNECT_STRING}")

    osc_resource = rm.open_resource(IP_ADDRESS_CONNECT_STRING)

    osc = RigolDS1054Z(osc_resource)
    print(osc)

    print("Stopping oscilloscope")
    osc.stop()

    print("Waiting 1 second")
    time.sleep(1)

    print("Running oscilloscope")
    osc.run()

    # time.sleep(5)

    # osc.autoscale()

    # Change voltage range of channel 1 to 50mV/div.
    # osc[1].set_vertical_scale_V(1000e-3)
    print("Waiting 2 seconds")
    time.sleep(2)

    channel1 = osc[1]
    print(channel1)

    # osc.visa_write(":WAV:DATA? CHAN1")
    # raw_data = osc.visa_read_raw(250000)
    # data = channel1.parse_waveform_data(raw_data)
    # print(raw_data)

    print("\n\n\n")
    info = channel1.get_data_premable()
    print(info)

    (t, v) = channel1.get_data(mode="norm")
    print("Data from channel 1 written to channel1.dat")
    print(t)
    print(v)
    # Stop the scope.
    print("Stopping oscilloscope")
    osc.stop()

    # Take a screenshot.
    print("Taking screenshot")
    osc.get_screenshot("example__reference_signal_channel1.png", "png")

    # Create a pandas DataFrame from the data.
    print("Creating pandas DataFrame and writing to CSV")
    trace = pd.DataFrame(
        {"Time (s)": t, "Voltage (V)": v}  # , columns=["Time (s)", "Voltage (V)"]
    )
    # print(trace)
    # trace.plot(x="Time (s)", y="Voltage (V)")
    print("Writing data to example__reference_signal_channel1.csv")
    trace.to_csv("example__reference_signal_channel1.csv", index=False)
    pandas_plot = trace.plot(
        x="Time (s)", y="Voltage (V)", title="Reference Signal from Channel 1 (Pandas)"
    )
    pandas_plot.figure.savefig("example__reference_signal_channel1_pandas_figure.png")

    # create a plot of the data using matplotlib
    plt.figure()

    # set the background color to black
    # https://stackoverflow.com/a/23645437
    ax = plt.gca()
    ax.set_facecolor("black")

    plt.plot(t, v, "y")  # yellow line to match Rigol's color scheme for channel 1
    plt.title("Reference Signal from Channel 1 (Matplotlib)")
    plt.xlabel("Time (s)")
    plt.ylabel("Voltage (V)")
    plt.legend(["Channel 1"])
    plt.grid()
    plt.savefig("example__reference_signal_channel1_matplotlib_figure.png")

    print("\n\n\n")


if __name__ == "__main__":
    main()

```
