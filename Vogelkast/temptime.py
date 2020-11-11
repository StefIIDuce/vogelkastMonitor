#######################################################################################
# Dit programma moet op de achtergrond gelopen worden voor het vogelkast programma.
#######################################################################################

from time import sleep
import os

while True:
    #Elk uur moet de tijd in temptime.txt ge-update worden voor de temperatuur meting in het hoofdprogramma.
    os.system('date > /home/pi/vogelkast_prog/temptime.txt')
    sleep(3600)