This is the configuration I'm using for my Home Assistant instance, which is running on a Raspberry Pi 3 (model b).

Cron run as root:
```
* 3 * * * cd /home/hass/.homeassistant/extraconfig/python_code && sudo /usr/bin/sonos_playlist.py > /tmp/listener.log 2>&1
* * * * * cd /home/hass/.homeassistant/extraconfig/webcam && sudo /usr/bin/avconv -i rtsp://192.168.0.59:554/onvif1 -ss 0:0:0 -frames 1 no1.jpg
2 * * * * cd /home/hass/.homeassistant/extraconfig/unix_scripts && sudo ./check_webcamfile.sh
```


Running device detection through IFTTT on iOS. The JSON below is what I sending through Maker:

```
curl -H "Content-Type: application/json" -X POST -d '{"topic": "/location/patrik_iphone", "payload": "Home" }' http://IP:8123/api/services/mqtt/publish?api_password=
```

Wi-fi:
```
sudo nano /etc/wpa_supplicant/wpa_supplicant.conf
network={
               ssid="home"
               psk="very secret passphrase"
          }
```


Bluez:
```
wget http://www.kernel.org/pub/linux/bluetooth/bluez-5.42.tar.xz
tar -xvf bluez-5.42.tar.xz
cd bluez-5.42

sudo apt-get update
sudo apt-get install -y libusb-dev libdbus-1-dev libglib2.0-dev libudev-dev libical-dev libreadline-dev

./configure
make
sudo make install

sudo cp attrib/gatttool /usr/local/bin/

systemctl status bluetooth
sudo systemctl start bluetooth
sudo systemctl enable bluetooth

sudo nano /lib/systemd/system/bluetooth.service
ExecStart=/usr/local/libexec/bluetooth/bluetoothd --experimental               
                                                  ^^^^^^^^^^^^
sudo systemctl daemon-reload
sudo systemctl restart bluetooth
```

Github:
```
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa
```

Misc:
```
sudo ln /home/pi/.bash_profile bash_profile
sudo ln /home/hass/.homeassistant/.gitignore gitignore

#Avconv
sudo apt-get install libav-tools
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

Monit:
```
sudo apt-get install monit
sudo nano /etc/monit/monitrc
sudo monit 
```

MQTT-stuff:
```
mosquitto_sub -h 192.168.0.140 -u xx -P xx -t /myDevice/sensor/
sudo tcpdump port 1883 -A -t -vvv
```
