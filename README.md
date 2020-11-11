# vogelkastMonitor

This README contains only a simple and quick step-by-step explanation for what must be
done to install the software.
So we asume that all required hardware components have been gathered, the hardware
setup is complete and only the software installation is left.
For more information regarding the installation and build of systems software
and hardware components consult the Wiki tab above.

The main Code tab above contains only 1 one folder, two files and three png's.
The folder contains the installation script, configuration files, main programmes
and necessary libraries.
The two files are for the RPi os.
The three png's show the setup of the hardware.

The first thing that must be done is downloading the raspbian os from the following link:
https://www.raspberrypi.org/downloads/raspberry-pi-os/
Pick the one with desktop and recommended software. This may take a few minutes.
Then download the code in Code tab as zip file.
Unzip it after download.

Insert the micro SD card into the PC's SD card port and open the balenaEtcher app.
We're going to flash the raspbian os onto the SD card. Make sure the SD card and os
are selected, then Flash.
Now remove and re-insert the SD card.
Open the wpa_supplicant.conf file and edit the contents of ssid and psk with the name
and password of you're wifi network. Also change the value of country to match the 
ISO 3166 alpha-2 country code of your country if necessary. When done save.
If the country code had to be changed edit inside the Vogelkast folder inside installconfig
the hostapd.conf file's country_code line to match.
This one isn't required but for extra security edit the wpa_passphrase in hostapd.conf
and change the password to you're liking, if not the default password for the wireless
acces-point is Anno20202021.

Open the SD card in the file explorer, then paste the ssh and wpa_supplicant.conf files
inside. Eject the SD card.

Preparing the raspbian os is now done. Insert the SD card into the RPi, connect all
external hardware(mouse, keyboard, screen), then power on the RPi.

When booting up for the first time the RPi will ask several questions, do these then it
will ask to download updates, agree then reboot the RPi.

After reboot open the file explorer from RPi.
On the PC place the Vogelkast folder on a USB drive then bring it over to the RPi, place
this folder in the /home/pi directory

Open a command line terminal and type:
cd Vogelkast
We need to give execute rights to the vogelkast.sh file so it can perform the final
installations.
Do this with:
chmod 777 vogelkast.sh
Now run the shell script with:
./vogelkast.sh

The final edit needs to be done manually, do the following steps.
To make shure the main programmes run on boot we need to edit crontab with:
sudo crontab -e
Select the bin/bash/ interpreter.
At the very bottom of the opened file add the following:

@/home/pi/vogelkast_prog/temptime.py &
@/home/pi/vogelkast_prog/Vogelkast.py &

Save and close the file.
Finally reboot with:
sudo systemctl reboot

With this the installation is complete, have fun.
