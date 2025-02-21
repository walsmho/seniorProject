import serial
import time

serialComm = serial.Serial('COM7', 9600)
serialComm.timeout = 1

while True:
    i = input("Turn ON or OFF:").strip()
    if i == 'q':
        break
    serialComm.write(i.encode())
    print(serialComm.readline().decode('ascii'))
    time.sleep(.5)

serialComm.close()
