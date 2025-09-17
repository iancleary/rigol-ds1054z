import time

from rigol_ds1054z import Rigol_DS1054Z
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def process_waveform(waveform, show=False, filename=None):
    """
    Convert the query of the waveform data into properly scaled Numpy arrays.

    Args:
        waveform: The namedtuple returned from ``Rigol_DS100Z().waveform()``.
        show (bool): Draw the waveform to a new matplotlib figure.
        filename (str): Save the display image to a file (CSV recommended).

    Returns:
        A tuple of two Numpy arrays, (xdata, ydata).
    """
    if waveform.format == "ASC":
        ydata = np.array(waveform.data[11:].split(","), dtype=float)
    if waveform.format in ("BYTE", "WORD"):
        ydata = (
            np.array(waveform.data) - waveform.yorigin - waveform.yreference
        ) * waveform.yincrement

    xdata = np.array(range(0, len(ydata)))
    xdata = xdata * waveform.xincrement + waveform.xorigin + waveform.xreference

    if show:
        xlim = (xdata[0], xdata[-1])
        ylim = tuple((np.array([-100, 100]) - waveform.yorigin) * waveform.yincrement)
        plt.plot(xdata, ydata)
        plt.xlim(*xlim)
        plt.xticks(np.linspace(*xlim, 13), rotation=30)
        plt.ylim(*ylim)
        plt.yticks(np.linspace(*ylim, 9))
        plt.ticklabel_format(style="sci", scilimits=(-3, 2))
        plt.grid()
        plt.show()

    if filename is not None:
        np.savetxt(filename, np.transpose(np.vstack((xdata, ydata))), delimiter=",")

    return xdata, ydata


def main():
    print("\n\n\n")

    print("Hello from rigol-ds1054z!")

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

    with Rigol_DS1054Z(visa_resource_string=IP_ADDRESS_CONNECT_STRING) as oscope:
        oscope = Rigol_DS1054Z(visa_resource_string=IP_ADDRESS_CONNECT_STRING)
        print(oscope)

        print("Stopping oscilloscope")
        oscope.stop()

        print("Waiting 1 second")
        time.sleep(1)

        print("Running oscilloscope")
        oscope.run()

        # time.sleep(5)

        # oscope.autoscale()

        # Change voltage range of channel 1 to 50mV/div.
        # oscope[1].set_vertical_scale_V(1000e-3)
        print("Waiting 2 seconds")
        time.sleep(2)

        print("Getting waveform from channel 1")
        channel1 = oscope.waveform(source=1, format="ASC")
        print(channel1)

        (t, v) = process_waveform(channel1)

        print(t)
        print(v)
        # # Stop the scope.
        print("Stopping oscilloscope")
        oscope.stop()

        # # Take a screenshot.
        # print("Taking screenshot")
        # oscope.get_screenshot("example__rewrite.png", "png")

        # # Create a pandas DataFrame from the data.
        print("Creating pandas DataFrame and writing to CSV")
        trace = pd.DataFrame(
            {"Time (s)": t, "Voltage (V)": v}  # , columns=["Time (s)", "Voltage (V)"]
        )
        print(trace)
        # # trace.plot(x="Time (s)", y="Voltage (V)")
        print("Writing data to example__rewrite.csv")
        trace.to_csv("example__rewrite.csv", index=False)
        pandas_plot = trace.plot(
            x="Time (s)",
            y="Voltage (V)",
            title="Reference Signal from Channel 1 (Pandas)",
        )
        pandas_plot.figure.savefig("example__rewrite_pandas_figure.png")

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
        plt.savefig("example__rewrite_matplotlib_figure.png")

        print("\n\n\n")


if __name__ == "__main__":
    main()
