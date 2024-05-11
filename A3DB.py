import mysql.connector

def connectar():
    global mydb
    print("Abriendo conexión a la BD...")
    mydb = mysql.connector.connect(
        host="shared.daw.cat",
        user="1dd05",
        password="1ASIXdaw*05",
        port="3306",
        database="1dd05_gestor_negocis"
    )

def desconnectar():
    mydb.close()