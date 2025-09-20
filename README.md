# rigol-ds1054z

Python VISA (USB and Ethernet) library to control Rigol DS1000z series oscilloscopes.

> First, you must pick a backend installation.

## VISA Backend Installation Instructions

Virtual instrument software architecture (VISA) is a widely used application programming interface (API) in the test and measurement (T&M) industry for communicating with instruments from a computer.

For more information, see the wikipedia page on VISA:
https://en.wikipedia.org/wiki/Virtual_instrument_software_architecture

This module depends on a VISA (Virtual Instrument Software Architecture) backend.

The `pyvisa` package is a Python wrapper for the VISA (Virtual Instrument Software Architecture) standard.

However, 'pyvisa' does not include a VISA backend itself, as it varies by application/scenario.

Therefore, you need to install a VISA backend separately to use this module.

In order to use this module, you have several options:

### Open Source Backends

#### TCP/IP

```bash
uv add 'rigol-ds1054z[tcpip]'
```

Note that `pyvisa-py` only supports TCPIP connections (without other dependecies).

> For more information, visit the [pyvisa-py documentation](https://pyvisa-py.readthedocs.io/en/latest/)
>
> There are instructions for installing additional backends to support USB and GPIB connections.

#### USB

Note that `pyusb` package only supports USB connections (without other dependecies).

```bash
uv add 'rigol-ds1054z[usb]'
```

#### Multiple Groups

> If you installed the National Instruments (NI) or Keysight proprietary options, they cover all the backends for you.

At home you might switch between USB and Ethernet or just be learning or want an easy solution (and don't mind extra packages in your environment).

```bash
uv add 'rigol-ds1054z[tcpip,usb]'
```

### Proprietery Backends

National Intruments VISA platform for your Operating Systems (OS)

> This is the a paved road option if you don't mind using closed source software.

For Windows, you can download and install the NI-VISA runtime from:

- https://www.ni.com/en-us/support/downloads/drivers/download.ni-visa.html

For both Linux and MacOS, you can use the same URL as Windows to download the NI-VISA runtime.

In this case, you do not need to install any additional packages.

```bash
uv add 'rigol-ds1054z'
```

The NI-VISA platform supports TCPIP, USB, and GPIB connections.

### pyvisa documentation directly

For more information on installing and using VISA backends, see the [PyVISA documentation directly](https://pyvisa.readthedocs.io/en/latest/).

## Authors and License

> learning from others, license attributions

I first discovered [jeanyvesb9/Rigol1000z](https://github.com/jeanyvesb9/Rigol1000z/tree/9834594d181b6a403af726d37e16468800e4442e) (as of 2025-09-15, that repo is no longer maintained). I edited this to work to capture scope data correctly, and added some additional functionality and examples.

I later found [amosborne/rigol-ds1000z](https://github.com/amosborne/rigol-ds1000z/blob/59a952ea1734c51d13fe04a57baaa18e94b51cad/LICENSE) and merged some of the changes from that repo in as well. I included the license attribution in the [AUTHORS.md](AUTHORS.md) file.

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

I wanted to learn more about the scope and how to control it via Python, so I wrote this library, continuing the MIT-licensed work of others.

> I hope you find it useful!

My main differences from [amosborne/rigol-ds1000z](https://github.com/amosborne/rigol-ds1000z/blob/59a952ea1734c51d13fe04a57baaa18e94b51cad/LICENSE) are:

- remove search functionality for VISA resources (you can use pyvisa directly for that, out of scope of this library...not needed in production lab environment)
- loosen main dependencies to just oscope connection optional dependencies in pyproject.toml
  - optional dependency for pyvisa-py backend to allow TCPIP connections without needing NI-VISA
  - optional dependency for pyusb and libusb1 to allow USB connections without needing NI-VISA
- using uv and ruff for linting and formatting
- adding my own examples (as I was learning how to use the library)

## IP Address Setup for Ethernet Connection

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

## Examples

### Test IP Address Connection

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

### Test USB Address Connection

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

> This uses an TCP/IP connection.
>
> There are comments in the script to help guide you to using a USB connection

If you don't have the probe hooked up to channel 1, modify the script to match your setup.

> In order to run this script you need

```bash
uv init ligor # rigol in reverse
cd ligor
uv add rigol-ds1054z
# with a backend installed per the above instructions
#
# in my case, for a TCP/ip connection
# without propietary NI-VISA installed
uv add 'rigol-ds1054z[tcpip]'

# for CSV, Trace Creation, and Plotting
uv add pandas numpy matplotlib
# pandas for making the csv file
# numpy for help making arrays
# matplotlib for making a chart, saving it to a png file
# the rigol-ds1054z library makes the screenshot png directly.
##  ^ the oscope does it, the library saves it a file.

# copy the below file into main.py
uv run main.py
```

Here is the [example\_\_reference_signal_channel1.py](./example__reference_signal_channel1.py) script

> Don't have both the USB and Ethernet cables plugged in at the same time, you might have issues.
> I had the USB interface work fine, but the TCP/IP connection timeout out.
> If I removed the USB connection, the ethernet TCP/IP connection worked as expected.

```python
# main.py

from rigol_ds1054z import Oscilloscope
from rigol_ds1054z.utils import process_waveform

import pandas as pd
import matplotlib.pyplot as plt


def main():
    print("\n\n\n")

    print("Hello from rigol-ds1054z!")

    # this module/library requires you to find this resource string
    #   this is intentional as a design choice, as the library helps you interface with your scope
    #   not figure out how you connected to it.
    #   In general, the USB connection will be slightly faster than TCPIP,
    #   but TCPIP has a much longer allowed cable length.
    #   See the README for instructions on how to connect via USB or set a static IP.
    #   My configuration when writing this is a network switch direct connection (not through my router)

    IP_ADDRESS = "169.254.209.1"  # change me to your address
    IP_ADDRESS_CONNECT_STRING = f"TCPIP0::{IP_ADDRESS}::INSTR"

    print(f"Connecting to oscilloscope at address {IP_ADDRESS_CONNECT_STRING}")

    # #   USB Example (untested), uncomment this entire block
    # #   uv add rigol_ds1054z[usb]
    # #   ...
    # #   then modify the below line to'
    # USB_ADDRESS_CONNECT_STRING = rm.list_resources()[0]
    # import pyvisa

    # rm = pyvisa.ResourceManager()

    # # We are connecting the oscilloscope through USB here.

    # USB_ADDRESS_CONNECT_STRING = rm.list_resources()[0]
    # # Only one VISA-compatible instrument is connected to our computer,
    # # thus the first resource on the list is our oscilloscope.
    # # You can see all connected and available local devices calling
    # print(rm.list_resources())

    # print(f"Connecting to oscilloscope at address {USB_ADDRESS_CONNECT_STRING}")

    # with Oscilloscope(visa_resource_string=USB_ADDRESS_CONNECT_STRING) as oscope:


    with Oscilloscope(visa_resource_string=IP_ADDRESS_CONNECT_STRING) as oscope:
        print(oscope)

        print("Stopping oscilloscope")
        oscope.run()

        # this includes a time.sleep(10)
        oscope.autoscale()

        print("Getting waveform from channel 1")
        channel1 = oscope.waveform(source=1, format="ASC")
        print(channel1)

        # this requires numpy, only when called (not when imported)
        # if this errors, notice when (during the function call, not the import)
        # this is to allow numpy to be an optional dependency
        (t, v) = process_waveform(channel1)

        print(t)
        print(v)
        # # Stop the scope.
        print("Stopping oscilloscope")
        oscope.stop()

        # # Take a screenshot.
        # print("Taking screenshot")
        # oscope.get_screenshot("example__reference_signal_channel1.png", "png")

        # # Create a pandas DataFrame from the data.
        print("Creating pandas DataFrame and writing to CSV")
        trace = pd.DataFrame(
            {"Time (s)": t, "Voltage (V)": v}  # , columns=["Time (s)", "Voltage (V)"]
        )
        print(trace)
        # # trace.plot(x="Time (s)", y="Voltage (V)")
        print("Writing data to example__reference_signal_channel1.csv")
        trace.to_csv("example__reference_signal_channel1.csv", index=False)
        pandas_plot = trace.plot(
            x="Time (s)",
            y="Voltage (V)",
            title="Reference Signal from Channel 1 (Pandas)",
        )
        pandas_plot.figure.savefig(
            "example__reference_signal_channel1_pandas_figure.png"
        )

        # # create a plot of the data using matplotlib
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

        oscope.get_screenshot(filename="example__reference_signal_channel1.png")

        print("\n\n\n")


if __name__ == "__main__":
    main()

```
