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

#Update system
sudo apt-get update
sudo apt-get upgrade

# SSH setup
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa

# Git setup and clone settings
sudo apt-get install git
sudo git config --global user.email "you@example.com"
sudo git config --global user.name "Your Name"
sudo systemctl stop home-assistant@homeassistant.service

# nb: .homeassistant-folder must be empty
cd /home/homeassistant/.homeassistant
sudo git clone git@github.com:ggravlingen/home-assistant.git .
sudo chown -R homeassistant.homeassistant *

# Backup bask profile and gitingore (gitignore not needed anymore?)
sudo rm -rf /home/homeassistant/.homeassistant/extraconfig/unix_scripts/bash_profile
sudo ln /home/pi/.bash_profile /home/homeassistant/.homeassistant/extraconfig/unix_scripts/bash_profile

sudo rm /home/homeassistant/.homeassistant/extraconfig/unix_scripts/gitignore
sudo ln /home/homeassistant/.homeassistant/.gitignore /home/homeassistant/.homeassistant/extraconfig/unix_scripts/gitignore


# Zwave
sudo apt-get install cython3 libudev-dev python3-sphinx python3-setuptools git -y
sudo pip3 install --upgrade cython==0.24.1

cd
git clone https://github.com/OpenZWave/python-openzwave.git
cd python-openzwave
git checkout python3
PYTHON_EXEC=$(which python3) make build
sudo PYTHON_EXEC=$(which python3) make install

# MQTT
systemctl start mosquitto
systemctl enable mosquitto

# Enable google cal (check states for info)

# Video monitor
sudo apt-get install libav-tools



```



Cron run as root:
```
* 3 * * * cd /home/hass/.homeassistant/extraconfig/python_code && sudo /usr/bin/sonos_playlist.py > /tmp/listener.log 2>&1
* * * * * cd /home/hass/.homeassistant/extraconfig/webcam && sudo /usr/bin/avconv -i rtsp://192.168.0.59:554/onvif1 -ss 0:0:0 -frames 1 no1.jpg
2 * * * * cd /home/hass/.homeassistant/extraconfig/unix_scripts && sudo ./check_webcamfile.sh
```


Running device detection through IFTTT on iOS. The JSON below is what I sending through Maker:

```
curl -H "Content-Type: application/json" -X POST -d '{"topic": "/location/patrik_iphone", "payload": "Home" }' http://IP:8123/api/services/mqtt/publish?api_password= > /home/pi/set_home.sh
```




Plex:
```
sudo apt-get update && sudo apt-get upgrade -y  
sudo apt-get update && sudo apt-get dist-upgrade  
sudo apt-get install apt-transport-https -y --force-yes  
wget -O - https://dev2day.de/pms/dev2day-pms.gpg.key  | sudo apt-key add -  
echo "deb https://dev2day.de/pms/ jessie main" | sudo tee /etc/apt/sources.list.d/pms.list  
sudo apt-get update  
sudo apt-get install -t jessie plexmediaserver -y  
sudo reboot  
```

Node:
```
curl -sL https://deb.nodesource.com/setup_4.x | sudo -E bash -
sudo apt-get install -y nodejs
```

PM2:
```
npm install pm2 -g 
pm2 startup
pm2 start app.js
pm2 save

```

Sonos:
```
cd /opt
sudo git clone https://github.com/jishi/node-sonos-http-api
sudo 
npm install --production
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



$ sudo systemctl stop home-assistant@homeassistant.service 
$ sudo su -s /bin/bash homeassistant
$  source /srv/homeassistant/bin/activate
$ pip3 install --upgrade homeassistant
$ exit
$ sudo systemctl start home-assistant@homeassistant.service
