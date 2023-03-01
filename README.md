# SPS30 - MicroPython

A simple library to communicate with a Sensirion SPS30 sensor using a serial communication. 
The SPS30 is an *MCERTS*-certified particulate matter sensor based on laser scattering measurement principles. 
It can classify particles within *PM1.0*, *PM2.5*, *PM4* and *PM10* categories.

## Sample usage

```python
sps30 = SPS30()
```

## Development notes

**Build the package:**
```bash 
poetry build
```
