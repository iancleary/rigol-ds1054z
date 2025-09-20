import sys

from rigol_ds1054z.src.waveform import WAVEFORM


def process_waveform(waveform: WAVEFORM):
    """
    Convert the query of the waveform data into properly scaled Numpy arrays.

    Require numpy to be installed only if you call the `process_waveform` function
        You do not need it if you just import this function

    Args:
        waveform: The namedtuple returned from ``Rigol_DS100Z().waveform()``.

    Returns:
        A tuple of two Numpy arrays, (xdata, ydata).
    """

    # Require numpy to be installed only if you call the `process_waveform` function
    NUMPY = "numpy"

    if NUMPY in sys.modules:
        print(
            f"{NUMPY!r} already in sys.modules"
        )  # however, it is not imported in this files
        import numpy as np

        pass  # no debug print needed, they know its there by the lack of this message
    else:
        print(f"can't find the {NUMPY!r} module, raising ImportError")
        raise ImportError("numpy is required to use this module.")

    if waveform.format == "ASC":
        ydata = np.array(waveform.data[11:].split(","), dtype=float)
    if waveform.format in ("BYTE", "WORD"):
        ydata = (
            np.array(waveform.data) - waveform.yorigin - waveform.yreference
        ) * waveform.yincrement

    xdata = np.array(range(0, len(ydata)))
    xdata = xdata * waveform.xincrement + waveform.xorigin + waveform.xreference

    return xdata, ydata
