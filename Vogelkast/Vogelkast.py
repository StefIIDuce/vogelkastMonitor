#######################################################################################
# Het project is het bouwen van een vogelkast monitor met de volgende mogelijkheden:
# Het moet opnames maken van vogels wanneer deze gedecteerd zijn.
# Opname stoppen als er geen vogel aanwezig is.
# Opname ook stop zetten na een bepaalde tijd: hier 5min.
# Opnames beschikbaar maken buitenaf op afstand.
# Geluidsopnames maken.
# Temperatuur meten zowel binnen als buiten de vogelkast.
# Log maken van temperatuur en vogels.
#
# Hiervoor wordt de volgende hardware toegepast:
# 2X Temperatuur sensoren (Type DHT11)
# IR-Camera ()
# Mic + Speaker
# Bewegingssensor (PIR sensor)
#
# Deze versie werkt met maar één DHT sensor. Voor een tweede DHT sensor te gebruiken
# uncomment #1 lijnen en comment #2 lijnen.
# Deze versie bevat geen mic dus deze functie is niet aanwezig.
#######################################################################################

from gpiozero import MotionSensor
from time import sleep
from picamera import PiCamera
import Adafruit_DHT as DHT
import os

#Declaraties.
pir = MotionSensor(17)
tempsens = DHT.DHT11
cam = PiCamera()

#Initialiseer startwaardes.
cam.resolution = (720, 480) #Stel de camera resolutie in.
#cam.rotation = 180 #Uncomment dit om de camera 180° te draaien. Andere waardes zijn 0, 90 en 270.
#Haal de laatste teller waarde als string uit camrec.
fb  = open('/home/pi/vogelkast_prog/camrec.txt', 'r') #Open text file in read mode.
teller = fb.read()
tel = int(teller) #Sla de teller waarde ook op als integer.
teller = str(tel) #Bij de initialisatie van camrec.txt wordt een \n caracter geplaats, dit wordt gefixt na de eerste loop.
fb.close() #Sluit camrec text file.
#Initialiseer formaat inhoud. Deze string wordt gebruikt om vids te formateren van h264 naar mp4.
formaat = "MP4Box -add /home/pi/camera/vid" +teller+ ".h264 /home/pi/camera/vid" +teller+ ".mp4"
#Sla de tijd voor de temperatuur meting op om tempT te initialiseren.
fb = open('/home/pi/vogelkast_prog/temptime.txt', 'r')
tempT = fb.readline()
fb.close()
sect = "00" #Deze moet bijhouden wanneer de laatste temp meting was.
norec = False #Deze bevestigd of er een opname gemaakt is.

#Deze functie maakt de opnames bij detectering van beweging.
def maak_opname():
	global norec
	if pir.wait_for_motion(5): #Wacht 5sec voor beweging. Zodat het programma hier niet vast zit.
		#start recording.
		print("start recording")
		#cam.start_preview() #De preview was voor de camera resolutie te testen
		cam.start_recording('/home/pi/camera/vid%s.h264' %tel) #Start opname met opslag folder.
		if pir.wait_for_no_motion(300): #Wacht 5min voor geen beweging.
			print("no more motion detected")
		else:
			print("5min exeeded")
		#stop recording.
		print("stop recording")
		cam.stop_recording() #Stop opname.
		#cam.stop_preview()
		norec = False
		return
	else:
		norec = True #Geen opname.
		return

