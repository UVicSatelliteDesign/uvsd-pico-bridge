# NOTE: CURRENTLY WORKING ON SPI CONNECTION BETWEEN NRFBOARD BUT USB CONNECTION WORKS

# UVic Satellite Design Pico Bridge

This repository contains a Raspberry Pi Pico firmware project and a laptop-side
USB serial receiver for transferring a JPEG image from the Pico to a computer.
The current firmware sends the image embedded in `spi_connection/photo.h`;
the intended SPI input path is not active yet.

## Note about photo.h

Currently the pico only transfers a hardcoded photo.h build from 
```bash
xxd -i photo.jpg > photo.h
```
Later this will be replaced by the actually SPI chunk frames from the nRF board when initialized.

## Repository layout

- `spi_connection/` — Pico firmware, embedded image, and CMake build files.
- `usb-laptop/` — Python USB serial receiver built on PySerial.

## Firmware build and flash

Requirements:

- Raspberry Pi Pico SDK 2.3.0 or later.
- CMake and a toolchain supported by the Pico SDK.

From the repository root, configure and build (replace the SDK path with your
local checkout):

```sh
./build.sh
```

Copy `spi_connection/build/spi_connection.uf2` using `./flash.sh` to the Pico while it is in
BOOTSEL mode to flash the firmware. 

## Laptop receiver

The receiver uses Python 3.14 or later and PySerial. From `usb-laptop/`, install
the project dependencies with:

```sh
uv sync
```

Before running `src/usb-laptop/main.py`, set the serial port for the laptop
(currently `/dev/ttyACM0` in the script) and provide a destination filename in
the `USBConnection` constructor. The current `__main__` call does not yet pass
that required filename, so the receiver needs this small configuration change
before it can run.

## Current transfer behavior

After boot, the Pico waits briefly, writes a text header over USB serial, sends
the image bytes in 3,072-byte chunks, then writes the `\n__IMAGE_EOF__\n`
terminator. The laptop receiver reads the stream, removes the terminator, looks
for the JPEG start marker, and writes the resulting bytes to the configured
file. The transfer currently uses a baud rate of 115200.

The firmware's SPI pin and peripheral setup is present only as commented-out
code; the image is currently sent from the embedded `photo.h` data instead.