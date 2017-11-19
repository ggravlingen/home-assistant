```shell

# Install of home assistant and zwave is based on:
# https://deviantengineer.com/2016/09/hass-dietpi/
# Home assistant site
# Guesswork


apt-get update && apt-get -y upgrade   # Make sure we're fully upgraded
apt-get -y install build-essential checkinstall cython3 git htop libgcrypt11-dev libgnutls28-dev libudev-dev libyaml-dev python3-dev python3-pip python3-setuptools python3-sphinx vim python3-venv nmap

apt-get install --upgrade pi-bluetooth
apt-get install --upgrade bluez
apt-get install --upgrade bluez-firmware

sudo useradd -rm homeassistant

# Setup virtual folder
cd /srv
mkdir homeassistant
chown homeassistant:homeassistant homeassistant

# Setup virtual user
su -s /bin/bash homeassistant 
cd /srv/homeassistant
python3 -m venv homeassistant_venv
source /srv/homeassistant/homeassistant_venv/bin/activate

# Install HA
pip3 install homeassistant

# Create systemd script
su -c 'cat <<EOF >> /etc/systemd/system/home-assistant@homeassistant.service
[Unit]
Description=Home Assistant
After=network.target

[Service]
Type=simple
User=homeassistant
ExecStartPre=source /srv/homeassistant/homeassistant_venv/bin/activate
ExecStart=/srv/homeassistant/homeassistant_venv/bin/hass -c "/home/hass/.homeassistant"

[Install]
WantedBy=multi-user.target
EOF'

# Load systemd script and make sure it's working properly
systemctl --system daemon-reload
systemctl enable home-assistant@homeassistant
systemctl start home-assistant@homeassistant
systemctl status home-assistant@homeassistant -l

# Optional, I'm using Github hence these settings
  # Setup ssh
  ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
  eval "$(ssh-agent -s)"
  ssh-add ~/.ssh/id_rsa

  # Git setup and clone settings
  git config --global user.email "you@example.com"
  git config --global user.name "Your Name"
  systemctl stop home-assistant.service@homeassistant

  # nb: .homeassistant-folder must be empty
  cd /home/homeassistant/.homeassistant
  rm -rf * .*
  git clone git@github.com:ggravlingen/home-assistant.git .
  systemctl start home-assistant.service@homeassistant

  # Not needed, I'm using this to backup my bash_profile
  # Manually put things in .bash_profile
  rm -rf /home/hass/.homeassistant/extraconfig/unix_scripts/bash_profile
  ln /root/.bash_profile /home/homeassistant/.homeassistant/extraconfig/unix_scripts/bash_profile

# Optional: recommended if you use nodejs
  # pm2 is used to ensure nodjs-scripts are always running
  npm install pm2 -g # install
  pm2 startup # enable autostart on reboot

# Optional: a nodejs-based Sonos controller
  # Install Sonos controller
  cd /opt
  git clone https://github.com/jishi/node-sonos-http-api
  cd node-sonos-http-api/
  npm install --production
  pm2 start server.js
  pm2 save

# Optional: my settings for cron
  # Setup cron
  crontab -e
  * 3 * * * cd /home/homeassistant/.homeassistant/extraconfig/python_code && sudo /usr/bin/python3 sonos_playlist.py > /tmp/listener.log 2>&1
  0 0 * * * cd /home/homeassistant/.homeassistant/extraconfig/python_code && sudo /usr/bin/python3 dropbox.py > /tmp/backup.log 2>&1


# Optional
  # Misc
  # My preferred search tool
  sudo apt-get install locate -y
  sudo updatedb

  # Video monitor
  sudo apt-get install libav-tools -y

  # Misc 2
  echo -e "curl -H "Content-Type: application/json" -X POST -d '{"topic": "/location/patrik_iphone", "payload": "Home" }' http://localhost:8123/api/services/mqtt/publish?api_password=" > set_home.sh && sudo chmod +x set_home.sh

# MQTT
sudo apt-get install libwebsockets-dev
useradd mosquitto
cd /var/lib/
mkdir mosquitto
chown mosquitto:mosquitto mosquitto
cd /srv/homeassistant/homeassistant_venv/src
curl -O http://repo.mosquitto.org/debian/mosquitto-repo.gpg.key
apt-key add mosquitto-repo.gpg.key
cd /etc/apt/sources.list.d/
curl -O http://repo.mosquitto.org/debian/mosquitto-jessie.list
apt-get update
apt-cache search mosquitto
apt-get install -y mosquitto mosquitto-clients
cd /etc/mosquitto
touch pwfile
chown mosquitto: pwfile
chmod 0600 pwfile
sudo mosquitto_passwd -b pwfile pi raspberry
sudo chown mosquitto: mosquitto.conf


# Make a symlink to /dev/zwave instead of trying to figure out what TTY it is on
echo 'SUBSYSTEM=="tty", ATTRS{idVendor}=="0658", ATTRS{idProduct}=="0200", SYMLINK+="zwave"' > /etc/udev/rules.d/99-usb-serial.rules

# Make sure homeassistant has write access to /dev/zwave
usermod -G root -a homeassistant

# For backup purposes
# https://www.raspberrypi.org/forums/viewtopic.php?f=63&t=164166
ln /home/homeassistant/.homeassistant/google_calendars.yaml /home/homeassistant/haconf/google_calendars.yaml
ln /home/homeassistant/.homeassistant/.google.token /home/homeassistant/haconf/.google.token
ln /home/homeassistant/.homeassistant/ha_conf.rb /home/homeassistant/haconf/ha_conf.rb
ln /home/homeassistant/.homeassistant/known_devices.yaml /home/homeassistant/haconf/known_devices.yaml
ln /home/homeassistant/.homeassistant/phue.conf /home/homeassistant/haconf/phue.conf
ln /home/homeassistant/.homeassistant/secrets.yaml /home/homeassistant/haconf/secrets.yaml
ln /home/homeassistant/.homeassistant/zwcfg_0xcf3eab81.xml /home/homeassistant/haconf/zwcfg_0xcf3eab81.xml
ln /home/homeassistant/.homeassistant/zwscene.xml /home/homeassistant/haconf/zwscene.xml
ln /home/homeassistant/.homeassistant/webostv.conf /home/homeassistant/haconf/webostv.conf
ln /srv/homeassistant/homeassistant_venv/src/python-openzwave/openzwave/config/options.xml /home/homeassistant/haconf/options.xml
ln /home/homeassistant/.homeassistant/tradfri.conf /home/homeassistant/haconf/tradfri.conf
ln /home/homeassistant/.homeassistant/.ios.conf /home/homeassistant/haconf/.ios.conf


# Homebridge
  sudo apt-get install libavahi-compat-libdnssd-dev
  npm install -g node-gyp
  npm install -g --unsafe-perm homebridge hap-nodejs

  cd /usr/local/lib/node_modules/homebridge/
  sudo npm install --unsafe-perm bignum
  cd /usr/local/lib/node_modules/hap-nodejs/node_modules/mdns
  sudo node-gyp BUILDTYPE=Release rebuild

  npm install -g homebridge-homeassistant

  sudo npm upgrade -g homebridge-homeassistant

  ln /root/.homebridge/config.json /home/homeassistant/haconf/homebridge.conf


# Bluetooth remote
bluetoothctl
scan on
pair [mac]
trust [mac]
connect [connect]


# Install docker
curl -sSL https://get.docker.com | sh

mosquitto_sub -t /location/patrik_iphone -q 1
curl -X POST -H "x-ha-access: pwd" -H "Content-Type: application/json" -d '{"payload": "Home", "topic": "/location/patrik_iphone"}' http://localhost:8123//api/services/mqtt/publish
# #123
pip3 install colorlog

###
###
### Install syslog-ng
apt-get install syslog-ng

# Add to syslog conf
source s_net { udp(ip(0.0.0.0) port(514)); };
destination d_router { file("/var/log/remote/${HOST}/${YEAR}_${MONTH}_${DAY}.log" create-dirs(yes)); }; # put files in tidy order

log { source(s_net); destination(d_router); };

sudo service syslog-ng restart

#Grafana
https://github.com/fg2it/grafana-on-raspberry/wiki


```
