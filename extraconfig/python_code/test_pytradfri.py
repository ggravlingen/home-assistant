#!/usr/bin/env python3

# Pre-requisites
# pip3 install pytradfri

import sys
import pytradfri
from homeassistant.util.color import *

# Assign configuration variables. The configuration check takes care they are present.
api = pytradfri.coap_cli.api_factory(sys.argv[1], sys.argv[2])
gateway = pytradfri.gateway.Gateway(api)
devices = gateway.get_devices()
lights = [dev for dev in devices if dev.has_light_control]

# Print all lights
print(lights)

# Lights can be accessed by its index, so lights[1] is the second light

# Example 1: checks state of the light 2 (true=on)
print(lights[2].light_control.lights[0].state)

# Example 2: get dimmer level of light 2
print(lights[2].light_control.lights[0].dimmer)

# Example 3: What is the name of light 2
print(lights[2].name)

# Example 4: Set the light level of light 2
lights[2].light_control.set_dimmer(20)

# Example 5: Change color of light 2
#lights[1].light_control.set_hex_color('f5faf6') # f5faf6 = cold | f1e0b5 = normal | efd275 = warm
#print(lights[2].light_control.lights[0].hex_color) # f5faf6 = cold | f1e0b5 = normal | efd275 = warm

moods = gateway.get_moods()
print(moods)


#rgb(245,250,246)
#rgb(241,224,181)
#rgb(239,210,117)

# Example 6: Color temp
#print("Color")
#print(lights[1].light_control.lights[0].raw)
#foo = color_xy_brightness_to_RGB(lights[1].light_control.lights[0].xy_color[0], lights[1].light_control.lights[0].xy_color[1], lights[1].light_control.lights[0].dimmer)
#print(foo)

#print(lights[1].light_control.lights[0].xy_color)

