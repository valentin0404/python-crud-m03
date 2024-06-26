#!/usr/bin/env python3
# from A2P2DB import *
import A3DB as db
import A3DML as dml
import A3DQL as dql
import datetime, os, re

dateformat = "%Y-%m-%d %H:%M:%S.%f"
sep = "-" * 20

####################################################
# 'C' cliente
# 'E' empleat         # LETRAS IDENTIFICATIVAS #
# 'P' proveidor
####################################################
# Constantes que sirven para las 3 tablas
CEP_ID = 0
CEP_NOM = 1

# Constantes que sirves para 'cliente' y 'empleat'
CE_CGM1 = 2
CE_CGM2 = 3

# Constante que sirve únicamente para 'cliente'
C_TLF = 4

# Constante que sirve únicamente para 'empleat'
E_DPT = 4

# Constantes que sirven únicamente para 'proveidor'
P_CIF = 2
P_ADR = 3
P_MAIL = 4
### Fin definición de constantes ###################

opcion = None
final = 4

try:
    db.connectar()
except Exception as e:
    print("ERROR abriendo la conexión de BD")  

#######################################################################################
# Definimos función para validar el número de opción introducida
def rango_opcion(opcion_final):
    while True:
        opcion = validar_opcion()
        if opcion in range(1, opcion_final + 1):
            return opcion
        else:
            print("\nNo has introducido una opción correcta.")
### Fin de función rango_opcion() ####################################################

#######################################################################################
# Definimos función para validar que la opción introducida por el usuario no esté vacía
def validar_opcion():
    while True:
        try:
            return int(input("\nEscoge la opción deseada: "))
        except KeyboardInterrupt:
            print("\nCtrl+C presionado. El proceso ha sido cancelado.")
            db.desconnectar() # Como en este except de teclado se va a salir del programa, se desconecta de la BD préviamente.
            exit()
        except ValueError:
            print("\nNo has introducido una opción válida")
### Fin de función validar_opcion() ###################################################

#######################################################################################
# Definimos función para efectuar búsqueda y para no repetir código
def subopcion2_generico(nombre_campo):
    valor = ""
    while True:
        try:
            valor = input("Introduce el valor: ")
            if len(valor) == 0:
                raise ValueError("\nEl valor no puede estar vacío.")
            elif len(valor) > 40:
                raise ValueError("\nEl valor no puede exceder los 40 caracteres.")
            break
        except ValueError as e:
            print(e)
    return valor
### Fin de función subopcion2_generico() ###################################################

#######################################################################################
# Definimos función para mostrar todos los clientes/empleados/proveedores y para no repetir código ya que se
# repite en las subopciones 1 y 2 y 3 de las 3 opciones generales.
def mostrar_generico():
    if nombre_tabla == "cliente":
        texto = "clientes"
    elif nombre_tabla == "empleat":
        texto = "empleados"
    elif nombre_tabla == "proveidor":
        texto = "proveedores"

    try:
        datos_tabla = dql.consultar_generico(nombre_tabla)
    except Exception as e:
        print(f"ERROR: no se han podido consultar los {texto}.")
        print(e)
    else:
        # Comprobar si 'datos_tabla' tiene información y, si tiene, mostrar los datos
        print("\n" + sep)
        if not datos_tabla:
            print(f"NO existen {texto}")
            print(sep)
        else:
            print(f"Existen los siguientes {texto}:\n")
            id_mapeo = {}  # Diccionario para almacenar el mapping enumerate ID -> real ID

            if nombre_tabla != "proveidor":
                for index, dato in enumerate(datos_tabla, start=1):
                    print(index, "-", dato[CEP_NOM], dato[CE_CGM1], dato[CE_CGM2])
                    id_mapeo[index] = dato[CEP_ID]
            else:
                for index, dato in enumerate(datos_tabla, start=1):
                    print(index, "-", dato[CEP_NOM])
                    id_mapeo[index] = dato[CEP_ID]

            print(sep)
            if opcion != 1:  # En la opción 1 no nos interesa devolver un return
                return datos_tabla, id_mapeo

