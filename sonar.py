##########################################
##	sonar.py - Sonar-Klasse	        ##
##########################################

#Bibliotheken einbinden
import RPi.GPIO as GPIO
import time

class Sonar (object):
	def __init__(self):
		#GPIO Modus (BOARD / BCM)
                GPIO.setmode(GPIO.BCM)
 
                #GPIO Pins zuweisen
                GPIO_TRIGGER = 18
                GPIO_ECHO = 24
                 
                #Richtung der GPIO-Pins festlegen (IN / OUT)
                GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
                GPIO.setup(GPIO_ECHO, GPIO.IN)

 

         
        def distance():
                #Trigger wird getriggert
                GPIO.output(GPIO_TRIGGER, True)
             
                #Trigger wird nach 0.01ms deaktiviert
                time.sleep(0.00001)
                GPIO.output(GPIO_TRIGGER, False)
                 
                StartTime = time.time()
                StopTime = time.time()
                 
                # speichere Startzeit des Signals
                while GPIO.input(GPIO_ECHO) == 0:
                    StartTime = time.time()
                 
                # speichere Ankunftszeit des Echos
                while GPIO.input(GPIO_ECHO) == 1:
                    StopTime = time.time()
                 
                # Zeit Differenz zwischen Start und Ankunft
                TimeElapsed = StopTime - StartTime
                
                # mit der Schallgeschwindigkeit (34300 cm/s) multiplizieren
                # und durch 2 teilen, da hin und zurueck
                distance = (TimeElapsed * 34300) / 2
                
                return distance
                 

       
