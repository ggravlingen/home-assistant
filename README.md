This is the configuration I'm using for my Home Assistant instance, which is running on a Raspberry Pi 3 (model b). The base is the HASSbian image.

Reinstall sequence (after first startup):
```
sudo raspi-config

#Network
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
network={
               ssid="home"
               psk="very secret passphrase"
          }

# Install home assistant
wget -Nnv https://raw.githubusercontent.com/home-assistant/fabric-home-assistant/master/hass_rpi_installer.sh && bash hass_rpi_installer.sh

# SSH setup
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa

# Give pi access righst to homeassistant folder

# Git setup and clone settings
git config --global user.email "you@example.com"
git config --global user.name "Your Name"
sudo systemctl stop home-assistant.service

# nb: .homeassistant-folder must be empty
cd /home/hass/.homeassistant
sudo mv deps ./.. #temporarily move deps out of the way
sudo rm .*
git clone git@github.com:ggravlingen/home-assistant.git .
sudo chown -R hass.hass *

# Backup bask profile and gitingore (gitignore not needed anymore?)
sudo rm -rf /home/hass/.homeassistant/extraconfig/unix_scripts/bash_profile
sudo ln /home/pi/.bash_profile /home/hass/.homeassistant/extraconfig/unix_scripts/bash_profile

sudo rm /home/hass/.homeassistant/extraconfig/unix_scripts/gitignore
sudo ln /home/hass/.homeassistant/.gitignore /home/hass/.homeassistant/extraconfig/unix_scripts/gitignore

# Enable google cal (check states for info)

# Running device detection through IFTTT on iOS. The JSON below is what I'm sending through Maker:
echo -e "curl -H "Content-Type: application/json" -X POST -d '{"topic": "/location/patrik_iphone", "payload": "Home" }' http://IP:8123/api/services/mqtt/publish?api_password=" > set_home.sh

# Install nodeJS, which is needed for Sonos control
curl -sL https://deb.nodesource.com/setup_4.x | sudo -E bash -
sudo apt-get install -y nodejs

# pm2 is used to ensure nodjs-scripts are always running
sudo npm install pm2 -g # install
sudo pm2 startup # enable autostart on reboot

# Install Sonos control
cd /opt
sudo git clone https://github.com/jishi/node-sonos-http-api
cd node-sonos-http-api/
sudo npm install --production
sudo pm2 start server.js
sudo pm2 save

# Setup cron
sudo crontab -e
* 3 * * * cd /home/hass/.homeassistant/extraconfig/python_code && sudo /usr/bin/python sonos_playlist.py > /tmp/listener.log 2>&1
* * * * * cd /home/hass/.homeassistant/extraconfig/webcam && sudo /usr/bin/avconv -i rtsp://192.168.0.59:554/onvif1 -ss 0:0:0 -frames 1 no1.jpg
2 * * * * cd /home/hass/.homeassistant/extraconfig/unix_scripts && sudo ./check_webcamfile.sh


# Misc
sudo apt-get install locate -y
sudo updatedb

# Video monitor
sudo apt-get install libav-tools -y


# Docker
curl -sSL get.docker.com | sh
sudo usermod -aG docker pi
sudo systemctl enable docker

git clone https://github.com/home-assistant/hadashboard.git
cd hadashboard
docker build -f Docker-raspi/Dockerfile -t hadashboard .



```






ESP-module:
```
http://www.wch.cn/download/CH341SER_ZIP.html
```

MQTT-stuff:
```
mosquitto_sub -h 192.168.0.140 -u xx -P xx -t /myDevice/sensor/
sudo tcpdump port 1883 -A -t -vvv
```

Bluetooth remove
```
bluetoothctl
scan on
pair [mac]
trust [mac]
connect [connect]
```
