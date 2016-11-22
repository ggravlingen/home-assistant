#!/bin/sh

if find /home/hass/.homeassistant/extraconfig/webcam/. -maxdepth 1 -mmin +5 -type f | grep no1 &> /dev/null && echo success || echo fail
then
	sudo cp /home/hass/.homeassistant/extraconfig/webcam/offline.jpg /home/hass/.homeassistant/extraconfig/webcam/no1.jpg 
fi
