import serial

serialComm = serial.Serial('COM7', 9600) #Com subject to change right now 
serialComm.timeout = 1

def response(moved, direction, speed):
    #Reducing bytes
    if moved == True:
        moved = "T"
    else:
        moved = "F"

    serialComm.write(str(moved).encode())
    serialComm.write(str(direction).encode())

    if serialComm.in_waiting > 0:
        print(serialComm.read(serialComm.in_waiting).decode())
    