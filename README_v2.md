Running on DietPi
```
DietPi setup:
Enable: Wi-fi
Enable: Bluetooth
Install: Node.js, Build-essentials, Git client, ssh-client

# Install of home assistant and zwave is based on this work https://deviantengineer.com/2016/09/hass-dietpi/
# Difference is that I am using default hass AIO directory for compatability with some of my old config-files

# Upgrade everything
apt-get update && apt-get -y upgrade

# Install dependencies
apt-get -y install build-essential checkinstall cython3 git htop libgcrypt11-dev libgnutls28-dev libudev-dev libyaml-dev python3-dev python3-pip python3-setuptools python3-sphinx vim   # Pre-requisites
pip3 install astral netdisco==0.7.1 pyyaml xmltodict   # Install HASS prereqs (for additional functionality)

# Install Home Assistant
pip3 install homeassistant   # Install latest Home Assistant release

pico /etc/systemd/system/hass.service   # Create hass (Home Assistant) systemd file

[Unit]
Description=Home Assistant (hass) Daemon
After=syslog.target network.target

[Service]
Type=forking
ExecStart=/usr/local/bin/hass -v --config /home/hass/.homeassistant --pid-file /var/run/hass.pid --daemon
PIDFile=/var/run/hass.pid

[Install]
WantedBy=multi-user.target

# End of systemd-file

# Reload systemd files
chmod +x /etc/systemd/system/hass.service && systemctl daemon-reload

# Generate configration files
systemctl start hass.service && sleep 5 &&  systemctl stop hass.service

# Create a link to /dev/zwave for the zwave-controller
echo 'SUBSYSTEM=="tty", ATTRS{idVendor}=="0658", ATTRS{idProduct}=="0200", SYMLINK+="zwave"' > /etc/udev/rules.d/99-usb-serial.rules

# Install python zwave
cd /opt && git clone https://github.com/OpenZWave/python-openzwave.git   # Grab python-openzwave
cd /opt/python-openzwave && git checkout python3   # Checkout python3 branch
PYTHON_EXEC=$(which python3) make build   # Compile python-openzwave
PYTHON_EXEC=$(which python3) make install   # Install python-openzwave

# Install openzwave controller
cd /opt && wget ftp://ftp.gnu.org/gnu/libmicrohttpd/libmicrohttpd-0.9.19.tar.gz   # Grab libmicrohttpd (dependency for OZWCP)
tar xf libmicrohttpd-0.9.19.tar.gz   # Extract libmicrohttpd
mv libmicrohttpd-0.9.19 libmicrohttpd && cd libmicrohttpd   # Rename package
wget -O config.sub 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD'   # Grab updated config.sub file
wget -O config.guess 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD'   # Grab updated config.guess file
./configure && make   # Complie libmicrohttpd
make install   # Install libmicrohttpd
cd /opt && git clone https://github.com/OpenZWave/open-zwave-control-panel.git   # Grab open zwave control panel (OZWCP)
cd /opt/open-zwave-control-panel && vim Makefile   # Edit Makefile
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
ln -s /opt/python-openzwave/openzwave/config   # Create symlink for openzwave configs
./ozwcp -p 8888   # Start ozwcp as a test (note, OZWCP and HASS should never both be running at the same time -- stop HASS before starting OZWCP, and kill OZWCP before starting HASS)

  config_path: /usr/local/lib/python3.4/dist-packages/libopenzwave-0.3.1-py3.4-linux-aarch64.egg/config

systemctl enable hass.service   # Enable HASS to run at system start
rm -rf /opt/libmicrohttpd*   # Cleanup unnecessary libmicrohttpd files
systemctl reboot   # Reboot server

# SSH setup
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa

# Git setup and clone settings
git config --global user.email "you@example.com"
git config --global user.name "Your Name"
systemctl stop home-assistant.service

# nb: .homeassistant-folder must be empty
cd /home/hass/.homeassistant
mv deps ./.. #temporarily move deps out of the way
rm .*
git clone git@github.com:ggravlingen/home-assistant.git .
chown -R hass.hass *

# Backup bash profile and gitingore
pico ~/.bash_profile
rm -rf /home/hass/.homeassistant/extraconfig/unix_scripts/bash_profile
ln /home/pi/.bash_profile /home/hass/.homeassistant/extraconfig/unix_scripts/bash_profile




```
