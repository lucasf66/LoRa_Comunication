#IMPORTS
import mysql.connector
import serial
import datetime
import sys


#CONEXAO ALTERÀVEL 
ser=serial.Serial("/dev/ttyS0",timeout=2) #Timeout = Tempo de execução em Segundos
connection = mysql.connector.connect(host='localhost', #HOST BANCO
                        user='root', #ALTERAR DE ACORDO COM O BANCO USER,PASS,DATABASE
                        password='1234', 
                        database='lora')
columns=["temperatura","umidade","co","hora"]

#FUNCAO DE INSERÇÂO NO SQL
def insertMysql():
    dados=["","","",""]
    try:
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
    except KeyboardInterrupt:
        print("PROCESSO INTERROMPIDO")


#CHECA SE EXISTE O ARGUMENTO NA LINHA DE COMANDO
def checkArgv(argument):
    if (any(element in argument for element in sys.argv)):
        signal=True
    else:
        signal=False
    return signal


#FUNCAO PARA PEGAR DO SQL E CRIAR UM CSV
def createCsv():
    print("CSV")


#MAIN()
if __name__ == '__main__':
    if(checkArgv('-e')):
        print("EM MODO DE EXECUÇÂO")
        insertMysql()
    elif(checkArgv('-csv')):
        print("CSV")
    else:
        print("Sem argumentos!")
     
