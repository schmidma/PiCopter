# coding: utf-8

##########################################
# accel.py - Accelerometer-Klasse
##########################################

#IMPORT
#importiere smbus für Zugriff auf die i2c-Ports
import smbus

#Definiere die Klasse "Accel" zum abfragen der Rotationswerte um die X-,Y-,Z-Achsen
class Accel ():
	
	#Klasse: Accel
	#Parameter:
	# - i2c_bus - Busadresse; Standard: 1
	# - i2c_address - Adresse des i2c_chips in HEX
	
	#Konstruktor-Methode
	def __init__(self, i2c_bus = 1, i2c_address = 0x53):
		
		#Initiiere den i2c-Bus
		self.__i2c_bus = smbus.SMBus(i2c_bus)
		
		#Setze die i2c-Adresse des Chips als Klassenvariable
		self.i2c_address = i2c_address
		
		#Setze das POWER_CTL auf 0x08 (00001000) - Measurement mode
		self.__i2c_bus.write_byte_data(self.i2c_address, 0x2D, 0x08)
		
		self.calibrateValues = [0,0,0]

	#Definiere read-Methode zum Auslesen der Achsen-Werte
	def read(self):
		#Liest die die nächsten 6 Bytes (2 pro Achse - High-Byte+Low-Byte) und liefert eine Liste
		self.bytes = self.__i2c_bus.read_i2c_block_data(self.i2c_address, 0x32, 6)
	
	#Definiere getResult-Methode zum Auswerten der Roh-Werte
	#Parameter: refresh - wenn True: Liest die Achsenwerte neu
	def getResult(self, refresh=0):
		if refresh:
			self.read()
		
		#Deklariere das Ergebnis-Liste
		res = []
		
		#for-Schleife mit den i-Werten 0,2,4
		for i in range(0, 6, 2):
			#Kombiniert die High- und Low-Bytes - Das High-Byte wird um 8bit verschoben und das Low-Byte angehängt
			g = self.bytes[i] | (self.bytes[i+1] << 8)
			#Verarbeitung des Zweierkomplements
			if g > 32767:
				g -= 65536
			#Anhängen des Wertes an die Ergebnis-List
			res.append(g)
			
		#Rückgabe der Ergebnis-Liste
		return res

	#Defniere getX-Methode zum Auslesen des X-Wertes
	#Parameter: refresh - wenn True: List die Achsenwerte neu
	def getX(self, refresh):
		X = self.getResult(refresh)[0]
		return X
	
	#Defniere getY-Methode zum Auslesen des Y-Wertes
	#Parameter: refresh - wenn True: List die Achsenwerte neu
	def getY(self, refresh):
		Y = self.getResult(refresh)[1]
		return Y
	
	#Defniere getZ-Methode zum Auslesen des Z-Wertes
	#Parameter: refresh - wenn True: List die Achsenwerte neu	
	def getZ(self, refresh):
		Y = self.getResult(refresh)[2]
		return Y
	
	def calibrateAccel(self):
		result = self.getResult(1)
		self.calibrateValues = [-result[0], -result[1], -result[2]]
		
	def getCalibrateValues(self):
		return self.calibrateValues