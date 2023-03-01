import struct
from time import sleep_ms

from machine import UART, Pin

from sps30.models import Measurement, StatusRegister
from sps30.utils import parse_status_register, transform_data

data_frame = {
    "start_measurement": b"\x7E\x00\x00\x02\x01\x03\xF9\x7E",
    "stop_measurement": b"\x7E\x00\x01\x00\xFE\x7E",
    "read_measurement": b"\x7E\x00\x03\x00\xFC\x7E",
    "read_product_type": b"\x7E\x00\xD0\x01\x00\x2E\x7E",
    "read_serial_number": b"\x7E\x00\xD0\x01\x03\x2B\x7E",
    "read_firmware_version": b"\x7E\x00\xD1\x00\x2E\x7E",
    "read_status_register": b"\x7E\x00\xD2\x01\x00\x2C\x7E",
}

# Maximum response times [ms]
# Taken from the official documentation (see SHDLC commands overview)
response_time = {
    "start_measurement": 20,
    "stop_measurement": 20,
    "read_measurement": 20,
    "read_product_type": 20,
    "read_serial_number": 20,
    "read_firmware_version": 20,
    "read_status_register": 20,
}


class SPS30:
    def __init__(self) -> None:
        self.conn = UART(1, baudrate=115200, parity=None, stop=1, tx=Pin(4), rx=Pin(5))

    def start_measurement(self):
        data = data_frame["start_measurement"]

        self._tx(data)
        sleep_ms(response_time["start_measurement"])
        self._rx(byte_cnt=7)

    def stop_measurement(self):
        data = data_frame["stop_measurement"]

        self._tx(data)
        sleep_ms(response_time["stop_measurement"])
        self._rx(byte_cnt=7)

    def read_measurement(self) -> Measurement:
        data = data_frame["read_measurement"]

        self._tx(data)
        sleep_ms(response_time["read_measurement"])

        data = self._rx(byte_cnt=47)

        measurement_data = Measurement(data)
        return measurement_data

    def read_product_type(self) -> str:
        """Reads the product type of the sensor.

        The type of the sensor is always equal to "00080000".
        If the value is different maybe the wrong port has been selected.

        Returns:
            Product type as string.

        """

        data = data_frame["read_product_type"]

        self._tx(data)
        sleep_ms(response_time["read_product_type"])

        data = self._rx(byte_cnt=16)
        data = data.decode("ascii")

        return data

    def read_serial_number(self) -> str:
        """Reads the serial number of the sensor.

        Returns:
            Serial number as string with maximal length of 32 ASCII characters.

        """

        data = data_frame["read_serial_number"]

        self._tx(data)
        sleep_ms(response_time["read_serial_number"])

        data = self._rx(byte_cnt=24)
        data = data.decode("ascii")

        return data

    def read_firmware_version(self) -> tuple[int, int]:
        """Reads firmware version of the sensor.

        Returns:
            Firmware version as tuple (major, minor).

        """

        data = data_frame["read_firmware_version"]

        self._tx(data)
        sleep_ms(response_time["read_firmware_version"])

        data = self._rx(byte_cnt=14)
        data = struct.unpack(">bbbbbbb", data)

        firmware_major: int = data[0]
        firmware_minor: int = data[1]

        return firmware_major, firmware_minor

    def read_status_register(self) -> StatusRegister:
        """Read the status register of the device.

        For further information about the status register, see the documentation.

        Returns:
            Current status register as 32bit unsigned integer.

        """

        data = data_frame["read_status_register"]

        self._tx(data)
        sleep_ms(response_time["read_status_register"])

        data = self._rx(byte_cnt=12)
        data = struct.unpack(">Ib", data)

        # Extract the register (Byte 4 is unused)
        register: int = data[0]

        register_data = parse_status_register(register)
        return register_data

    def _tx(self, data: bytes) -> int:
        """Transmit data to the UART device.

        Args:
            data: Data to send to the device.

        Returns:
             Number of bytes sent.

        """

        response = self.conn.write(data)
        if response is None:
            # Transmit timeout; TODO: Handle error
            ...

        return response

    def _rx(self, byte_cnt: int) -> bytes:
        """Receive data from the UART device.

        Args:
            byte_cnt: Number of bytes that should be read from the device.

        """

        while self.conn.any() < byte_cnt:
            # TODO: Include timeout to avoid endless loop
            sleep_ms(10)

        data = self.conn.read()
        data = transform_data(data)

        return data
