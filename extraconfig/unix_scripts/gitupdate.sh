#!/bin/bash

#cd /home/homeassistant/.homeassistant
#source /srv/homeassistant/homeassistant_venv/bin/activate
#hass --script check_config

#default="Minor update"
#echo -n "Enter the Description for the Change: " [Minor Update]
#read CHANGE_MSG

cd /home/homeassistant/.homeassistant
git add .
git status

read -e -p "Enter the Description for the Change:" -i "Minor" CHANGE_MSG

echo $CHANGE_MSG

#read -p "Enter the Description for the Change: " CHANGE_MSG
#name=${CHANGE_MSG:-Minor}

git commit -m "${CHANGE_MSG}"
git push origin master

exit
