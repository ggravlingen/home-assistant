#!/bin/bash

#cd /home/homeassistant/.homeassistant
#source /srv/homeassistant/homeassistant_venv/bin/activate
#hass --script check_config

cd /home/homeassistant/.homeassistant
git add .
git status

read -e -p "Enter the Description for the change: " -i "Minor update" CHANGE_MSG
git commit -m "${CHANGE_MSG}"
git push origin master

exit
