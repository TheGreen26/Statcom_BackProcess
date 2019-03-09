

import time
import json

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

    '''
      ---------------------------------------------------------
      description: erases the reservation in the database

      create by: Simon Belanger
      Last mmodified by : Simon Belanger @2019-01-24
      ---------------------------------------------------------
      '''
    def eraseInDB(self):


        reservationDBIn = open("/home/statcom/Documents/statcom-v1/reservationDB.json",'r')
        resJson = json.load(reservationDBIn)
        reservationDBIn.close()
        reservationDBOut = open("/home/statcom/Documents/statcom-v1/reservationDB.json", 'w')

        for res in resJson:
            if res['Time UTC'] == self.timeUTC:
                resJson.remove(res)
        jsonDB = json.dumps(resJson)
        reservationDBOut.write(jsonDB)
        reservationDBOut.close()










