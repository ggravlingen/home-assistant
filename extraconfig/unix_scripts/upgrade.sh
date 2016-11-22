#!/bin/bash

sudo su -s /bin/bash hass
source /srv/hass/hass_venv/bin/activate
pip3 install --upgrade homeassistant
pip3 install homeassistant==0.31.1
