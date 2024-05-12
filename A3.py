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
                    nombre_campo = "nom"
                    valor = subopcion2_generico(nombre_campo)
                elif opcion == 2:
                    nombre_campo = "cognom1"
                    valor = subopcion2_generico(nombre_campo)
                elif opcion == 3:
                    nombre_campo = "cognom2"
                    valor = subopcion2_generico(nombre_campo)

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
                    
                    if len(str(id_cliente)) == 0:
                        raise ValueError("\nEl nombre no puede estar vacío.")
                    
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
                
                except KeyboardInterrupt:
                    print("\nCtrl+C presionado. Saliendo de la opción...")
                            
                except ValueError:
                    print("\nDebes introducir un número entero como ID de cliente.")
            
            elif opcion == 4:
                opcion = None
                print("\nHas elegido añadir un nuevo cliente")
                nuevo_cliente = {} # IMPORTANTE: Si se ejecuta el programa con una versión anterior a Python 3.7 habrán procedimientos dentro de funciones que no funcionarán correctamente, ya que el orden no se garantiza en versiones posteriores. Este programa ha sido probado con la versión 3.11.0rc1, lo que garantiza en correcto funcionamiento.
                
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

                nuevo_cliente["nom"] = nombre
                nuevo_cliente["cognom1"] = apellido1
                nuevo_cliente["cognom2"] = apellido2
                nuevo_cliente["telefon"] = telefono
                
                try:
                    existe = dql.comprobar_generico(nombre_tabla, nuevo_cliente)
                    if not existe:
                        try:
                            dml.añadir_generico(nombre_tabla, nuevo_cliente)
                            print(f"\nSe ha añadido el nuevo cliente {nombre}, {apellido1} {apellido2}.")
                        except Exception as e:
                            print(f"\nERROR: no se ha podido añadir al nuevo cliente ({nombre}, {apellido1} {apellido2}).")
                            print(e)
                    else:
                        print("\nATENCIÓN: El cliente que intentas introducir ya existe en la BD.")
                except Exception as e:
                    print(f"\nERROR: no se ha podido comprobar si existen los datos en la BD del nuevo cliente ({nombre}).")
                    print(e)
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
                    nombre_campo = "nom"
                    valor = subopcion2_generico(nombre_campo)
                elif opcion == 2:
                    nombre_campo = "cognom1"
                    valor = subopcion2_generico(nombre_campo)
                elif opcion == 3:
                    nombre_campo = "cognom2"
                    valor = subopcion2_generico(nombre_campo)

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
                except KeyboardInterrupt:
                    print("\nCtrl+C presionado. Saliendo de la opción...")
            
            elif opcion == 4:
                opcion = None
                print("\nHas elegido añadir un nuevo empleado")
                nuevo_empleado = {}
                
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

                nuevo_empleado["nom"] = nombre
                nuevo_empleado["cognom1"] = apellido1
                nuevo_empleado["cognom2"] = apellido2
                nuevo_empleado["departament"] = departamento
                
                try:
                    existe = dql.comprobar_generico(nombre_tabla, nuevo_empleado)
                    if not existe:
                        try:
                            dml.añadir_generico(nombre_tabla, nuevo_empleado)
                            print(f"\nSe ha añadido el nuevo empleado {nombre}, {apellido1} {apellido2}.")
                        except Exception as e:
                            print(f"\nERROR: no se ha podido añadir al nuevo empleado ({nombre}, {apellido1} {apellido2}).")
                            print(e)
                    else:
                        print("\nATENCIÓN: El empleado que intentas introducir ya existe en la BD.")
                except Exception as e:
                    print(f"\nERROR: no se ha podido comprobar si existen los datos en la BD del nuevo empleado ({nombre}).")
                    print(e)
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
                mostrar_proveedores()
            
            elif opcion == 2:
                print("""
                Has elegido buscar un proveedor, ¿por qué dato quieres efectuar la búsqueda?\n
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
                except KeyboardInterrupt:
                        print("\nCtrl+C presionado. Saliendo de la opción...")
            
            elif opcion == 4:
                opcion = None
                print("\nHas elegido añadir un nuevo proveedor")
                nuevo_proveedor = {}
                
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

                
                nuevo_proveedor["empresa"] = nombre
                nuevo_proveedor["cif"] = cif
                nuevo_proveedor["adreca"] = direccion
                nuevo_proveedor["mail"] = correo
                
                try:
                    existe = dql.comprobar_generico(nombre_tabla, nuevo_proveedor)
                    if not existe:
                        try:
                            dml.añadir_generico(nombre_tabla, nuevo_proveedor)
                            print(f"\nSe ha añadido el nuevo proveedor {nombre}.")
                        except Exception as e:
                            print(f"\nERROR: no se ha podido añadir al nuevo proveedor ({nombre}.")
                            print(e)
                    else:
                        print("\nATENCIÓN: El proveedor que intentas introducir ya existe en la BD.")
                except Exception as e:
                    print(f"\nERROR: no se ha podido comprobar si existen los datos en la BD del nuevo proveedor ({nombre}).")
                    print(e)
            elif opcion == 7:
                break 
                    
    elif opcion == 4:
        print("Cerrando conexión a la BD...")
        db.desconnectar()