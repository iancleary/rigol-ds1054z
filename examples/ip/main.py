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

    with Oscilloscope(visa_resource_string=IP_ADDRESS_CONNECT_STRING) as oscope:
        print(oscope)

        print("Running oscilloscope")
        oscope.run()

        print("Autoscale oscilloscope")
        # this includes a time.sleep(10)'
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
