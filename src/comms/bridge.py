# NEEDS DOCSTRINGS
import serial
from src.config import *

class communicator:
    def __init__(self, COM='COM7', baud=9600):
        """Create a new connection to the serial monitor using given COM and baud rate
        
            ### Args:
                COM (str): COM number for connection to arduino serial
                baud (int): baud rate. This should match the serial rate on the arduino

            ### Returns:
                None
        
        """

        self.serialComm = serial.Serial(COM, baud) #Com subject to change right now 
        self.serialComm.timeout = 1

    def issueCommand(self, command, debug=False):
        """Send a message to arduino via the Serial monitor.
        
            ### Args:
                command (str): message to go to Arduino. Be aware that message length matters
                debug (bool): enter debug mode

            ### Returns:
                None
        
        """

        if command is not None:
            self.serialComm.write(command.encode())
            if debug:
                print(f"\nbridge.issueCommand: Sent command: {command}")

    def receiveMessage(self, debug=False):
        """Checks Serial monitor to see if there is an incoming message.
        
            ### Args:
                None

            ### Returns:
                message (str): if message is available, returns decoded message. Else, returns None.
        
        """

        if self.serialComm.in_waiting > 0:
            message = self.serialComm.read(self.serialComm.in_waiting).decode()
        else:
            message = None

        return message
