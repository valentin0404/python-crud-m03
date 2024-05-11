#!/usr/bin/env python3
# from A2P2DB import *
import A3DB as db
# import A2P2DML as dml
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

while opcion != final:
    #######################################################
        # Menú inicial de opciones
    #######################################################
    print("""
    1. Clientes
    2. Empleados
    3. Proveedores
    4. Sortir""")

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
                        if cliente[0] == id_cliente:
                            encontrado = True
                            print(f"{sep}\nHas elegido consultar a {cliente[1]} {cliente[2]} {cliente[3]}.")
                            print(f"Su teléfono es {cliente[4]}.\n{sep}")
                            break  # Salir del bucle una vez encontrado el cliente

                    if not encontrado:
                        print("\nNo se encontró ningún cliente con el ID proporcionado.")
                else:
                    print("\nEl ID del cliente no es válido. Debe estar dentro del rango de la lista de clientes.")
                    
            except ValueError:
                print("\nDebes introducir un número entero como ID de cliente.")

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
            datos_empleados = dql.consultar_generico(nombre_tabla)
    
            # Comprobar si existen empleados y, si existen, mostrarlos
            print("\n" + sep)
            if not datos_empleados:
                print("NO existen empleados")
                print(sep)
            else:
                for empleado in datos_empleados:
                    print(empleado[CEP_ID], "-", empleado[CEP_NOM], empleado[CE_CGM1], empleado[CE_CGM2])
                print(sep)

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
            datos_proveedores = dql.consultar_generico(nombre_tabla)
    
            # Comprobar si existen proveedores y, si existen, mostrarlos
            print("\n" + sep)
            if not datos_proveedores:
                print("NO existen proveedores")
                print(sep)
            else:
                for proveedor in datos_proveedores:
                    print(proveedor[CEP_ID], "-", proveedor[CEP_NOM])
                print(sep)

    elif opcion == 4:
        print("Cerrando conexión a la BD...")
        db.desconnectar()