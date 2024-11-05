import sqlite3 as sql
import random
import string
from encript import *

#Esta funcion nos genera una clave, usando las bibliotecas random y string, con la longitud dada como parametro.
def generar_contraseña(longitud):
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres) for _ in range(longitud))

# Creamos una funcion para crear la base de datos 
def crear_database():
    #Generamos la conexión y el cursor 
    conexion = sql.connect('database.db')
    #Guardamos los cambios y cerramos la conexión
    conexion.commit()
    conexion.close()

#Esta funcion nos crea la tabla donde vamos a guardar la información
def crear_tabla():
    with sql.connect('database.db') as connection:
        cursor = connection.cursor()
        #CREAMOS LA TABLA CON LOS CAMPOS QUE VAMOS A UTILIZAR
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuario(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sitio_web TEXT NOT NULL,
                email TEXT NOT NULL,
                contraseña TEXT NOT NULL         
                )
            ''')
        connection.commit()    
#Esta funcion lo que hace es nos muestra las cuentas que tenemos guardadas en la base de datos.
def ver_cuentas():
    with sql.connect('database.db') as connection:
        cursor = connection.cursor()
        cursor.execute('SELECT * from usuario')
        filas = cursor.fetchall()
        for fila in filas:
            print(f"Cuenta: {fila}")
        print('Desea desencriptar la contraseña? (SI/NO)')
        pregunta_desencriptar = input('Elija una opción: ').upper()
        if pregunta_desencriptar != 'SI':
            print('Ok...')
        else:
            ver_cuentas_desencriptadas()

def ver_cuentas_desencriptadas():
    # Conectar a la base de datos
    conexion = sql.connect('database.db')
    cursor = conexion.cursor()
    # Seleccionar todas las filas de la tabla usuarios
    cursor.execute('SELECT * FROM usuario')
    # Fetchall recupera todos los datos de la tabla y las devuelve en forma de tupla 
    filas = cursor.fetchall()
    for fila in filas:
        # Desencriptar la contraseña (asumiendo que la contraseña está en la columna 3)
        contraseña_desencriptada = desencriptar_datos(fila[3])
        # Imprimir la fila con la contraseña desencriptada
        print(f"Cuenta: {fila}, Contraseña desencriptada: {contraseña_desencriptada}")
    conexion.close()
#Esta funcion nos borra la cuenta elegida.
def eliminar_cuenta(id):
    with sql.connect('database.db') as connection:
        cursor = connection.cursor()
        cursor.execute( ''' 
            DELETE FROM usuario 
            WHERE id = ?             
        ''', (id,))
        connection.commit()
#Esta funcion nos actualiza la contraseña.
def actualizar_contraseña(id):
    contraseña_encriptada = encriptar_datos(generar_contraseña(12))    
    with sql.connect('database.db') as connection:
        cursor = connection.cursor()
        cursor.execute('''
            UPDATE usuario u
            SET  u.contraseña = ?
            where u.id = ?
        ''', (contraseña_encriptada, id))
        connection.commit()
#Esta funcion nos permite actualizar el email.
def actualizar_email(id):
    email = input('Ingrese su nuevo email.')
    with sql.connect('database.db') as connection:
        cursor = connection.cursor()
        cursor.execute('''
            UPDATE usuario 
            SET  email = ?
            where id = ?
        ''', (email, id))
        connection.commit()
#Esta es la funcion madre para actualizar una cuenta, abarca las funciones de actualizacion de contraseña y email.
def actualizar_cuenta(id):
    print('Que queres actualizar?')
    print('A. E-MAIL \nB. Contraseña')
    respuesta = input('Elija una opción. ')
    if respuesta.upper() == 'A':
        actualizar_email(id)
    elif respuesta.upper() == 'B':
        actualizar_contraseña(id)
    else:
        print('Elija una opcion válida.')
#Esta es la funcion principal, nos permite generar una contraseña y guardarla en la base de datos
def guardar_cuenta():   
    email = input('Ingrese el email, por favor. ')   
    pregunta_pagina = input('A que página le pertenece?')
    contraseña  = preguntaEncriptar()
    with sql.connect('database.db') as connection:
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO usuario(sitio_web, email, contraseña) 
            values (?, ?, ?)
        ''', (pregunta_pagina, email, contraseña))
        connection.commit()
    print('Cuenta guardada correctamente...')

def preguntaEncriptar():
    print('Desea encriptar la contraseña? ')
    answer = input('Elija una opción: ').lower()
    if answer != 'si':
        print('Opción inválida. Vuelva a intentarlo. ')
    else:
        contraseña_encriptada = encriptar_datos(generar_contraseña(12))
        return contraseña_encriptada
