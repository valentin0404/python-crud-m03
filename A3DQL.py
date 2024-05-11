import mysql.connector
import A3DB as db

def consultar_generico(nombre_tabla):
    datos = []
    mycursor = db.mydb.cursor()
    sql = "SELECT * FROM {}".format(nombre_tabla)  # Hago uso de un formateador de cadena por qué me genera errores sin ello, o no encuentra la tabla o me da error de sintaxis SQL. 
    mycursor.execute(sql)
    datos = mycursor.fetchall()
    mycursor.close()
    return datos

def buscar_generico(nombre_tabla, nombre_campo, valor):
    datos = []
    mycursor = db.mydb.cursor()
    sql = "SELECT * FROM {} WHERE {} LIKE '%{}%'".format(nombre_tabla, nombre_campo, valor)
    mycursor.execute(sql)
    datos = mycursor.fetchall()
    mycursor.close()
    return datos