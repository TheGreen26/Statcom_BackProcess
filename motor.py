import socket
import struct
import rotctld
import os

class Motor():
    def __init__(self, azimuth, elevation, port):
        self.azimuth = azimuth
        self.elevation = elevation
        self.port = port




        # todo : verify if the mototrs serial number is needed in rotctld to connect
def init():
    os.system("")

def prepareMotor(self):
    # command:
    position = str(self.azimuth)+' '+str(self.elevation)
    command = 'echo "+P '+ position + '" | nc -w 1 localhost '+str(self.port)
    ok = os.system(command)
    #check
    msg = 'set_pos: ' + position
    if ok == msg is False:
        print("PrepareMotor did not return the expected result")

def resetPosition(self):
    command = 'echo "+P 0 0" | nc -w 1 localhost ' + str(self.port)
    ok = os.system(command)
    # check
    msg = 'set_pos: 0 0 '
    if ok == msg is False:
        print("ResetPosition did not return the expected result")

def tracking():
    # todo : completer la focntion

