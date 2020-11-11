#!/bin/bash

echo "Creating directories."
mkdir /home/pi/vogelkast_log
mkdir /home/pi/vogelkast_prog
mkdir /home/pi/camera


echo "Copying files and folders."
# Copy programmes to folder.
cp /home/pi/Vogelkast/temptime.py /home/pi/vogelkast_prog/
cp /home/pi/Vogelkast/Vogelkast.py /home/pi/vogelkast_prog/
# Create text files and initialise their content.
touch /home/pi/vogelkast_prog/camrec.txt
echo 0 > /home/pi/vogelkast_prog/camrec.txt
touch /home/pi/vogelkast_prog/temptime.txt
date > /home/pi/vogelkast_prog/temptime.txt
# Create log text files.
touch /home/pi/vogelkast_log/templog.txt
touch /home/pi/vogelkast_log/vogellog.txt
# Replace dist-packages folder.
sudo rm -r /usr/local/lib/python3.7/dist-packages
sudo cp -r /home/pi/Vogelkast/dist-packages /usr/local/lib/python3.7/


echo "Installing required software."
# Install format software.
sudo apt-get install gpac -y
# Install apache2 webserver.
sudo apt install apache2 -y
sudo rm /var/www/html/index.html
# Install software for wireless acces-point.
sudo apt install hostapd
sudo systemctl unmask hostapd
sudo systemctl enable hostapd
sudo apt install dnsmasq -y
sudo DEBIAN_FRONTEND=noninteractive apt install -y netfilter-persistent iptables-persistent


echo "Replacing configuration files."
# These configuration files are for the wireless acces-point.
sudo rm /etc/dhcpcd.conf
sudo cp /home/pi/Vogelkast/installconfig/dhcpcd.conf /etc/
sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig
sudo cp /home/pi/Vogelkast/installconfig/dnsmasq.conf /etc/
sudo rfkill unblock wlan
sudo cp /home/pi/Vogelkast/installconfig/hostapd.conf /etc/hostapd/
# This config doc is to enable the camera.
sudo rm /boot/config.txt
sudo cp /home/pi/Vogelkast/installconfig/config.txt /boot/


# The last edit to de config files has to be done manually.
x=0
while [ $x -le 25 ]
do
	echo ""
	x=$(( $x + 1 ))
done # This is to make shure the following text stands out.
echo "The following has to be done manually."
echo "Modify the crontab file as instructed by typing the following in the command line:"
echo "sudo crontab -e"
echo "Select the /bin/bash interpreter"
sudo ""
echo "At the bottom of the opened file add the following."
echo "@/home/pi/vogelkast_prog/temptime.py &"
echo "@/home/pi/vogelkast_prog/Vogelkast.py &"
echo "Now exit, save and close by pressing ctrl+x then y then Enter."
echo ""
echo "When done reboot with following command:"
echo "sudo systemctl reboot"

