from pathlib import Path
import Reservation
import json
import time
import threading
import sched
import os



class ReservationChecker(threading.Thread):
    '''
      ---------------------------------------------------------
      description: initialisation of the checker

      create by: Simon Belanger
      Last mmodified by : Simon Belanger @2019-01-24
      ---------------------------------------------------------
      '''
    def __init__(self):

        self.reservationList=[]
        self.events=[]
        self.reservationNumber=0
        self.calendar = sched.scheduler(time.time)
        self.checkerThread=threading.Thread(target=self.calendar.run)
        self.modificationDate=0
        threading.Thread.__init__(self)

    '''
      ---------------------------------------------------------
      description: start the thread

      create by: Simon Belanger
      Last mmodified by : Simon Belanger @2019-01-24
      ---------------------------------------------------------
      '''
    def run(self):

        while (True):

            if self.fileChanged(): #verify if there was a modification in the database
                time.sleep(1)
                stat = os.stat("/home/simon/PycharmProjects/statcom-v1/statcom-v1/reservationDB.json")
                self.modificationDate = stat.st_mtime
                self.update()
                print('checker updated')





    '''
   ---------------------------------------------------------
   description: update the list of reservation

   create by: Simon Belanger
   Last mmodified by : Simon Belanger @2019-01-24
   ---------------------------------------------------------
   '''

    def update(self):
        ## cancel the previous calendar

        reservationDB = open("/home/simon/PycharmProjects/statcom-v1/statcom-v1/reservationDB.json")

        resJson = json.load(reservationDB)
        print(len(resJson))
        i=0
        for element in resJson:
            temp=Reservation.Reservation(satellite=element['satellite'],reservationTime=element['reservationTime'],
                                         client=element['client'], length=element['length'], data=element['command file'],
                                         frequencies=[element['Uplink'],element['Downlink']],timeUTC=element['Time UTC'])
            self.reservationList.append(temp)
            self.reservationNumber=self.reservationNumber+1
            i=i+1
        reservationDB.close()
        self.schedule_pass()
        self.calendar.run(blocking=False)

    '''
       ---------------------------------------------------------
       description: schedule the passes by creating events that will pop at a proper time

       create by: Simon Belanger
       Last mmodified by : Simon Belanger @2019-01-24
       ---------------------------------------------------------
       '''
    def schedule_pass(self):

        for res in self.reservationList:

            self.events.append(self.calendar.enterabs(res.setUpTime, 1,self.print_event,('prepare the motor',)))
            self.events.append(self.calendar.enterabs(res.timeUTC, 1, self.print_event,('start the engine',)))
        # TODO: replace print with the real function

    def print_event(self, callType):
        print(str(callType)+str(time.time()))

    '''
           ---------------------------------------------------------
           description: verify is the file has changed

           create by: Simon Belanger
           Last mmodified by : Simon Belanger @2019-01-24
           ---------------------------------------------------------
           '''
    def fileChanged(self):

        stat=os.stat("/home/simon/PycharmProjects/statcom-v1/statcom-v1/reservationDB.json")
        if(self.modificationDate == stat.st_mtime):

            return False
        else:

            print(self.modificationDate)
            return True

    '''
   ---------------------------------------------------------
   description: empty the calendar queue before making a new one 

   create by: Simon Belanger
   Last mmodified by : Simon Belanger @2019-01-24
   ---------------------------------------------------------
   '''

    def stopCalendar(self):
        print(len(self.events))

        for res in self.events:
            try:
                self.calendar.cancel(res)

                print("clearing events")
            except:
                print("already happended")
        self.reservationNumber=0
        self.reservationList.clear()
        self.events.clear()

def main():
    checker= ReservationChecker()
    checker.start() #starts the checker thread
    time.sleep(2)
    while (True):
        time.sleep(2)
        print(time.time())
        print(' number '+str(checker.reservationNumber)+'\n')
        if checker.fileChanged():
            checker.stopCalendar()





main()