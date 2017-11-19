#!/bin/bash

cd /home/homeassistant/.homeassistant/www/custom_ui/floorplan

# Disabled because I have some custom css of my own
rm floorplan.css
wget https://raw.githubusercontent.com/pkozul/ha-floorplan/master/www/custom_ui/floorplan/floorplan.css

rm ha-floorplan.html
wget https://raw.githubusercontent.com/pkozul/ha-floorplan/master/www/custom_ui/floorplan/ha-floorplan.html

cd /home/homeassistant/.homeassistant/www/custom_ui/floorplan/lib

rm *
wget https://raw.githubusercontent.com/pkozul/ha-floorplan/master/www/custom_ui/floorplan/lib/svg-pan-zoom.min.js
wget https://raw.githubusercontent.com/pkozul/ha-floorplan/master/www/custom_ui/floorplan/lib/moment.min.js
wget https://raw.githubusercontent.com/pkozul/ha-floorplan/master/www/custom_ui/floorplan/lib/jquery-3.2.1.min.js

