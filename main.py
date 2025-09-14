import pyvisa
import Rigol1000z
import pandas as pd
import matplotlib.pyplot as plt

import time


def main():
    print("Hello from rigol!")

    rm = pyvisa.ResourceManager()

    # We are connecting the oscilloscope through USB here.
    # Only one VISA-compatible instrument is connected to our computer,
    # thus the first resource on the list is our oscilloscope.
    # You can see all connected and available local devices calling
    #
    print(rm.list_resources())
    #
    osc_resource = rm.open_resource(rm.list_resources()[0])

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

    print("Stopping oscilloscope")
    osc.stop()

    trace = pd.DataFrame({"time": t, "voltage": v})
    print(trace)
    trace.plot(x="time", y="voltage")
    plt.savefig("channel1.png")

    # Capture the data sets from channels 1--4 and=
    # write the data sets to their own file.
    # for c in range(1,2):
    #     channel_string = 'channel{c}.dat'
    #     print(f"Capturing data from channel {c} to file {channel_string}")
    #     osc[c].get_data('raw', channel_string)


if __name__ == "__main__":
    main()
