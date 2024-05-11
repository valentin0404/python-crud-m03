#!/usr/bin/env python3
# from A2P2DB import *
import A3DB as db
import A3DML as dml
import A3DQL as dql
import datetime, os

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
        except ValueError:
            print("\nNo has introducido una opción válida")
### Fin de función validar_opcion() ###################################################

#######################################################################################
# Definimos función para mostrar todos los clientes y para no repetir código ya que se
# repite en las subopciones 1 y 2 de ambas opciones generales.
def mostrar_clientes():
    try:
        datos_clientes = dql.consultar_generico(nombre_tabla)
    except Exception as e:
            print("ERROR: no se han podido consultar los clientes.")
            print(e)
    else:
        # Comprobar si 'datos_clientes' tiene información y, si tiene, mostrar los clientes
        print("\n" + sep)
        if not datos_clientes:
            print("NO existen clientes")
            print(sep)
        else:
            print("Existen los siguientes clientes:\n")
            for cliente in datos_clientes:
                print(cliente[CEP_ID]-10, "-", cliente[CEP_NOM], cliente[CE_CGM1], cliente[CE_CGM2])
            print(sep)
            return datos_clientes
### Fin de función mostrar_clientes() ###################################################

#######################################################################################
# Definimos función para mostrar todos los empleados y para no repetir código
def mostrar_empleados():
    try:
        datos_empleados = dql.consultar_generico(nombre_tabla)
    except Exception as e:
        print("ERROR: no se han podido consultar los empleados.")
        print(e)
    else:
        # Comprobar si existen empleados y, si existen, mostrarlos
        print("\n" + sep)
        if not datos_empleados:
            print("NO existen empleados")
            print(sep)
        else:
            print("Existen los siguientes empleados:\n")
            for empleado in datos_empleados:
                print(empleado[CEP_ID], "-", empleado[CEP_NOM], empleado[CE_CGM1], empleado[CE_CGM2])
            print(sep)
            return datos_empleados
### Fin de función mostrar_empleados() ###################################################

#######################################################################################
# Definimos función para mostrar todos los proveedores y para no repetir código
def mostrar_proveedores():
    try:
        datos_proveedores = dql.consultar_generico(nombre_tabla)
    except Exception as e:
        print("ERROR: no se han podido consultar los proveedores.")
        print(e)
    else:
        # Comprobar si existen proveedores y, si existen, mostrarlos
        print("\n" + sep)
        if not datos_proveedores:
            print("NO existen proveedores")
            print(sep)
        else:
            for proveedor in datos_proveedores:
                print(proveedor[CEP_ID], "-", proveedor[CEP_NOM])
            print(sep)
            return datos_proveedores
### Fin de función mostrar_proveedores() ###################################################

