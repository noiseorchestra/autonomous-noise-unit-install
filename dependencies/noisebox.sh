#!/bin/bash

# update system

sudo apt update
sudo apt full-upgrade -y

#install noisebox

sudo apt-get install -y git
if [ -d "/home/pi/autonomous-noise-unit" ]
then
  sudo rm -r /home/pi/autonomous-noise-unit
fi

sudo -u pi mkdir /home/pi/autonomous-noise-unit
sudo -u pi git clone https://github.com/noiseorchestra/autonomous-noise-unit.git /home/pi/autonomous-noise-unit
pip3 install -r /home/pi/autonomous-noise-unit/requirements.txt

#install OLED dependencies

sudo apt-get install -y python3-dev python-smbus i2c-tools python3-pil python3-pip python3-setuptools python3-rpi.gpio
sudo apt-get install -y libopenjp2-7-dev

#install meter_bridge

wget -c https://www.aelius.com/njh/jackmeter/jackmeter-0.4.tar.gz -O - | tar -xz
sudo apt-get install -y libjack-jackd2-dev
cd jackmeter-0.4/
./configure
make
sudo make install