### Fin de función mostrar_generico() ###################################################

# Definimos función para buscar coincidencias del valor introducido en todos los 
# clientes/empleados/proveedores y para no repetir código ya que se repite en las 
# subopciones 2 de las 3 opciones generales.
def buscar_dato():
    if nombre_tabla == "cliente":
        texto = "cliente"
    elif nombre_tabla == "empleat":
        texto = "empleado"
    elif nombre_tabla == "proveidor":
        texto = "proveedor"

    print(f"Has elegido buscar un {texto}, ¿por qué dato quieres efectuar la búsqueda?\n")

    if nombre_tabla != "proveidor":
        print(f"""
        1. Nombre
        2. Primer apellido
        3. Segundo apellido
        """)

        opcion = rango_opcion(3)

        if opcion == 1:
            nombre_campo = "nom"
            valor = subopcion2_generico(nombre_campo)
        elif opcion == 2:
            nombre_campo = "cognom1"
            valor = subopcion2_generico(nombre_campo)
        elif opcion == 3:
            nombre_campo = "cognom2"
            valor = subopcion2_generico(nombre_campo)
    else:
        print("""
        1. Nombre
        2. CIF
        """)

        opcion = rango_opcion(2)

        if opcion == 1:
            nombre_campo = "empresa"
            valor = subopcion2_generico(nombre_campo)
        elif opcion == 2:
            nombre_campo = "cif"
            valor = subopcion2_generico(nombre_campo)

    try:
        datos_tabla = dql.buscar_generico(nombre_tabla, nombre_campo, valor)
    except Exception as e:
        print(f"ERROR: no se han podido consultar los {texto}s.")
        print(e)
    else:
        # Comprobar si 'datos_tabla' tiene información y, si tiene, mostrar lo/s cliente/s | empleado/s | proveedor/es coincidentes con el valor de la búsqueda.
        print("\n" + sep)
        if not datos_tabla:
            print(f"NO existen {texto}s coincidentes con el valor introducido ({valor}).")
            print(sep)
        else:
            contador = 0
            for index, dato in enumerate(datos_tabla, start=1):
                if nombre_tabla != "proveidor":
                    print(index, "-", dato[CEP_NOM], dato[CE_CGM1], dato[CE_CGM2])
                else:
                    print(index, "-", dato[CEP_NOM])
                contador+=1
            print(f"\nSe han encontrado {contador} coincidencias.")
            print(sep)
### Fin de función buscar_dato() ###################################################

#######################################################################################
# Definimos función para consultar el cliente/empleado/proveedor a la elección de lo introducido por el usuario
# y para no repetir código ya que se repite en la subopcion 3 de las 3 opciones generales.
def consultar_datos():
    if nombre_tabla == "cliente":
        texto = "cliente"
    elif nombre_tabla == "empleat":
        texto = "empleado"
    elif nombre_tabla == "proveidor":
        texto = "proveedor"

    print(f"\nHas elegido consultar datos sobre un {texto}")
    datos_tabla, id_mapeo = mostrar_generico()
    try:
        id_dato = int(input(f"\nQué {texto} quieres elegir?: "))
                
        if id_dato >= 1 and id_dato <= len(datos_tabla):
            encontrado = False  # Variable para indicar si se encuentra el cliente/empleado/proveedor
            id_dato=id_mapeo[id_dato]
            for dato in datos_tabla:
                if dato[CEP_ID] == id_dato:
                    encontrado = True
                    if nombre_tabla != "proveidor": # Condicionales para mostrar dependiendo de que tabla se consulta unos datos u otros.
                        print(f"{sep}\nHas elegido consultar a {dato[CEP_NOM]} {dato[CE_CGM1]} {dato[CE_CGM2]}.")
                        if nombre_tabla == "empleat":
                            print(f"Su teléfono es {dato[C_TLF]}.\n{sep}")
                        else:
                            print(f"Su departamento es {dato[E_DPT]}.\n{sep}")
                    else:
                        print(f"{sep}\nHas elegido consultar a {dato[CEP_NOM]}.")
                        print(f"Su CIF es {dato[P_CIF]}.")
                        print(f"Su dirección es {dato[P_ADR]}.")
                        print(f"Su correo electrónico es {dato[P_MAIL]}.\n{sep}")
                    break  # Salir del bucle una vez encontrado el cliente/empleado/proveedor

            if not encontrado:
                print(f"\nNo se encontró ningún {texto} con el ID proporcionado.")
        else:
            if nombre_tabla != "proveidor":
                print(f"\nEl ID del {texto} no es válido. Debe estar dentro del rango de la lista de {texto}s.")
            else:
                print(f"\nEl ID del {texto} no es válido. Debe estar dentro del rango de la lista de {texto}es.")

    except KeyboardInterrupt:
        print("\nCtrl+C presionado. Saliendo de la opción...")
                
    except ValueError:
        print(f"\nDebes introducir un número entero como ID de {texto}.")
