

import time

class Reservation:



    def __init__(self, satellite, reservationTime, length, client, data, timeUTC, frequencies):

        self.satellite = satellite
        self.reservationTime = reservationTime
        self.setUpTime =  int(timeUTC)  - 2*60
        self.client=client
        self.length=length
        self.data = data
        self.frequencies=frequencies
        self.timeUTC=int(timeUTC)



    ##  this print function allows to simulate calling the motor functions that arent implemented yet:
    def print_function(a='default'):
        print("From print_function", time.time(), a)



