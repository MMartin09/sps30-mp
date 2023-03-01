import struct
import time


class Measurement:
    """Helper class representing a single measurement of the device.

    See the documentation for more information.

    Args:
        data: Transformed byte array received from the device.
        precision: Defines the precision (decimal places) of the measurement. Defaults to 1.

    Attributes:
        ts: GMT Timestamp now
        pm10: Mass Concentration PM1.0
        pm25: Mass Concentration PM2.5
        pm40: Mass Concentration PM4.0
        pm100: Mass Concentration PM10
        n05: Number Concentration 0.5
        n10: Number Concentration 1.0
        n25: Number Concentration 2.5
        n40: Number Concentration 4.0
        n100: Number Concentration 10
        tps: Typical Particle Size

    """

    def __init__(self, data: bytes, precision: int = 1) -> None:
        data = struct.unpack(">ffffffffff", data)

        self.ts = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(*time.gmtime())
        self.pm10 = round(data[0], precision)
        self.pm25 = round(data[1], precision)
        self.pm40 = round(data[2], precision)
        self.pm100 = round(data[3], precision)
        self.n05 = round(data[4], precision)
        self.n10 = round(data[5], precision)
        self.n25 = round(data[6], precision)
        self.n40 = round(data[7], precision)
        self.n100 = round(data[8], precision)
        self.tps = round(data[9], precision)

    def __str__(self):
        return f"Measurement(ts={self.ts}, pm10={self.pm10}, pm25={self.pm25}, pm40={self.pm40}, pm100={self.pm100}, n05={self.n05}, n10={self.n10}, n25={self.n25}, n40={self.n40}, n100={self.n100}, tps={self.tps}"


class StatusRegister:
    """Helper class representing the available attributes of the device status register.

    See the documentation for more information.

    Attributes:
        fan_speed_ok: True if the speed of the fan is ok. False otherwise.
        laser_current_ok: True if the current is ok. False otherwise.
        fan_ok: True if the fan is working as expected. False otherwise.

    """

    def __init__(self) -> None:
        self.fan_speed_ok: bool = True
        self.laser_current_ok: bool = True
        self.fan_ok: bool = True

    def __str__(self):
        return f"StatusRegister(fan_speed_ok={self.fan_speed_ok}; laser_current_ok={self.laser_current_ok}; fan_ok={self.fan_ok})"
