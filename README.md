# SPS30 - MicroPython

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat-square&labelColor=ef8336)](https://pycqa.github.io/isort/)

A simple library to communicate with a Sensirion SPS30 sensor using a serial communication.
The SPS30 is an *MCERTS*-certified particulate matter sensor based on laser scattering measurement principles.
It can classify particles within *PM1.0*, *PM2.5*, *PM4* and *PM10* categories.

## Sample usage

```python
from machine import Pin
from time import sleep

from sps30 import SPS30


def main() -> None:
    sps30 = SPS30(id=1, tx=Pin(4), rx=Pin(5))

    sps30.start_measurement()
    sleep(5)

    for i in range(10):
        measurement = sps30.read_measurement()
        print(measurement)

        sleep(1)

    sps30.stop_measurement()


if __name__ == "__main__":
    main()
```

In this example, the *UART1* interface of the Pico is used with port `GP4` for the *TX* and port `GP5` for the *RX* line. 

## Useful information

**Pinout diagram of the Raspberry Pi Pico W**

The image is taken from the official [documentation](https://www.raspberrypi.com/documentation/microcontrollers/raspberry-pi-pico.html). 

<p align="center">
<img src="/assets/pico_pinout.png" alt="Raspberry Pi Pico W Pinout" title="Raspberry Pi Pico W Pinout" style="width: 800px">
</p>

## Contribution notes

**Install dependencies**

To install the required dependencies including the *dev* packages run:
```bash
poetry install
```

**Build the package:**

To build the *.whl* package run:
```bash
poetry build
```
