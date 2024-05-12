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

def comprobar_generico(nombre_tabla, campos_valores) -> bool:
    mycursor = db.mydb.cursor()
    
    # Si la tabla es 'proveidor', comprobar primero el CIF
    if nombre_tabla == 'proveidor':
        cif = campos_valores['cif']
        sql = f"SELECT COUNT(*) FROM {nombre_tabla} WHERE cif = %s"
        mycursor.execute(sql, (cif,))
        count = mycursor.fetchone()[0]
        mycursor.close()
        return count > 0

    # Si no es 'proveidor' comprobar todos los campos
    claves_interes = list(campos_valores.keys())
    condiciones = ' AND '.join([f"{campo} = %s" for campo in claves_interes])
    valores = tuple(campos_valores[key] for key in claves_interes)
    sql = f"SELECT COUNT(*) FROM {nombre_tabla} WHERE {condiciones}"
    
    mycursor.execute(sql, valores)
    count = mycursor.fetchone()[0]
    
    mycursor.close()

    return count > 0