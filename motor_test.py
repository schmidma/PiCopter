from motor import Motor

m1 = Motor(15)
m2 = Motor(27)
m3 = Motor(10)
m4 = Motor(7)

motors = [m1,m2,m3,m4]

c = raw_input("Start motors")

for i in motors:
	i.start()
loop = 1

while loop:
	get = raw_input("Type power: ")
	if get == "off":
		for i in motors:
			i.stop()
		loop = 0
		break
	else:
		for i in motors:
			i.setW(int(get))
			print(get)
	
