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
        if(argument=='-csv'):
            cont=0
            global nameCsv
            for x in sys.argv:
                try:
                    if(x=='-csv'):
                        nameCsv=sys.argv[(cont+1)]
                    cont+=1
                except:
                    nameCsv="data"
    else:
        signal=False
    return signal


#FUNCAO PARA PEGAR DO SQL E CRIAR UM CSV
def createCsv(nameCsv):
    received =  connection.cursor()
    querry = ("SELECT * FROM data")
    received.execute(querry)
    filename=str(nameCsv)+".csv"
    file = open(filename,"a")
    file.write("Umidade(%),Temperatura(C),CO(ppm),Horário\n")
    file.close()
    for(temperatura,umidade,co,hora) in received:
        data = (f"{temperatura},{umidade},{co},{hora}")
        file = open(filename,"a")
        file.write(data+"\n")
        file.close()
    received.close
    print("Arquivo "+nameCsv+".csv criado com sucesso!!")

#ZERAR TODOS OS DADOS DA DATABASE
def resetDatabase():
    try:
        received = connection.cursor()
        querry = ("DELETE FROM data WHERE temperatura !=0")
        received.execute(querry)
        connection.commit() #SEMPRE UTILIZAR COMMIT PRA ATUALIZAR O COMANDO 
        received.close()
        print("DATABASE RESETADO")
    except:
        print("Ocorreu algum erro")

def seeAlldatas():
    received =  connection.cursor()
    querry = ("SELECT * FROM data")
    received.execute(querry)
    for(temperatura,umidade,co,hora) in received:
        data = (f"{temperatura},{umidade},{co},{hora}")
        print(data)
    received.close
    



#MAIN()
if __name__ == '__main__':
    if(checkArgv('-e')):
        print("EM MODO DE EXECUÇÂO")
        insertMysql()
    elif(checkArgv('-csv')):
        print("CRIANDO CSV")
        createCsv(nameCsv)
    elif(checkArgv('-reset')):
        resetDatabase()
    elif(checkArgv('-view')):
        seeAlldatas()
    else:
        print("Sem argumentos!")