#Deze functie maakt de temperatuur meting.
def meet_temp():
	global tempT #tempT en sect zijn globaal.
	global sect
	#Eerst moet het huidige uur uit de temptime.txt file geïsoleerd worden.
	dp = tempT[17:18] #Zoek waar het eerste dubbel punt staat.
	if dp == ':': 
		dp = tempT[15:17] #Isoleer het uur.
		if dp != sect: #Als het uur verschilt van de laatste meting.
			#Nu kan de temperatuur meting gemaakt worden.
			hum, temp = DHT.read_retry(tempsens, 4) #Meet temperatuur en luchtvochtigheid.
			#hum2, temp2 = DHT.read_retry(tempsens, 18) #Meet temperatuur en luchtvochtigheid. #1
			tempf = temp * 9/5.0 + 32 #Zet temperatuur om naar Fahrenheit.
			#tempf2 = temp2 * 9/5.0 + 32 #Zet temperatuur om naar Fahrenheit. #1
			hum = str(hum) #Verander de metingen naar strings.
			temp = str(temp)
			tempf = str(tempf)
			#hum2 = str(hum2) #1
			#temp2 = str(temp2) #1
			#tempf2 = str(tempf2) #1
			#Maak de string inhoud voor temptlog.
			temptxt = tempT+ "Temp: " +temp+ "°C  " +tempf+ "F\nHum:  " +hum+ "%\n\n" #2
			#temptxt = tempT+ "Binnen:\n  Temp: " +temp+ "°C  " +tempf+ "F\n  Hum:  " +hum+ "%\nBuiten:\n  Temp: " +temp2+ "°C  " +tempf2+ "F\n  Hum:  " +hum2+ "%\n\n" #1
			#Update inhoud variabelen en temperatuur log file.
			fb = open('/home/pi/vogelkast_log/templog.txt', 'a')
			fb.write(temptxt) #Schrijf de temptxt inhoud in de templog.txt file.
			fb.close()
			sect = dp #Update sect inhoud met huidige uur.
			return #Ga terug naar hoofdlus na meting en log.
		else: #Zijn ze hetzelfde, maak dan geen meting.
			fb = open('/home/pi/vogelkast_prog/temptime.txt', 'r')
			tempT = fb.readline() #Update tempT inhoud.
			fb.close()
			return
	else: #Indien niet daar.
		dp = tempT[18:19] #Zoek tweede plaats waar het eerste dubbel punt kan staat.
		if dp == ':':
			dp = tempT[16:18] #Isoleer het uur.
			if dp != sect:
				#Nu kan de temperatuur meting gemaakt worden.
				hum, temp = DHT.read_retry(tempsens, 4)
				#hum2, temp2 = DHT.read_retry(tempsens, 18) #1
				tempf = temp * 9/5.0 + 32
				#tempf2 = temp2 * 9/5.0 + 32 #1
				hum = str(hum)
				temp = str(temp)
				tempf = str(tempf)
				#hum2 = str(hum2) #1
				#temp2 = str(temp2) #1
				#tempf2 = str(tempf2) #1
				#Maak de string inhoud voor temptlog.
				temptxt = tempT+ "Temp: " +temp+ "°C  " +tempf+ "F\nHum:  " +hum+ "%\n\n" #2
				#temptxt = tempT+ "Binnen:\n  Temp: " +temp+ "°C  " +tempf+ "F\n  Hum:  " +hum+ "%\nBuiten:\n  Temp: " +temp2+ "°C  " +tempf2+ "F\n  Hum:  " +hum2+ "%\n\n" #1
				#Update inhoud variabelen en temperatuur log file.
				fb = open('/home/pi/vogelkast_log/templog.txt', 'a')
				fb.write(temptxt)
				fb.close()
				sect = dp
				return
			else: #Zijn ze hetzelfde, maak dan geen meting.
				fb = open('/home/pi/vogelkast_prog/temptime.txt', 'r')
				tempT = fb.readline()
				fb.close()
				return
		else:
			return #Onderbreek temperatuur meting als het uur niet gevonden kan worden.

#Deze functie formateerd de vids en update alle variabelen en logs voor de volgende loop.
def update_var_form():
	#Deze variabelen zijn globaal, anders ziet de functie ze niet.
	global formaat
	global tel
	global teller
	global norec
	if norec == False:
		x = "vid" +teller+ ".mp4 "
		os.system(formaat) #Vorm formaat om naar mp4.
		os.system('rm /home/pi/camera/vid%s.h264' %tel) #Verwijder oorspronkelijke file.
		#Update de variabelen.
		tel = tel + 1 #Update integer teller waarde.
		teller = str(tel) #update string teller waarde.
		formaat = "MP4Box -add /home/pi/camera/vid" +teller+ ".h264 /home/pi/camera/vid" +teller+ ".mp4"
		#Update de logs.
		fb = open('/home/pi/vogelkast_prog/camrec.txt', 'w') #Open text file in write mode.
		fb.write(teller) #Save nieuwe teller waarde.
		fb.close() #Sluit text file.
		fb = open('/home/pi/vogelkast_log/vogellog.txt', 'a') #Open text file in append mode.
		fb.write(x) #Save vid naam.
		fb.close() #Sluit text file.
		os.system('date >> /home/pi/vogelkast_log/vogellog.txt') #Save de tijd info in verband met de vids.
		return
	return

#Hoofdlus.
while True:
	maak_opname()
	meet_temp()
	update_var_form()
	#Copieer the camera folder to the apache2 webserver folder.
	os.system("sudo cp -r /home/pi/camera /var/www/html/")
	os.system("sudo cp -r /home/pi/vogelkast_log /var/www/html/")
	sleep(1) #Wacht 1sec.