import os
import json
from pathlib import Path

import time, sched

class Reservation:



    def __init__(self, satellite, reservationTime, length, client, data, timeUTC, frequencies):

        self.satellite = satellite
        self.reservationTime = reservationTime
        self.setUpTime = int(timeUTC)  - 2*60
        self.client=client
        self.length=length
        self.data = data
        self.frequencies=frequencies
        self.timeUTC=timeUTC



    ##  this print function allows to simulate calling the motor functions that arent implemented yet:
    def print_function(a='default'):
        print("From print_function", time.time(), a)

    def schedule_pass(self):
        s = sched.scheduler(time.time)
        s.enterabs(self.setUpTime, 1, Reservation.print_function('Call Motor set up time'))
        s.enterabs(self.reservationTime, 1, Reservation.print_function('Call track Satellite time'))
        # TODO: replace print with the real function

