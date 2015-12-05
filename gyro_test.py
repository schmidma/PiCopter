import time
from gyro import Gyro

g = Gyro()

g.calibrateGyro()

while True:
    print(g.getGyroValues())
    time.sleep(0.1)