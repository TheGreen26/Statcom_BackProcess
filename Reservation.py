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

    def saveInDB(self):

        # check if file exist
        file = Path("./reservationDB.json")
        if file.exists():
            previousJson = open("./reservationDB.json")
        else:
            previousJson = open("./reservationDB.json", "w")
        if os.stat("./reservationDB.json").st_size == 0:
            reservationList = []
            print('empty json')
        else:
            reservationList = json.load(previousJson)
        print(type(reservationList))


        dict = {
            'satellite': self.satellite,
            'reservationTime': self.reservationTime,
            'setUpTime': self.setUpTime,
            'client': self.client,
            'length': self.length,
            'command file': self.data,
            'Uplink': self.frequencies[0],
            'Downlink': self.frequencies[1],
            'Time UTC' :self.timeUTC
          # TODO : modify userWindow.py
        }

        reservationList.append(dict)

        #sorting the database by soonest reservation time
        reservationList = sorted(reservationList, key=lambda k: k['reservationTime'])

        jsonDB = json.dumps(reservationList)

        with open('reservationDB.json', 'w') as resDB:
            resDB.write(jsonDB)

            jsonDB.sort(key = lambda x: x['setUpTime'], reverse = True)
            for i in jsonDB['reservation']:
                next = i+1
                prev = i -1
                if prev['reservationTime']+prev['length']+1 > i['setUpTime']:
                    #todo: delete reservation json
                    print('this reservation is impossible')
                elif i['reservationTime']+i['length']+1 > next['setUpTime']:
                    # todo: delete reservation json
                    print('this reservation is impossible')
                else:
                    print('the reservations are okay')

