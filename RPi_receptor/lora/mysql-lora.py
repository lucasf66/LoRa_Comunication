import mysql.connector
import serial
import datetime
ser=serial.Serial("/dev/ttyS0",timeout=2)
connection = mysql.connector.connect(host='localhost',
                            user='root',
                            password='1234',
                            database='lora')
columns=["temperatura","umidade","co","hora"]
dados=["","","",""]
while (True):
    if(ser.inWaiting()>0):
        print("chegou")
        timeAll=datetime.datetime.now()
        time=(str(timeAll.hour)+":"+str(timeAll.minute)+":"+str(timeAll.second))
        print(time)
        getData=str(ser.readline())
        print(getData)
        dados[0]=getData[2:4]
        dados[1]=getData[5:7]
        dados[2]=getData[8:11]
        dados[3]=time
        if(len(getData) <= 12):
            cursor = connection.cursor()
            insert_coluna=""
            insert_dado=""
            for coluna,dado in zip(columns,dados):
                insert_coluna+=str(coluna)+","
                insert_dado+='"'+str(dado)+'",'
            sql='INSERT INTO data ('+insert_coluna[:-1]+') VALUES ('+insert_dado[:-1]+')'
            print(sql)
            cursor.execute(sql)
            connection.commit()
            cursor.close()
        else:
            print("Dado corrompido!!")
