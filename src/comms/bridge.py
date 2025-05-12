# NEEDS DOCSTRINGS
import serial
import time
from src.config import *

class communicator:
    def __init__(self, COM='COM7', baud=115200, debug=False):
        """Create a new connection to the serial monitor using given COM and baud rate
        
            ### Args:
                COM (str): COM number for connection to arduino serial
                baud (int): baud rate. This should match the serial rate on the arduino
                debug (bool): Enter debug mode

            ### Returns:
                None
        
        """

        self.serialComm = serial.Serial(COM, baud) #Com subject to change right now 
        self.serialComm.timeout = 1
        if debug:
            print("\ncommunicator.init: succesful initialization of communicator object")

    def issueCoordinate(self, info, debug=False):
        """Send a coordinate message to arduino via the Serial monitor.
        
            ### Args:
                info (list): info package of deltas, sx, sy, and err
                debug (bool): Enter debug mode
        
            ### Returns:
                None

        """

        if len(info) != 4:
            print("\nbridge.issueCoordinate: VALUE ERROR: coordinate package to send to arduino missing cruicial information.")
            print(f"Package length: {len(info)}\nPackage content: {info}")
            return
        else:
            # Need to put in format easy for arduino to deconstruct
            command = f"GOTO dx{info[0]} dy{info[1]} sx{info[2]} sy{info[3]} er{info[4]}\n"
    
        # Send command to Arduino
        self.serialComm.write(command.encode())  # Send the command
        if debug:
            print(f"\nbridge.issueCoordinate: Sent command: {command}")

    def issueCommand(self, command, debug=False):
        """Send a message to arduino via the Serial monitor.
        
            ### Args:
                command (str): message to go to Arduino. Be aware that message length matters
                debug (bool): Enter debug mode

            ### Returns:
                None
        
        """

        if command is not None:
            commandEncoded = f"{command}\n"
            self.serialComm.write(commandEncoded.encode())
            if debug:
                print(f"\nbridge.issueCommand: Sent command: {command}")

    def receiveMessage(self, debug=False):
        """Checks Serial monitor to see if there is an incoming message in the monitor.
        
            ### Args:
                None

            ### Returns:
                message (str): if message is available, returns decoded message. Else, returns None.
        
        """

        if self.serialComm.in_waiting > 0:
            if debug:
                print("bridge.receiveMessage: message found")
            message = self.serialComm.read(self.serialComm.in_waiting).decode()
        else:
            message = None

        return message
    
    def waitForMessage(self, debug=False):
        """Waits until a message from Arduino is sent in the Serial monitor
        
            ### Args:
                debug (bool): Enter debug mode
            
            ### Returns:
                message (str): if message is available, returns decoded message.
        
        """

        while self.serialComm.in_waiting == 0:
            time.sleep(0.01)  # wait 10ms
            message = self.receiveMessage()
        return message
