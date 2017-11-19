#!/usr/bin/env python

import sys
import evdev

devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]

print(devices)

if len(devices) == 0:
    print("No devices found, try running with sudo")
    sys.exit(1)

for device in devices:
    print(device.name)
    if device.name == 'Bluetooth Remote Shutter':
        print(device)
        device.grab()
        for event in device.read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                print(evdev.categorize(event))
