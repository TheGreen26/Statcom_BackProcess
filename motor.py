import socket
import struct
#import rotctld
import subprocess
import os

class Motor():
    def __init__(self,  port):

        self.port = port
        self.isActive=False
        self.satellite=''

        # todo : verify if the mototrs serial number is needed in rotctld to connect

    def init(self, satellite):
        #os.system("")
        self.satellite=satellite
        cmd = ['predict', '-p', self.satellite]
        output = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]

        strCmd = output.decode("utf-8")

        # split to have a single line
        strOut = strCmd.split()
        print(strOut)
        print(self.satellite)
        azimut=strOut[5]
        print('init ' + strOut[5])
        self.moveMotor(0, azimut)


    def moveMotor(self, elevation, azimut):

        # command:
        position = str((abs(int(azimut))))+' '+str(abs(int(elevation)))
        command = 'rotctl -m 603 -r /dev/ttyS0 -C retry=0 P '+position
        ok = os.system(command)
        #check


    def resetPosition(self):

        self.moveMotor(0,0)
        print('position reset')

    def tracking(self):
        # while the passe isnt over follow the satellite

        while (not self.isActive):
            [elevation, azimut]=self.getPositionPredict()
            prevElevation=elevation
            prevAzimut=azimut
            print(elevation)
            while abs(int(elevation)) > 0:
                [elevation, azimut] = self.getPositionPredict()
                self.isActive=True

                if not azimut == prevAzimut or not elevation == prevElevation:
                    self.moveMotor(elevation,azimut)
                    print(elevation +' '+ azimut)
                prevElevation = elevation
                prevAzimut = azimut

        self.isActive=False
        self.resetPosition(0, 0)


        # todo : completer la focntion

    def getPositionPredict(self):

        cmd = ['predict', '-f', self.satellite]
        output = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]

        strCmd = output.decode("utf-8")

        # split to have a single line
        strOut = strCmd.split()

        # split to have two single times

        elevation = strOut[4]
        azimut = strOut[5]
        return [elevation,azimut]