#######################################################################################
# Definimos función para formatear cadenas y que cada palabra empiece por mayúscula
# esto se implementa al añadir y modificar, así todo queda uniforme
def formatear_cadena(cadena):
    # Dividir la cadena en una lista de palabras
    palabras = cadena.split()
    
    # Formatear cada palabra: primera letra mayúscula, resto minúsculas
    palabras_formateadas = [palabra.capitalize() for palabra in palabras]
    
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
            mostrar_clientes() # Función para mostrar todos los clientes.
        
        elif opcion == 2:
            print("""
            Has elegido buscar un cliente, ¿por qué dato quieres efectuar la búsqueda?\n
            1. Nombre
            2. Primer apellido
            3. Segundo apellido
            """)

            opcion = rango_opcion(3)
            
            if opcion == 1:
                valor = input("Introduce el valor: ")
                nombre_campo = "nom"
            elif opcion == 2:
                valor = input("Introduce el valor: ")
                nombre_campo = "cognom1"
            elif opcion == 3:
                valor = input("Introduce el valor: ")
                nombre_campo = "cognom2"

            datos_cliente = dql.buscar_generico(nombre_tabla, nombre_campo, valor)

            # Comprobar si 'datos_clientes' tiene información y, si tiene, mostrar lo/s cliente/s coincidentes con el valor de la búsqueda.
            print("\n" + sep)
            if not datos_cliente:
                print(f"NO existen clientes coincidentes con el valor introducido ({valor}).")
                print(sep)
            else:
                contador = 0
                for cliente in datos_cliente:
                    print(cliente[CEP_ID], "-", cliente[CEP_NOM], cliente[CE_CGM1], cliente[CE_CGM2])
                    contador+=1
                print(f"\nSe han encontrado {contador} coincidencias.")
                print(sep)
            
        elif opcion == 3:
            print("\nHas elegido consultar datos sobre un cliente")
            datos_clientes = mostrar_clientes()
            try:
                id_cliente = int(input("\nQué cliente quieres elegir?: "))

                if id_cliente >= 1 and id_cliente <= len(datos_clientes):
                    encontrado = False  # Variable para indicar si se encuentra el cliente
                    id_cliente=id_cliente+10
                    for cliente in datos_clientes:
                        if cliente[CEP_ID] == id_cliente:
                            encontrado = True
                            print(f"{sep}\nHas elegido consultar a {cliente[CEP_NOM]} {cliente[CE_CGM1]} {cliente[CE_CGM2]}.")
                            print(f"Su teléfono es {cliente[C_TLF]}.\n{sep}")
                            break  # Salir del bucle una vez encontrado el cliente

                    if not encontrado:
                        print("\nNo se encontró ningún cliente con el ID proporcionado.")
                else:
                    print("\nEl ID del cliente no es válido. Debe estar dentro del rango de la lista de clientes.")
                    
            except ValueError:
                print("\nDebes introducir un número entero como ID de cliente.")
        
        elif opcion == 4:
            opcion = None # Se le quita el valor únicamente en las opciones '4' para que cuando salgan de estas no finalice el programa.
            print("\nHas elegido consultar añadir un nuevo cliente")
            nuevo_cliente = []
            nombre = input("Introduce el nombre del nuevo cliente: ")
            apellidos = input("Introduce los apellidos del nuevo cliente: ")
            
            try:
                telefono = int(input("Introduce el teléfono del nuevo cliente: "))
            except ValueError:
                print("\nDebes de introducir números únicamente")
            if len(nombre) == 0 or len(apellidos) == 0 or len(str(telefono)) == 0:
                print("\nNo has rellenado todos los campos, debes de rellenar todos.")
            else:
                nombre = formatear_cadena(nombre)
                apellidos = formatear_cadena(apellidos)
                if len(str(telefono)) == 9:
                    # Separar los apellidos
                    apellidos_separados = apellidos.split()
                    apellido1 = apellidos_separados[0]  # Asignar la primera palabra al primer apellido
                    
                    if len(apellidos_separados) > 1:
                        # Si hay más de una palabra en los apellidos, asignar el resto al segundo apellido
                        apellido2 = ' '.join(apellidos_separados[1:])
                    else:
                        apellido2 = ''

                    try:
                        nuevo_cliente.append(apellido1)
                        nuevo_cliente.append(apellido2)
                        nuevo_cliente.append(telefono)
                    except Exception as e:
                        print("\nERROR: Ha ocurrido un error al añadir datos al cliente.")
                        print(e)
                    try:
                        dml.añadir_generico(nombre_tabla, nombre, apellido1, apellido2, telefono)
                        print(f"S\ne ha añadido el nuevo cliente {nombre}, {apellido1} {apellido2}.")
                    except Exception as e:
                        print(f"\nERROR: no se ha podido añadir al nuevo cliente ({nombre}, {apellido1} {apellido2}).")
                        print(e)
                else:
                    print("\nEl teléfono no cumple el formato de 9 dígitos.")

    elif opcion == 2:
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
            mostrar_empleados()        
        elif opcion == 2:
            print("""
            Has elegido buscar un empleado, ¿por qué dato quieres efectuar la búsqueda?\n
            1. Nombre
            2. Primer apellido
            3. Segundo apellido
            """)

            opcion = rango_opcion(3)
            
            if opcion == 1:
                valor = input("Introduce el valor: ")
                nombre_campo = "nom"
            elif opcion == 2:
                valor = input("Introduce el valor: ")
                nombre_campo = "cognom1"
            elif opcion == 3:
                valor = input("Introduce el valor: ")
                nombre_campo = "cognom2"

            datos_empleado = dql.buscar_generico(nombre_tabla, nombre_campo, valor)

            # Comprobar si 'datos_empleados' tiene información y, si tiene, mostrar lo/s empleado/s coincidentes con el valor de la búsqueda.
            print("\n" + sep)
            if not datos_empleado:
                print(f"NO existen empleados coincidentes con el valor introducido ({valor}).")
                print(sep)
            else:
                contador = 0
                for empleado in datos_empleado:
                    print(empleado[CEP_ID], "-", empleado[CEP_NOM], empleado[CE_CGM1], empleado[CE_CGM2])
                    contador+=1
                print(f"\nSe han encontrado {contador} coincidencias.")
                print(sep)

        elif opcion == 3:
            print("\nHas elegido consultar datos sobre un empleado")
            datos_empleados = mostrar_empleados()
            try:
                id_empleado = int(input("\nQué empleado quieres elegir?: "))

                if id_empleado >= 1 and id_empleado <= len(datos_empleados):
                    encontrado = False  # Variable para indicar si se encuentra el empleado
                    for empleado in datos_empleados:
                        if empleado[CEP_ID] == id_empleado:
                            encontrado = True
                            print(f"{sep}\nHas elegido consultar a {empleado[CEP_NOM]} {empleado[CE_CGM1]} {empleado[CE_CGM2]}.")
                            print(f"Su departamento es {empleado[E_DPT]}.\n{sep}")
                            break  # Salir del bucle una vez encontrado el empleado

                    if not encontrado:
                        print("\nNo se encontró ningún empleado con el ID proporcionado.")
                else:
                    print("\nEl ID del empleado no es válido. Debe estar dentro del rango de la lista de empleados.")
                    
            except ValueError:
                print("\nDebes introducir un número entero como ID de empleado.")

    elif opcion == 3:
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
            mostrar_proveedores()
        
        elif opcion == 2:
            print("""
            Has elegido buscar un proveedor, ¿por qué dato quieres efectuar la búsqueda?\n
            1. Nombre
            2. CIF
            """)

            opcion = rango_opcion(2)
            
            if opcion == 1:
                valor = input("Introduce el valor: ")
                nombre_campo = "empresa"
            elif opcion == 2:
                valor = input("Introduce el valor: ")
                nombre_campo = "cif"

            datos_proveedor = dql.buscar_generico(nombre_tabla, nombre_campo, valor)

            # Comprobar si 'datos_proveedor' tiene información y, si tiene, mostrar lo/s proveedor/es coincidentes con el valor de la búsqueda.
            print("\n" + sep)
            if not datos_proveedor:
                print(f"NO existen proveedores coincidentes con el valor introducido ({valor}).")
                print(sep)
            else:
                contador = 0
                for proveedor in datos_proveedor:
                    print(proveedor[CEP_ID], "-", proveedor[CEP_NOM])
                    contador+=1
                print(f"\nSe han encontrado {contador} coincidencias.")
                print(sep)
        
        elif opcion == 3:
            print("\nHas elegido consultar datos sobre un proveedor")
            datos_proveedores = mostrar_proveedores()
            try:
                id_proveedor = int(input("\nQué proveedor quieres elegir?: "))

                if id_proveedor >= 1 and id_proveedor <= len(datos_proveedores):
                    encontrado = False  # Variable para indicar si se encuentra el proveedor
                    for proveedor in datos_proveedores:
                        if proveedor[CEP_ID] == id_proveedor:
                            encontrado = True
                            print(f"{sep}\nHas elegido consultar a {proveedor[CEP_NOM]}.")
                            print(f"Su CIF es {proveedor[P_CIF]}.")
                            print(f"Su dirección es {proveedor[P_ADR]}.")
                            print(f"Su correo electrónico es {proveedor[P_MAIL]}.\n{sep}")
                            break  # Salir del bucle una vez encontrado el proveedor

                    if not encontrado:
                        print("\nNo se encontró ningún proveedor con el ID proporcionado.")
                else:
                    print("\nEl ID del proveedor no es válido. Debe estar dentro del rango de la lista de proveedores.")
                    
            except ValueError:
                print("\nDebes introducir un número entero como ID de proveedor.")

    elif opcion == 4:
        print("Cerrando conexión a la BD...")
        db.desconnectar()