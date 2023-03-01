from sps30.models import StatusRegister


def reverse_byte_stuffing(raw_data: bytes) -> bytes:
    """Apply reverse byte-stuffing on an input byte string.

    See the documentation for more information.

    Args:
        raw_data: Input bytes to be replaced.

    Returns:
        The input data with reversed byte-stuffed characters.

    """

    if b"\x7D\x5E" in raw_data:
        raw_data = raw_data.replace(b"\x7D\x5E", b"\x7E")
    if b"\x7D\x5D" in raw_data:
        raw_data = raw_data.replace(b"\x7D\x5D", b"\x7D")
    if b"\x7D\x31" in raw_data:
        raw_data = raw_data.replace(b"\x7D\x31", b"\x11")
    if b"\x7D\x33" in raw_data:
        raw_data = raw_data.replace(b"\x7D\x33", b"\x13")

    return raw_data


def trim_data(raw_data: bytes) -> bytes:
    """Removes head and tail from byte string.

    Args:
        raw_data: Input bytes to be trimmed.

    Returns:
        Trimmed data characters.

    """

    return raw_data[5:-2]


def transform_data(raw_data: bytes) -> bytes:
    """Transform raw input byte string.

    Apply inverse byte stuffing and remove head and tail characters.

    Args:
        raw_data: Input bytes to be transformed.

    Returns:
        Transformed data characters.

    """

    raw_data = reverse_byte_stuffing(raw_data)
    raw_data = trim_data(raw_data)

    return raw_data


def is_set(n: int, b: int) -> int:
    """Checks if a bit is set.

    Args:
        n: Input number.
        b: Bit that should be checked.
    Returns:
        True if the `b`-th bit is set in `n`. False otherwise.
    """

    return n & 1 << b


def parse_status_register(register) -> StatusRegister:
    """Parse the status register into a dict.

    See the class definition of StatusRegister for more information.

    Args:
        register (int): Status register as 32 bit unsigned integer.

    Returns:
        StatusRegister object.

    """

    register_data = StatusRegister()

    # if the register is 0 everything is ok
    if register == 0:
        return register_data

    if is_set(register, 4):
        register_data.fan_ok = False

    if is_set(register, 5):
        register_data.laser_current_ok = False

    if is_set(register, 21):
        register_data.fan_speed_ok = False

    return register_data
