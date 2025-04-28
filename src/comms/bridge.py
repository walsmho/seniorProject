import serial
from src.config import *

class communicator:
    def __init__(self):
        self.serialComm = serial.Serial('COM7', 9600) #Com subject to change right now 
        self.serialComm.timeout = 1

    def issueCommand(self, command, debug=False):
        if command is not None:
            self.serialComm.write(command.encode())
            if debug:
                print(f"\nbridge.issueCommand: Sent command: {command}")

    def receiveMessage(self, debug=False):
        if self.serialComm.in_waiting > 0:
            message = self.serialComm.read(self.serialComm.in_waiting).decode()
        else:
            message = None

        return message
