[?1049h[1;48r(B[m[4l[?7h[?12l[?25h[?1h=[?1h=[?1h=[39;49m[39;49m(B[m[H[2J(B[0;7m  GNU nano 2.2.6                                        File: README.md                                                                                        [3;1H(B[mRunning on DietPi:[4dEnable: Wi-fi[5dEnable: Bluetooth[6dInstall: Node.js, Build-essentials, Git client, ssh-client[8d```[10d# Install of home assistant and zwave is based on:[11d# https://deviantengineer.com/2016/09/hass-dietpi/[12d# Home assistant site[13d# Guesswork[16dapt-get update && apt-get -y upgrade   # Make sure we're fully upgraded[17dapt-get -y install build-essential checkinstall cython3 git htop libgcrypt11-dev libgnutls28-dev libudev-dev libyaml-dev python3-dev python3-pip python3-setup$[19;1Hapt-get install --upgrade pi-bluetooth[20dapt-get install --upgrade bluez[21dapt-get install --upgrade bluez-firmware[23dsudo useradd -rm homeassistant[25d# Setup virtual folder[26dcd /srv[27dmkdir homeassistant[28dchown homeassistant:homeassistant homeassistant[30d# Setup virtual user[31dsu -s /bin/bash homeassistant[32dcd /srv/homeassistant[33dpython3 -m venv homeassistant_venv[34dsource /srv/homeassistant/homeassistant_venv/bin/activate[36d# Install HA[37dpip3 install homeassistant[39d# Create systemd script[40dsu -c 'cat <<EOF >> /etc/systemd/system/home-assistant@homeassistant.service[41d[Unit][42dDescription=Home Assistant[43dAfter=network.target[45d[Service][46;71H(B[0;7m[ Read 228 lines ][47d^G(B[m Get Help[47;27H(B[0;7m^O(B[m WriteOut[47;53H(B[0;7m^R(B[m Read File[47;79H(B[0;7m^Y(B[m Prev Page[47;105H(B[0;7m^K(B[m Cut Text[47;131H(B[0;7m^C(B[m Cur Pos[48d(B[0;7m^X(B[m Exit[48;27H(B[0;7m^J(B[m Justify[48;53H(B[0;7m^W(B[m Where Is[48;79H(B[0;7m^V(B[m Next Page[48;105H(B[0;7m^U(B[m UnCut Text[48;131H(B[0;7m^T(B[m To Spell[3d[46;54H(B[0;7m[ line 1/229 (0%), col 1/19 (5%), char 0/7678 (0%) ][3d(B[m[2;45r[2;1HM[1;48r[1;150H(B[0;7mModified[4d(B[m[48;1H[?1049l[?1l>[48;1H[?1049l[?1l>