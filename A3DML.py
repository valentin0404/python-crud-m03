import mysql.connector
import A3DB as db

def añadir_generico(nombre_tabla, campos_valores):
    mycursor = db.mydb.cursor()
    
    # Generar la cadena de campos y valores dinámicamente
    campos = ', '.join(campos_valores.keys()) # Cuidado con la versión de Python, comentario detallado en el archivo del programa principal.
    valores = ', '.join(['%s'] * len(campos_valores))  # Generar '%s' por cada campo
    sql = f"INSERT INTO {nombre_tabla} ({campos}) VALUES ({valores})"
    
    # Obtener los valores de los campos del diccionario
    valores = tuple(campos_valores.values())  # Cuidado con la versión de Python, comentario detallado en el archivo del programa principal.
    
    mycursor.execute(sql, valores)
    db.mydb.commit()
    mycursor.close()