#!/bin/bash

set -e

trap 'catch_err' ERR

catch_err() {
  tput setaf 1; printf "\nERROR: Installation not complete\n"; tput sgr0;
  kill -l SIGINT >> /dev/null 2>&1
}

cat /home/pi/autonomous-noise-unit-install/logo.txt

while true; do
    tput setaf 2; printf "\nWelcome! This script will setup your Raspberry Pi as a NoiseBox, do you want to continue (y/n)? : "; tput sgr0; read yn
    case $yn in
        [Yy]* ) tput setaf 2; printf "\nGreat! Let's go...\n"; tput sgr0; break;;
        [Nn]* ) printf "\nOkay, goodbye."; exit;;
        * ) printf "\nPlease answer yes or no.";;
    esac
done

# INSTALLER DEPENDENCIES
sudo apt-get update
sudo apt-get install python3-pip -y
sudo -H pip3 install enquiries colored

# RUN noisebox_setup.py

sudo python3 /home/pi/autonomous-noise-unit-install/noisebox_setup.py
