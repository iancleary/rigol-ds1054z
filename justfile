help:
  just --list

# run the example script to get a reference signal from a Rigol DS1054X oscilloscope and save it to CSV and PNG files
run:
  uv run example__reference_signal_channel1.py

# run the example script to connect to an instrument via IP using PyVISA
ip:
  uv run example__pyvisa_connect_via_ip.py

# run the example script to connect to an instrument via USB using PyVISA
usb:
  uv run example__reference_signal_channel1.py

# install the module's dependencies
install:
  uv install

# run pre-commit hooks
pre-commit:
  uv run pre-commit run --all-files

precommit: pre-commit

# run ruff linter
lint:
  uv run ruff check .

# run ruff linter with 
fix:
  uv run ruff check . --fix

# run ruff formatter
format:
  uv run ruff format .

# run tests with coverage
test:
  uv run pytest tests

visa:
  @echo ""
  @echo "--------------------------------------------------------------------------------"
  @echo "VISA Backend Installation Instructions (Start)"
  @echo "--------------------------------------------------------------------------------"
  @echo ""
  @echo "Virtual instrument software architecture (VISA) is a widely used application programming interface (API) in the test and measurement (T&M) industry for communicating with instruments from a computer."
  @echo ""
  @echo "    For more information, see the wikipedia page on VISA:"
  @echo "        https://en.wikipedia.org/wiki/Virtual_instrument_software_architecture"
  @echo ""
  @echo "This module depends on a VISA (Virtual Instrument Software Architecture) backend."
  @echo "The 'pyvisa' package is a Python wrapper for the VISA (Virtual Instrument Software Architecture) standard."
  @echo ""
  @echo "However, 'pyvisa' does not include a VISA backend itself, as it varies by application/scenario."
  @echo ""
  @echo "Therefore, you need to install a VISA backend separately to use this module."
  @echo ""
  @echo "In order to use this module, you have two options:"
  @echo ""
  @echo "1) [Open Source], you can install the open-source version of VISA called 'pyvisa-py' using pip:"
  @echo "    uv add pyvisa-py"
  @echo ""
  @echo "    uv add Rigol1000z[openvisa]"
  @echo ""
  @echo "    Note that pyvisa-py only supports TCPIP connections (without other dependecies)."
  @echo ""
  @echo "    For more information, visit the pyvisa-py documentation at:"
  @echo "        https://pyvisa-py.readthedocs.io/en/latest/"
  @echo ""
  @echo "    There are instructions for installing additional backends to support USB and GPIB connections."
  @echo "    However, these backends may require additional dependencies and setup that installing this package does not cover."
  @echo ""
  @echo "2) [Proprietery] National Intruments VISA platform for your Operating Systems (OS)"
  @echo "    This is the a paved road option if you don't mind using closed source software."
  @echo ""
  @echo "    For Windows, you can download and install the NI-VISA runtime from:"
  @echo "    https://www.ni.com/en-us/support/downloads/drivers/download.ni-visa.html"
  @echo ""
  @echo "    For both Linux and MacOS, you can use the same URL as Windows to download the NI-VISA runtime."
  @echo ""
  @echo "    In this case, you do not need to install any additional packages."
  @echo "    uv add Rigol1000z"
  @echo ""
  @echo "    The NI-VISA platform supports TCPIP, USB, and GPIB connections."
  @echo ""
  @echo "--------------------------------------------------------------------------------"
  @echo "For more information on installing and using VISA backends, see the PyVISA documentation at:"
  @echo "    https://pyvisa.readthedocs.io/en/latest/"
  @echo ""
  @echo "--------------------------------------------------------------------------------"
  @echo "VISA Backend Installation Instructions (End)"
  @echo "--------------------------------------------------------------------------------"
  @echo ""

