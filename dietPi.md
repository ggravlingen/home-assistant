Running on DietPi:
Enable: Wi-fi
Enable: Bluetooth
Install: Node.js, Build-essentials, Git client, ssh-client

```

# Install of home assistant and zwave is based on this
# https://deviantengineer.com/2016/09/hass-dietpi/


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

# Optional: only if you're using github
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
  ln /root/.bash_profile /home/hass/.homeassistant/extraconfig/unix_scripts/bash_profile

# pm2 is used to ensure nodjs-scripts are always running
npm install pm2 -g # install
pm2 startup # enable autostart on reboot

# Install Sonos controller
cd /opt
git clone https://github.com/jishi/node-sonos-http-api
cd node-sonos-http-api/
npm install --production
pm2 start server.js
pm2 save

# Setup cron
crontab -e
* 3 * * * cd /home/homeassistant/.homeassistant/extraconfig/python_code && sudo /usr/bin/python sonos_playlist.py > /tmp/listener.log 2>&1
* * * * * cd /home/homeassistant/.homeassistant/extraconfig/webcam && sudo /usr/bin/avconv -i rtsp://192.168.0.59:554/onvif1 -ss 0:0:0 -frames 1 no1.$
2 * * * * cd /home/homeassistant/.homeassistant/extraconfig/unix_scripts && sudo ./check_webcamfile.sh

# Misc
# Not required, this is for my setup only
  # My preferred search tool
  sudo apt-get install locate -y
  sudo updatedb

  # Video monitor
  sudo apt-get install libav-tools -y

  # Misc
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


# Requirement for openzwave
wget ftp://ftp.gnu.org/gnu/libmicrohttpd/libmicrohttpd-0.9.19.tar.gz
tar xf libmicrohttpd-0.9.19.tar.gz   # Extract libmicrohttpd
mv libmicrohttpd-0.9.19 libmicrohttpd && cd libmicrohttpd   # Rename package

wget -O config.sub 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD'   # Grab updated config.sub file
wget -O config.guess 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD'   # Grab updated config.guess file
./configure && make   # Complie libmicrohttpd
make install   # Install libmicrohttpd

# Install Openzwave
# Make a symlink to /dev/zwave instead of trying to figure out what TTY it is on
echo 'SUBSYSTEM=="tty", ATTRS{idVendor}=="0658", ATTRS{idProduct}=="0200", SYMLINK+="zwave"' > /etc/udev/rules.d/99-usb-serial.rules

# Dependencies
apt-get install cython3 libudev-dev python3-sphinx python3-setuptools git

# Activate virtual environment
su -s /bin/bash homeassistant 
cd /srv/homeassistant
source /srv/homeassistant/homeassistant_venv/bin/activate

# Everything below must be run in venv
  pip3 install --upgrade cython==0.24.1

  cd /srv/homeassistant/homeassistant_venv
  mkdir src
  cd src
  git clone https://github.com/OpenZWave/python-openzwave.git
  cd python-openzwave
  git checkout python3

  PYTHON_EXEC=$(which python3) make build
  PYTHON_EXEC=$(which python3) make install

  cd /srv/homeassistant/homeassistant_venv/src
  git clone https://github.com/OpenZWave/open-zwave-control-panel.git
  cd /opt/open-zwave-control-panel && nano Makefile   # Edit Makefile

  # Edit lines 24-25 to be
---
OPENZWAVE := ../python-openzwave/openzwave  
LIBMICROHTTPD := /usr/local/lib/libmicrohttpd.a
---

# Uncomment line 33, and edit to be
---
GNUTLS := -lgnutls -lgcrypt
---

# Uncomment lines 37-38, and Comment out lines 44-45
make   # Compile OZWCP
ln -s /srv/homeassistant/homeassistant_venv/src/python-openzwave/openzwave/config/   # Create symlink for openzwave configs
./ozwcp -p 8888



```
