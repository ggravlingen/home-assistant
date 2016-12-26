Running on DietPi:
Enable: Wi-fi
Enable: Bluetooth
Install: Node.js, Build-essentials, Git client, ssh-client

```

# Install of home assistant and zwave is based on this
# https://deviantengineer.com/2016/09/hass-dietpi/


apt-get update && apt-get -y upgrade   # Make sure we're fully upgraded
apt-get -y install build-essential checkinstall cython3 git htop libgcrypt11-dev libgnutls28-dev libudev-dev libyaml-dev python3-dev python3-pip python3-setuptools python3-sphinx vim python3-venv

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

pico /etc/systemd/system/hass.service   # Create hass (Home Assistant) systemd file

[Unit]
Description=Home Assistant
After=network.target

[Service]
Type=simple
User=homeassistant
ExecStartPre=source /srv/homeassistant/bin/activate
ExecStart=/srv/homeassistant/bin/hass -c "/home/hass/.homeassistant"

[Install]
WantedBy=multi-user.target

# End systemd file here

systemctl --system daemon-reload
systemctl enable hass.service
systemctl start hass.service















```
