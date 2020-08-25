#!/bin/bash

# install vpncloud dependencies

printf "deb https://repo.ddswd.de/deb stable main" | sudo tee /etc/apt/sources.list.d/vpncloud.list > /dev/null
wget https://repo.ddswd.de/deb/public.key -qO - | sudo apt-key add
sudo apt-get update

#install vpncloud

sudo apt-get -y install vpncloud
