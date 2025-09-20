from functools import partial
import importlib.util
import os
import pathlib
import sys
from time import sleep
from typing import Optional


from pyvisa import ResourceManager

from rigol_ds1054z.src.channel import channel
from rigol_ds1054z.src.display import display
from rigol_ds1054z.src.ieee import ieee
from rigol_ds1054z.src.timebase import timebase
from rigol_ds1054z.src.trigger import trigger
from rigol_ds1054z.src.waveform import waveform

# Require pyvisa to be installed without try catch
PYVISA = "pyvisa"
PYVISA_INSTALLED = False

if PYVISA in sys.modules:
    # print(f"{PYVISA!r} already in sys.modules")
    pass  # no debug print needed, they know its there by the lack of this message
elif (spec := importlib.util.find_spec(PYVISA)) is not None:
    # If you choose to perform the actual import ...
    pass  # not needed here, since pyvisa resource is passed to the class
else:
    print(f"can't find the {PYVISA!r} module, raising ImportError")
    raise ImportError("pyvisa is required to use this module.")


class Oscilloscope:
    """
    A class for communicating with a Rigol DS1000Z series oscilloscope.
    Tested with a Rigol DS1054Z oscilloscope

    This class is compatible with context managers. The functional interfaces
    ``ieee``, ``channel``, ``timebase``, ``display``, ``waveform``, and ``trigger``
    are bound to this object as partial functions.

    Args:
        visa_resource_string (str): The VISA resource address string.
    """

    def __init__(self, visa_resource_string: str = None):
        self.visa_resource_string = visa_resource_string

        self.ieee = partial(ieee, self)
        self.channel = partial(channel, self)
        self.timebase = partial(timebase, self)
        self.display = partial(display, self)
        self.waveform = partial(waveform, self)
        self.trigger = partial(trigger, self)

        self.open()

    def __enter__(self):
        return self.open()

    def __exit__(self, exc_type, exc_value, exc_traceback):
        return self.close()

    def open(self):
        """Open the VISA resource to establish the communication channel."""
        self.visa_rsrc = ResourceManager().open_resource(self.visa_resource_string)
        return self

    def close(self):
        """Close the VISA resource to terminate the communication channel."""
        self.visa_rsrc.close()

    def write(self, cmd: str):
        """
        Write a command over the VISA communication interface.
        The command is automatically appended with a ``*WAI`` command.

        Args:
            cmd (str): The command string to be written.
        """
        self.visa_rsrc.write(cmd + ";*WAI")

    def read(self):
        """
        Read back over the VISA communication interface.

        Returns:
            The received string.
        """
        return self.visa_rsrc.read().strip()

    def query(self, cmd: str, delay: Optional[float] = None):
        """
        Execute a query over the VISA communication interface.
        The command is automatically appended with a ``*WAI`` command.

        Args:
            cmd (str): The command string to be written.
            delay (float): Time delay between write and read (optional).

        Returns:
            The received string.
        """
        return self.visa_rsrc.query(cmd + ";*WAI", delay).strip()

    def autoscale(self, sleep_duration: float = 10):
        """``:AUToscale`` Autoscale the oscilloscope, followed by a 10s delay."""
        self.write(":AUT")
        sleep(sleep_duration)

    def clear(self, sleep_duration: float = 1):
        """``:CLEar`` Clear the oscilloscope display, followed by a 1s delay."""
        self.write(":CLE")
        sleep(sleep_duration)

    def run(self, sleep_duration: float = 1):
        """``:RUN`` Run the oscilloscope, followed by a 1s delay."""
        self.write(":RUN")
        sleep(sleep_duration)

    def stop(self, sleep_duration: float = 1):
        """``:STOP`` Stop the oscilloscope, followed by a 1s delay."""
        self.write(":STOP")
        sleep(sleep_duration)

    def single(self, sleep_duration: float = 1):
        """``:SINGle`` Single trigger the oscilloscope, followed by a 1s delay."""
        self.write(":SING")
        sleep(sleep_duration)

    def tforce(self, sleep_duration: float = 1):
        """``:TFORce`` Force trigger the oscilloscope, followed by a 1s delay."""
        self.write(":TFOR")
        sleep(sleep_duration)

    def get_screenshot(self, filename=None, format="png"):
        """
        Downloads a screenshot from the oscilloscope.

        Args:
            filename (str): The path of the image file.  The appropriate
                extension should be included (i.e. jpg, png, bmp or tif).
                If you do not, filename = f"{filename}.{format}" is called for you.
            format (str): The format image that should be downloaded.  Options
                are 'jpeg, 'png', 'bmp8', 'bmp24' and 'tiff'.  It appears that
                'jpeg' takes <3sec to download while all the other formats take
                <0.5sec.  Default is 'png'.
        """

        # an advantage here is this does not require an external library beyond pyvisa

        assert format in ("jpeg", "png", "bmp8", "bmp24", "tiff")

        # Due to the up to 3s delay, we are setting timeout to None for this operation only
        old_timeout = self.visa_rsrc.timeout
        self.visa_rsrc.timeout = None

        # create the image
        self.write(":disp:data? on,off,%s" % format)

        # read the image data back
        # these are magic numbers
        raw_img = self.visa_rsrc.read_raw(3850780)[11:-4]

        # set the timeout back after the operation is done
        self.visa_rsrc.timeout = old_timeout

        if filename is not None:
            if not filename.lower().endswith(f".{format}"):
                filename = f"{filename}.{format}"

            if pathlib.Path(filename).exists():
                os.remove(filename)

            with open(filename, "wb") as fs:
                fs.write(raw_img)

        return raw_img