### Fin de función consultar_datos() ###################################################

def añadir_datos():
    if nombre_tabla == "cliente":
        texto = "cliente"
    elif nombre_tabla == "empleat":
        texto = "empleado"
    elif nombre_tabla == "proveidor":
        texto = "proveedor"
    try:
        existe = dql.comprobar_generico(nombre_tabla, nuevo_registro)
        if not existe:
            try:
                dml.añadir_generico(nombre_tabla, nuevo_registro)
                if nombre_tabla != "proveidor":
                    print(f"\nSe ha añadido el nuevo {texto} {nombre}, {apellido1} {apellido2}.")
                else:
                    print(f"\nSe ha añadido el nuevo {texto} {nombre}.")
            except Exception as e:
                if nombre_tabla != "proveidor":
                    print(f"\nERROR: no se ha podido añadir al nuevo {texto} ({nombre}, {apellido1} {apellido2}).")
                else:
                    print(f"\nERROR: no se ha podido añadir al nuevo {texto} ({nombre}).")
                print(e)
        else:
            print(f"\nATENCIÓN: El {texto} que intentas introducir ya existe en la BD.")
    except Exception as e:
        if nombre_tabla != "proveidor":
            print(f"\nERROR: no se ha podido comprobar si existen los datos en la BD del nuevo {texto} ({nombre}, {apellido1} {apellido2}).")
        else:
            print(f"\nERROR: no se ha podido comprobar si existen los datos en la BD del nuevo {texto} ({nombre}).")
        print(e)

#######################################################################################
# Definimos función para formatear cadenas y que cada palabra empiece por mayúscula
# esto se implementa al añadir y modificar, así todo queda uniforme
def formatear_cadena(cadena):
    # Lista de abreviaturas a mantener en mayúsculas
    abreviaturas = {"s.a.", "s.e.", "s.l.", "s.r.l.", "s.r.c.", "s.c."}
    
    # Dividir la cadena en una lista de palabras
    palabras = cadena.split()
    
    # Formatear cada palabra
    palabras_formateadas = []
    for palabra in palabras:
        if palabra.lower() in abreviaturas:
            # Convertir la palabra a mayúsculas si es una abreviatura conocida
            palabras_formateadas.append(palabra.upper())
        else:
            # Capitalizar la palabra normalmente
            palabras_formateadas.append(palabra.capitalize())
    
    # Unir las palabras formateadas de nuevo en una cadena
    cadena_formateada = ' '.join(palabras_formateadas)
    
    return cadena_formateada
### Fin de función formatear_cadena() ##################################################

##############################################################################################
############################ FIN DE DECLARACIÓN DE FUNCIONES #################################
##############################################################################################


