import serial
import datetime
from time import sleep
ser=serial.Serial("/dev/ttyS0",timeout=2)
filename="data.csv"
file = open(filename,"a")
file.write("Horario,Umidade(%),Temperatura(C),CO(ppm)\n")
file.close()
while (True):
    if(ser.inWaiting()>0):
        print("chegou")
        timeAll=datetime.datetime.now()
        time=(str(timeAll.hour)+":"+str(timeAll.minute)+":"+str(timeAll.second))
        getData=str(ser.readline())
        getData=ser.readline()
        data=getData
        print(data)
        file = open(filename,"a")
        file.write(time+","+data+"\n")
        file.close()
        ser.flushInput()

