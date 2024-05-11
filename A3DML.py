import mysql.connector
import A3DB as db

def añadir_generico(nombre_tabla, nombre, apellido1, apellido2, telefono):
    mycursor = db.mydb.cursor()
    sql = "INSERT INTO {} (nom, cognom1, cognom2, telefon) VALUES (%s, %s, %s, %s)".format(nombre_tabla)
    val = (nombre, apellido1, apellido2, telefono)
    mycursor.execute(sql, val)
    db.mydb.commit()
    mycursor.close()