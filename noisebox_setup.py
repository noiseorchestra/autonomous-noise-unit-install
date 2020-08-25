import subprocess
import os
from shutil import copy
import socket
import enquiries
from colored import fg, attr

green = fg(2)
res = attr('reset')

root = '/home/pi/autonomous-noise-unit-install/'

# CONFIGURE NOISEBOX

if 'noisebox' not in socket.gethostname():
    print(green + '\nDefault RPi password not safe, please choose a new one: ' + res)
    subprocess.run('sudo passwd pi', shell=True)

id = input(green + '\nPlease enter the ID no. of this noisebox (1, 2, 3, 4 etc...): ' + res)

soundcards = ['pisound', 'hifiberry-dacplusadc', 'none']
print(green + '\nWhich audio device do you want to use?:' + res)
soundcard = enquiries.choose('', soundcards)

print(green + '\nAudio interface:', soundcard + res)

# NOISEBOX DEPENDENCIES

subprocess.run('sudo bash ' + root + 'dependencies/noisebox.sh', shell=True)

# NOISEBOX CONFIG FILE

if os.path.isfile(root + 'custom_config/noisebox/config.ini'):
    copy(root + 'custom_config/noisebox/config.ini', '/home/pi/noisebox/config.ini')

# RPi HOSTNAME

print(green + 'Configuring RPi hostname...' + res)
print('127.0.1.' + id + ' noisebox' + id)

copy(root + 'rpi_config/hosts', '/etc/hosts')

with open('/etc/hosts', 'a') as hosts:
    hosts.write('127.0.1.' + id + ' noisebox' + id)

with open('/etc/hostname', 'w') as hostname:
    hostname.write('noisebox' + id)

# SYSTEMD

print(green + '\nConfiguring Noisebox daemon...' + res)

subprocess.run('sudo cproot +  rpi_config/noisebox.service /lib/systemd/system/noisebox.service', shell=True)
subprocess.run('sudo systemctl daemon-reload', shell=True)
subprocess.run('sudo systemctl enable noisebox.service', shell=True)

# RPi AUDIO

print(green + 'Configuring RPi soundcard and audio...' + res)

copy(root + 'rpi_config/config.txt', '/boot')
copy(root + 'rpi_config/profile', '/etc/profile')

with open('/etc/profile', 'a') as profile:
    profile.write('export JACK_NO_AUDIO_RESERVATION=1')

# SOUNDCARD > PISOUND

if soundcard == 'pisound':
    print(green + 'Configuring pisound soundcard...' + res)
    print(green + 'Installing pisound software...' + res)

    subprocess.call('curl -s https://blokas.io/pisound/install.sh  | sh', shell=True)

    with open('/boot/config.txt', 'a') as config:
        config.write('dtparam=audio=off\n')
        config.write('dtoverlay=pisound\n')

    # disable pisound services
    subprocess.run('sudo systemctl daemon-reload', shell=True)
    subprocess.run('sudo systemctl disable pisound-btn', shell=True)
    subprocess.run('sudo systemctl disable pisound-ctl', shell=True)

# SOUNDCARD > HIFIBERRY

if soundcard == 'hifiberry-dacplusadc':
    print(green + 'Configuring Hifiberry soundcard...' + res)
    with open('/boot/config.txt', 'a') as config:
        config.write('dtparam=audio=off\n')
        config.write('dtoverlay=hifiberry-dacplusadc\n')

# SOUNDCARD > NONE

if soundcard == 'none':
    print(green + 'Configuring inbuilt audio...' + res)
    with open('/boot/config.txt', 'a') as config:
        config.write('dtparam=audio=on\n')

# OLED

print(green + 'Configuring OLED...' + res)
copy(root + 'rpi_config/modules', '/etc/modules')

# VPN

if os.path.isfile(root + 'custom_config/vpncloud/vpncloud.txt'):

    print(green + 'Configuring vpncloud for remote access...' + res)

    subprocess.run('sudo bash ' + root + 'dependencies/vpncloud.sh', shell=True)
    copy('/etc/vpncloud/example.net.disabled', '/etc/vpncloud/mynet.net')
    f = open(file=root + 'custom_config/vpncloud/vpncloud.txt', mode='r')
    vpncloud_append = f.read()
    f.close()

    with open('/etc/vpncloud/mynet.net', 'a') as vpncloud_config:
        vpncloud_config.write(str(vpncloud_append))
        vpncloud_config.write("ifup: 'ifconfig $IFNAME 10.0.0.' + id + '/24 mtu 1500'\n")
        vpncloud_config.write('statsd_prefix: noisebox' + id + '\n')

    f = open(file=root + 'custom_config/vpncloud/hosts.txt', mode='r')
    vpncloud_hosts = f.read()
    f.close()

    with open('/etc/hosts', 'a') as hosts:
        # this isn't working
        hosts.write(str(vpncloud_hosts))

    subprocess.run('sudo systemctl enable vpncloud@mynet', shell=True)

else:
    print(green + 'Skipping vpncloud configuration.' + res)


# TELEGRAF METRICS

if os.path.isfile(root + 'custom_config/telegraf/telegraf.conf'):

    print(green + 'Configuring telegraf metrics server...' + res)

    subprocess.run('sudo bash ' + root + 'dependencies/telegraf.sh', shell=True)
    subprocess.run('usermod -aG video telegraf', shell=True)
    subprocess.run("setcap 'cap_net_admin,cap_net_raw+ep' $(which ping)", shell=True)
    copy(root + 'custom_config/telegraf/telegraf.conf', '/etc/telegraf/telegraf.conf')
else:
    print(green + 'Skipping telegraf configuration.' + res)

print(green + '\nInstallation complete!' + res)
print(green + '\nRebooting system.' + res)

subprocess.run('sudo reboot', shell=True)
