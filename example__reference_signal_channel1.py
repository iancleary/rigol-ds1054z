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

    # Capture the data sets from channels 1--4 and=
    # write the data sets to their own file.
    # for c in range(1,2):
    #     channel_string = 'channel{c}.dat'
    #     print(f"Capturing data from channel {c} to file {channel_string}")
    #     osc[c].get_data('raw', channel_string)


if __name__ == "__main__":
    main()
