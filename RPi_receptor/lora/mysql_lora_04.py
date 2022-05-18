#IMPORTS
import mysql.connector
import serial
import datetime
import sys
import json
import requests


#CONEXAO ALTERÀVEL 
ser=serial.Serial("/dev/ttyS0",timeout=1) #Timeout = Tempo de execução em Segundos
connection = mysql.connector.connect(host='localhost', #HOST BANCO
                        user='root', #ALTERAR DE ACORDO COM O BANCO USER,PASS,DATABASE
                        password='1234', 
                        database='lora')
columns=["temperatura","umidade","co","hora","dia"]

#FUNCAO DE INSERÇÂO NO SQL
def insertMysql():
    try:
        print("Dados recebidos:")
        print("Umidade , Temperatura , CO , Hora , Dia ")
        while (True):
            if(ser.inWaiting()>0):
                timeAll=datetime.datetime.now()
                time=(str(timeAll.hour)+":"+str(timeAll.minute)+":"+str(timeAll.second))
                getData=str(ser.readline())
                one=getData.split("'")
                dados=one[1].split(",")
                dados.append(time)
                dados.append(datetime.date.today())
                msg="|"
                for dado in dados:
                    msg+=(" "+ str(dado)+" |")
                print(msg)
                if(len(getData) <= 12):
                    cursor = connection.cursor()
                    insert_coluna=""
                    insert_dado=""
                    for coluna,dado in zip(columns,dados):
                        insert_coluna+=str(coluna)+","
                        insert_dado+='"'+str(dado)+'",'
                    sql='INSERT INTO data ('+insert_coluna[:-1]+') VALUES ('+insert_dado[:-1]+')'
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
        if((argument=='-csv') or (argument=='-upload')):
            cont=0
            global nameCsv
            for x in sys.argv:
                try:
                    if((argument=='-csv') or (argument=='-upload')): #CONFERE SE EXISTE CSV E UPLOAD
                        nameCsv=sys.argv[(cont)]
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
    file.write("Umidade,Temperatura,CO,Horario,Dia\n")
    file.close()
    for(temperatura,umidade,co,hora,dia) in received:
        data = (f"{temperatura},{umidade},{co},{hora},{dia}")
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
    for(temperatura,umidade,co,hora,dia) in received:
        data = (f"{temperatura},{umidade},{co},{hora},{dia}")
        print(data)
    received.close

#UPANDO ARQUIVOS PRO GOOGLE DRIVE
def uploadToGoogleDrive(nameCsv):
    headers = {"Authorization": "Bearer "+"ya29.a0ARrdaM_eG-YRq5_9hghYnyleVROUkCra2tNHaPJ3ExwDk21bJ8B7epHOitU-8i9dQvg2tJaSDeGE7ejD941ASOxU6xQH_XH59vkBl0WTKSYEMJbS-ZCN2UiH1mImCidoRMSmLd81NAA3w78cxVvm6qX4Y3FA"}
    #AUTORIZAÇÂO https://developers.google.com/oauthplayground/ >GOOGLE DRIVE API > ACESS TOKEN
    para = {
        "name":nameCsv,
        "parents":["1JTyh2bONy9JUnaRagstYP03PSnnhMUSQ"] #LINK PASTA GOOGLE DRIVE 
        #EXEMPLO : https://drive.google.com/drive/folders/113osm7ZaQrjJTnO0HKVDW8JnZ5z8hcc9
    }
    files = {
        'data': ('metadata', json.dumps(para), 'application/json; charset=UTF-8'),
        'file': open("./"+nameCsv, "rb") #SELECIONAR O ARQUIVO
    }
    r = requests.post(
        "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart",
        headers=headers,
        files=files)
    print("Upload concluido com sucesso!")

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
    elif(checkArgv('-upload')):
        uploadToGoogleDrive(nameCsv)
    else:
        print("Sem argumentos!")
