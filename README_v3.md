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
sudo systemctl --system daemon-reload
sudo systemctl enable home-assistant@homeassistant
sudo systemctl start home-assistant@homeassistant
sudo systemctl status home-assistant@homeassistant -l

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
mv deps ./.. #temporarily move deps out of the way
rm .*
git clone git@github.com:ggravlingen/home-assistant.git .
systemctl start home-assistant.service@homeassistant

# Put things in .bash_profile
rm -rf /home/hass/.homeassistant/extraconfig/unix_scripts/bash_profile
ln /root/.bash_profile /home/hass/.homeassistant/extraconfig/unix_scripts/bash_profile


# Install Openzwave
echo 'SUBSYSTEM=="tty", ATTRS{idVendor}=="0658", ATTRS{idProduct}=="0200", SYMLINK+="zwave"' > /etc/udev/rules.d/99-usb-serial.rules
apt-get install cython3 libudev-dev python3-sphinx python3-setuptools git








```
