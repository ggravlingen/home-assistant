#!/usr/bin/env python3

# Pre-requisites
# pip3 install pytradfri

import sys
import pytradfri

# Assign configuration variables. The configuration check takes care they are present.
api = pytradfri.coap_cli.api_factory(sys.argv[1], sys.argv[2])
gateway = pytradfri.gateway.Gateway(api)
devices = gateway.get_devices()
lights = [dev for dev in devices if dev.has_light_control]

# Print all lights
print(lights)

# Lights can be accessed by its index, so lights[1] is the second light

# Example 1: checks state of the light 2 (true=on)
print(lights[1].light_control.lights[0].state)

# Example 2: get dimmer level of light 2
print(lights[1].light_control.lights[0].dimmer)

# Example 3: What is the name of light 2
print(lights[1].name)

# Example 4: Set the light level of light 2
lights[1].light_control.set_dimmer(20)

# Example 5: Change color of light 2
lights[1].light_control.set_hex_color('f5faf6') # f5faf6 = cold | f1e0b5 = normal | efd275 = warm

#rgb(245,250,246)
#rgb(241,224,181)
#rgb(239,210,117)

# Example 6: Color temp
print("Color")
print(lights[1].light_control.lights[0].raw)
print(lights[1].light_control.lights[0].xy_color[0])

