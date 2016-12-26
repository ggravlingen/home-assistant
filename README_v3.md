```

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

```
