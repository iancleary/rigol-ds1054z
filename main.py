import pyvisa
import Rigol1000z
import pandas as pd
import matplotlib.pyplot as plt

import time


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
    IP_ADDRESS = "169.254.209.0"
    IP_ADDRESS_CONNECT_STRING = f"TCPIP0::{IP_ADDRESS}::INSTR"

    print(f"Connecting to oscilloscope at address {IP_ADDRESS_CONNECT_STRING}")

    osc_resource = rm.open_resource(IP_ADDRESS_CONNECT_STRING)

    osc = Rigol1000z.Rigol1000z(osc_resource)
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

    (t, v) = channel1.get_data(mode="norm", filename="channel1.dat")
    print("Data from channel 1 written to channel1.dat")
    print(t)
    print(v)
    # Stop the scope.
    print("Stopping oscilloscope")
    osc.stop()

    # Take a screenshot.
    print("Taking screenshot")
    osc.get_screenshot("screenshot.png", "png")

    trace = pd.DataFrame({"time": t, "voltage": v})
    print(trace)
    trace.plot(x="time", y="voltage")
    plt.savefig("channel1.png")

    print("\n\n\n")

    # Capture the data sets from channels 1--4 and=
    # write the data sets to their own file.
    # for c in range(1,2):
    #     channel_string = 'channel{c}.dat'
    #     print(f"Capturing data from channel {c} to file {channel_string}")
    #     osc[c].get_data('raw', channel_string)


if __name__ == "__main__":
    main()