while opcion != final:
    #######################################################
        # Menú inicial de opciones
    #######################################################
    print("""
    1. Clientes
    2. Empleados
    3. Proveedores
    4. Salir""")

    opcion = rango_opcion(4)

    if opcion == 1:
        while True:
            #######################################################
            # Menú de opciones dentro de clientes
            #######################################################
            print("""
            1. Consultar todos los clientes existentes
            2. Buscar un cliente
            3. Consultar datos sobre un cliente
            4. Añadir nuevo cliente
            5. Modificar cliente
            6. Borrar cliente
            7. Salir""")

            opcion = rango_opcion(7)
            nombre_tabla = "cliente"

            if opcion == 1:
                print("\nConsultando todos los clientes existentes...")
                mostrar_generico() # Función para mostrar todos los clientes.
            
            elif opcion == 2:
                buscar_dato() # Función para buscar coincidencias del valor en los clientes.
                
            elif opcion == 3:
                consultar_datos() # Función para consultar los datos del cliente seleccionado
                            
            elif opcion == 4:
                opcion = None
                print("\nHas elegido añadir un nuevo cliente")
                nuevo_registro = {} # IMPORTANTE: Si se ejecuta el programa con una versión anterior a Python 3.7 habrán procedimientos dentro de funciones que no funcionarán correctamente, ya que el orden no se garantiza en versiones posteriores. Este programa ha sido probado con la versión 3.11.0rc1, lo que garantiza en correcto funcionamiento.
                
                # Validación de nombre
                nombre = ""
                while True:
                    try:
                        nombre = input("\nIntroduce el nombre del nuevo cliente (máximo 40 caracteres): ")
                        if len(nombre) == 0:
                            raise ValueError("\nEl nombre no puede estar vacío.")
                        elif len(nombre) > 40:
                            raise ValueError("\nEl nombre no puede exceder los 40 caracteres.")
                        break
                    except KeyboardInterrupt:
                        print("\nCtrl+C presionado. El proceso ha sido cancelado.")
                        exit()
                    except ValueError as e:
                        print(e)
                
                # Validación de apellidos
                apellidos = ""
                while True:
                    try:
                        apellidos = input("\nIntroduce los apellidos del nuevo cliente (máximo 40 caracteres): ")
                        if len(apellidos) == 0:
                            raise ValueError("\nLos apellidos no pueden estar vacíos.")
                        elif len(apellidos) > 60:
                            raise ValueError("\nLos apellidos no pueden exceder los 40 caracteres.")
                        break
                    except KeyboardInterrupt:
                        print("\nCtrl+C presionado. El proceso ha sido cancelado.")
                        exit()
                    except ValueError as e:
                        print(e)
                
                # Validación de teléfono
                telefono = ""
                while True:
                    try:
                        telefono = input("\nIntroduce el teléfono del nuevo cliente (9 dígitos): ")
                        if len(telefono) == 0:
                            raise ValueError("\nLos apellidos no pueden estar vacíos.")
                        if not telefono.isdigit():
                            raise ValueError("\nEl teléfono debe contener únicamente dígitos.")
                        if len(telefono) != 9:
                            raise ValueError("\nEl teléfono debe contener 9 dígitos.")
                        break
                    except KeyboardInterrupt:
                        print("\nCtrl+C presionado. El proceso ha sido cancelado.")
                        exit()
                    except ValueError as e:
                        print(e)
                
                nombre = formatear_cadena(nombre)
                apellidos = formatear_cadena(apellidos)
                
                apellidos_separados = apellidos.split()
                apellido1 = apellidos_separados[0]  # Asignar la primera palabra al primer apellido
                
                if len(apellidos_separados) > 1:
                    apellido2 = ' '.join(apellidos_separados[1:])  # Si hay más de una palabra en los apellidos, asignar el resto al segundo apellido
                else:
                    apellido2 = ''

                nuevo_registro["nom"] = nombre
                nuevo_registro["cognom1"] = apellido1
                nuevo_registro["cognom2"] = apellido2
                nuevo_registro["telefon"] = telefono
                
                añadir_datos() # Función para añadir el nuevo cliente.

            elif opcion == 7:
                break  # Salir del bucle interno y volver al menú inicial

    elif opcion == 2:
        while True:
            #######################################################
            # Menú de opciones dentro de empleados
            #######################################################
            print("""
            1. Consultar todos los empleados existentes
            2. Buscar un empleado
            3. Consultar datos sobre un empleado
            4. Añadir nuevo empleado
            5. Modificar empleado
            6. Borrar empleado
            7. Salir""")

            opcion = rango_opcion(7)
            nombre_tabla = "empleat"

            if opcion == 1:
                print("\nConsultando todos los empleados existentes...")
                mostrar_generico() # Función para mostrar todos los empleados 
            elif opcion == 2:
                buscar_dato() # Función para buscar coincidencias del valor en los empleados

            elif opcion == 3:
                consultar_datos() # Función para consultar los datos del empleado seleccionado
            
            elif opcion == 4:
                opcion = None
                print("\nHas elegido añadir un nuevo empleado")
                nuevo_registro = {}
                
                # Validación de nombre
                nombre = ""
                while True:
                    try:
                        nombre = input("\nIntroduce el nombre del nuevo empleado (máximo 40 caracteres): ")
                        if len(nombre) == 0:
                            raise ValueError("\nEl nombre no puede estar vacío.")
                        elif len(nombre) > 40:
                            raise ValueError("\nEl nombre no puede exceder los 40 caracteres.")
                        break
                    except KeyboardInterrupt:
                        print("\nCtrl+C presionado. El proceso ha sido cancelado.")
                        exit()
                    except ValueError as e:
                        print(e)
                
                # Validación de apellidos
                apellidos = ""
                while True:
                    try:
                        apellidos = input("\nIntroduce los apellidos del nuevo empleado (máximo 40 caracteres): ")
                        if len(apellidos) == 0:
                            raise ValueError("\nLos apellidos no pueden estar vacíos.")
                        elif len(apellidos) > 60:
                            raise ValueError("\nLos apellidos no pueden exceder los 40 caracteres.")
                        break
                    except KeyboardInterrupt:
                        print("\nCtrl+C presionado. El proceso ha sido cancelado.")
                        exit()
                    except ValueError as e:
                        print(e)
                
                # Validación de departamento
                departamento = ""
                while True:
                    try:
                        departamento = input("\nIntroduce el departamento del nuevo empleado (máximo 40 caracteres): ")
                        if len(departamento) == 0:
                            raise ValueError("\nEl departamento no puede estar vacío.")
                        elif len(departamento) > 40:
                            raise ValueError("\nEl departamento no puede exceder los 40 caracteres.")
                        break
                    except KeyboardInterrupt:
                        print("\nCtrl+C presionado. El proceso ha sido cancelado.")
                        exit()
                    except ValueError as e:
                        print(e)
                
                nombre = formatear_cadena(nombre)
                apellidos = formatear_cadena(apellidos)
                departamento = formatear_cadena(departamento)            

                apellidos_separados = apellidos.split()
                apellido1 = apellidos_separados[0]  # Asignar la primera palabra al primer apellido
                
                if len(apellidos_separados) > 1:
                    apellido2 = ' '.join(apellidos_separados[1:])  # Si hay más de una palabra en los apellidos, asignar el resto al segundo apellido
                else:
                    apellido2 = ''

                nuevo_registro["nom"] = nombre
                nuevo_registro["cognom1"] = apellido1
                nuevo_registro["cognom2"] = apellido2
                nuevo_registro["departament"] = departamento
                
                añadir_datos() # Función para añadir el nuevo empleado.

            elif opcion == 7:
                break

    elif opcion == 3:
        while True:
            #######################################################
            # Menú de opciones dentro de proveedores
            #######################################################
            print("""
            1. Consultar todos los proveedores existentes
            2. Buscar un proveedor
            3. Consultar datos sobre un proveedor
            4. Añadir nuevo proveedor
            5. Modificar proveedor
            6. Borrar proveedor
            7. Salir""")

            opcion = rango_opcion(7)
            nombre_tabla = "proveidor"

            if opcion == 1:
                print("\nConsultando todos los proveedores existentes...")
                mostrar_generico() # Función para mostrar todos los proveedores
            
            elif opcion == 2:
                buscar_dato() # Función para buscar coincidencias del valor en los proveedores
            
            elif opcion == 3:
                consultar_datos() # Función para consultar los datos del proveedor seleccionado
            
            elif opcion == 4:
                opcion = None
                print("\nHas elegido añadir un nuevo proveedor")
                nuevo_registro = {}
                
                # Validación de nombre
                nombre = ""
                while True:
                    try:
                        nombre = input("\nIntroduce el nombre del nuevo proveedor (máximo 40 caracteres): ")
                        if len(nombre) == 0:
                            raise ValueError("\nEl nombre no puede estar vacío.")
                        elif len(nombre) > 40:
                            raise ValueError("\nEl nombre no puede exceder los 40 caracteres.")
                        break
                    except KeyboardInterrupt:
                        print("\nCtrl+C presionado. El proceso ha sido cancelado.")
                        exit()
                    except ValueError as e:
                        print(e)
                
                # Validación del CIF
                cif = ""
                while True:
                    try:
                        cif = input(f"\nIntroduce el CIF del nuevo proveedor ({nombre}) (A12345678): ")
                        if len(cif) == 0:
                            raise ValueError("\nEl CIF no puede estar vacío.")
                        elif len(cif) != 9:
                            raise ValueError("\nEl CIF debe tener 9 caracteres.")
                        # Se valida el CIF mediante funciones de Python el CIF, pero también se podría usar la librería 're — Regular expression operations', que es más cómoda, al usar expresiones regulares. Se usará más adelante.
                        elif not cif[0].isalpha() or not cif[1:].isdigit():
                            raise ValueError("\nEl CIF debe tener el formato A12345678.")
                        break
                    except KeyboardInterrupt:
                        print("\nCtrl+C presionado. El proceso ha sido cancelado.")
                        exit()
                    except ValueError as e:
                        print(e)
                
                # Validación de dirección
                direccion = ""
                while True:
                    try:
                        direccion = input("\nIntroduce la dirección del nuevo proveedor (máximo 40 caracteres): ")
                        if len(direccion) == 0:
                            raise ValueError("\nLa dirección no puede estar vacío.")
                        elif len(direccion) > 40:
                            raise ValueError("\nLa dirección no puede exceder los 40 caracteres.")
                        break
                    except KeyboardInterrupt:
                        print("\nCtrl+C presionado. El proceso ha sido cancelado.")
                        exit()
                    except ValueError as e:
                        print(e)

                # Validación de dirección
                correo = ""
                while True:
                    try:
                        correo = input("\nIntroduce el correo electrónico del nuevo proveedor (máximo 40 caracteres): ")
                        if len(correo) == 0:
                            raise ValueError("\nEl correo electrónico no puede estar vacío.")
                        elif len(correo) > 40:
                            raise ValueError("\nEl correo electrónico no puede exceder los 40 caracteres.")
                        # Validar el formato del correo electrónico utilizando la librería 're' mencionada anteriormente.
                        if not re.match(r"[^@]+@[^@]+\.[^@]+", correo): # La expresión verifica que haya al menos un caráctes antes y despues de la arroba y tambíen lo mismo antes y después del '.'(punto).
                            raise ValueError("\nEl formato del correo electrónico no es válido.")
                        break
                    except KeyboardInterrupt:
                        print("\nCtrl+C presionado. El proceso ha sido cancelado.")
                        exit()
                    except ValueError as e:
                        print(e)
                
                nombre = formatear_cadena(nombre)

                
                nuevo_registro["empresa"] = nombre
                nuevo_registro["cif"] = cif
                nuevo_registro["adreca"] = direccion
                nuevo_registro["mail"] = correo
                
                añadir_datos() # Función para añadir el nuevo proveedor.

            elif opcion == 7:
                break 
                    
    elif opcion == 4:
        print("Cerrando conexión a la BD...")
        db.desconnectar()