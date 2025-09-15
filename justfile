help:
  just --list

run:
  uv run main.py

debug:
  uv run debug.py

install:
  uv install

visa:
  echo "In order to use this module, you must have the VISA platform installed for your operating system." 
  echo "For Windows, you can download and install the NI-VISA runtime from:"
  echo "    https://www.ni.com/en-us/support/downloads/drivers/download.ni-visa.html"
  echo "For both Linux and MacOS, you can use the same URL as Windows to download the NI-VISA runtime."

format:
  uv run ruff format .