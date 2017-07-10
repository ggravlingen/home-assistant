#!/bin/bash

cd /home/homeassistant/.homeassistant/www/custom_ui/floorplan

# Disabled because I have some custom css of my own
rm floorplan.css
wget https://raw.githubusercontent.com/pkozul/ha-floorplan/master/www/custom_ui/floorplan/floorplan.css

rm ha-floorplan.html
wget https://raw.githubusercontent.com/pkozul/ha-floorplan/master/www/custom_ui/floorplan/ha-floorplan.html

rm svg-pan-zoom.min.js
wget https://raw.githubusercontent.com/pkozul/ha-floorplan/master/www/custom_ui/floorplan/svg-pan-zoom.min.js

