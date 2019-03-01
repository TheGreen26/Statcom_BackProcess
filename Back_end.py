from pathlib import Path
import Reservation
import json

class ReservationChecker:
    def __init__(self):

        self.reservationList=[]
        self.reservationNumber=0

    '''
   ---------------------------------------------------------
   description: update the list of reservation

   create by: Simon Belanger
   Last mmodified by : Simon Belanger @2019-01-24
   ---------------------------------------------------------
   '''

    def update(self):
        file = Path("./reservationDB.json")

        reservationDB = open("/home/simon/PycharmProjects/statcom-v1/statcom-v1/reservationDB.json")

        resJson = json.load(reservationDB)

        for element in resJson:
            temp=Reservation.Reservation(satellite=element['satellite'],reservationTime=element['reservationTime'],
                                         client=element['client'], length=element['length'], data=element['command file'],
                                         frequencies=[element['Uplink'],element['Downlink']],timeUTC=element['Time UTC'] )
            self.reservationList.append(temp)
            self.reservationNumber=self.reservationNumber+1


def main():
    checker= ReservationChecker()
    checker.update()
    print(checker.reservationNumber)



main()