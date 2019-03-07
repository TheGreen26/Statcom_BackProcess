
import Reservation
import motor
import subprocess
import json
import time
import threading
import sched
import os
import limesdr_receive_WB
import wx



class ReservationChecker(threading.Thread):
    '''
      ---------------------------------------------------------
      description: initialisation of the checker

      create by: Simon Belanger
      Last mmodified by : Simon Belanger @2019-01-24
      ---------------------------------------------------------
      '''
    def __init__(self):

        super(ReservationChecker, self).__init__()
        self.reservationList=[]
        self.events=[]
        self.reservationNumber=0
        self.stop_event = threading.Event()
        self.calendar = sched.scheduler(time.time, delayfunc=self.stop_event.wait)
        self.checkerThread=threading.Thread(target=self.calendar.run)
        self.modificationDate=0
        super(ReservationChecker, self).__init__()
        self.yaesus = motor.Motor(4533)
        self.isCommunicating = False
        self.pendingReservation=0

        threading.Thread.__init__(self)


    '''
      ---------------------------------------------------------
      description: start the thread

      create by: Simon Belanger
      Last mmodified by : Simon Belanger @2019-01-24
      ---------------------------------------------------------
      '''
    def run(self):

        self.update()


        while (True):
            if (self.fileChanged()):
                time.sleep(0.1)

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

        reservationDB = open("/home/statcom/PycharmProjects/statcom-v1/reservationDB.json")

        resJson = json.load(reservationDB)
        print(len(resJson))
        i=0
        if not len(resJson)==0:
            for element in resJson:
                temp=Reservation.Reservation(satellite=element['satellite'],reservationTime=element['reservationTime'],
                                             client=element['client'], length=element['length'], data=element['command file'],
                                             frequencies=[element['Uplink'],element['Downlink']],timeUTC=time.time()+6)#todo changer
                self.reservationList.append(temp)
                self.reservationNumber=self.reservationNumber+1

                i=i+1
            reservationDB.close()
            self.schedule_pass()
            stat = os.stat("/home/statcom/PycharmProjects/statcom-v1/reservationDB.json")
            self.modificationDate = stat.st_mtime
            self.calendar.run()

    '''
       ---------------------------------------------------------
       description: schedule the passes by creating events that will pop at a proper time

       create by: Simon Belanger
       Last mmodified by : Simon Belanger @2019-01-24
       ---------------------------------------------------------
       '''
    def schedule_pass(self):

        for res in self.reservationList:

            self.events.append(self.calendar.enterabs(res.setUpTime, 1, self.yaesus.init, (res.satellite,)))
            self.events.append(self.calendar.enterabs(res.timeUTC, 1, self.communicate, (res,)))
        # TODO: replace print with the real function

    '''
          ---------------------------------------------------------
          description: setting up the antenna to the start of the passe

          create by: Simon Belanger
          Last mmodified by : Simon Belanger @2019-03-04
          ---------------------------------------------------------
          '''

    def communicate(self, reservation):

        self.pendingReservation=reservation

        self.isCommunicating=True
        self.yaesus.tracking()




    '''
           ---------------------------------------------------------
           description: verify is the file has changed

           create by: Simon Belanger
           Last mmodified by : Simon Belanger @2019-01-24
           ---------------------------------------------------------
           '''
    def fileChanged(self):

        stat=os.stat("/home/statcom/PycharmProjects/statcom-v1/reservationDB.json")
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
        self.stop_event.set()

def main( top_block_cls=limesdr_receive_WB.limesdr_receive_WB):
    checker= ReservationChecker()
    checker.start() #starts the checker thread
    stat = os.stat("/home/statcom/PycharmProjects/statcom-v1/reservationDB.json")
    #SDR_handler=top_block_cls(1e09,'',0)
    #SDR_handler= limesdr_receive_WB.limesdr_receive_WB(1e09,'',0)
    checker.modificationDate = stat.st_mtime
    time.sleep(2)
    sdr=doppler_handler()


    while (True):

        if checker.fileChanged():
            checker.stopCalendar()

        if checker.isCommunicating:

            sdr.currentReservation=checker.pendingReservation
            sdr.start()
            sdr.join()
            #cmd = ['python', 'limesdr_receive_WB.py', checker.pendingReservation.satellite, str(checker.pendingReservation.frequencies[1]), str(checker.pendingReservation.length),'&']
            #output = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()
        #    SDR_handler.sat_name=checker.pendingReservation.satellite
         #   SDR_handler.freq_RX=checker.pendingReservation.frequencies[1]
          #  SDR_handler.duration=checker.pendingReservation.length*1000
            #SDR_handler.Start()
            #SDR_handler.Wait()

class doppler_handler(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.currentReservation=Reservation.Reservation('', '',0,'','',0,[])
    def run(self):
        cmd = ['python', 'limesdr_receive_WB.py', self.currentReservation.satellite,
               str(self.currentReservation.frequencies[1]), str(self.currentReservation.length), ' &']
        output = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()


main()