#!/bin/sh

sudo su -s /bin/bash hass

source /srv/hass/hass_venv/bin/activate
hass --script check_config
