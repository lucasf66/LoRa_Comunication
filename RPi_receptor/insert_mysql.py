import pymysql

connection = pymsql.connect(host='localhost',
                            user='root',
                            passwor='1234',
                            database='lora')

columns=["temperatura","umidade","co","hora"]
dados=["30","60","200","21:56"]

insert_coluna=""
insert_dado=""
with connection:
    with connection.cursor() as cursor:
        print('ok')
        for coluna,dado in zip(columns,dados):
            insert_coluna+=str(coluna)+","
            insert_dado+='"'+str(dado)+'",'
        print(insert_coluna)
        print(insert_dado)
        sql='INSERT INTO data('+insert_coluna[:-1]+') VALUE('+insert_dado[:-1]+')'
        cursor.execute(sql)
    connection.commit()
