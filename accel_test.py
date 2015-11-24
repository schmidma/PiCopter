#Accel-Test

from accel import Accel
import time, datetime

ac = Accel()
t1 = datetime.datetime.now()
a = ac.getResult(1)
t2 = datetime.datetime.now()
t = t2-t1
print(a)
print(t)
