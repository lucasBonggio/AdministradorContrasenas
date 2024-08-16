import sqlite3
import string
import random
from encript import encriptar, desencriptar_contraseña, encriptar_new

# Generar contraseña
def generate_pass(longitud, usar_caracteres_especiales=True):
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres) for _ in range(longitud))

# Crear bd
def crear_database():
    conexion = sqlite3.connect('database.db')
    cursor = conexion.cursor()
    conexion.commit()
    conexion.close()

# Crear tabla
def crear_tabla():
    # Conectarse a la base de datos
    conexion = sqlite3.connect('database.db')
    cursor = conexion.cursor()
    # Crear tabla
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sitio_web TEXT NOT NULL,
            email TEXT NOT NULL,
            contraseña TEXT NOT NULL
        )
    ''')
    conexion.commit()
    conexion.close()

# Añadir cuenta
@encriptar
def insertar_cuenta(sitio, email, contraseña_encriptada):
    # Conectar a la base de datos
    conexion = sqlite3.connect('database.db')
    cursor = conexion.cursor()
    # Insertar datos en la tabla
    cursor.execute('''
        INSERT INTO usuarios (sitio_web, email, contraseña)
        VALUES (?, ?, ?)
    ''', (sitio, email, contraseña_encriptada))
    # Guardar los cambios
    conexion.commit()
    # Cerrar la conexión
    conexion.close()

# Mostrar cuentas
def ver_cuentas():
    # Conectar a la base de datos
    conexion = sqlite3.connect('database.db')
    cursor = conexion.cursor()
    # Seleccionar todas las filas de la tabla usuarios
    cursor.execute('SELECT * FROM usuarios')
    # Fetchall recupera todos los datos de la tabla y las devuelve en forma de tupla 
    filas = cursor.fetchall()
    for fila in filas:
        print(fila)
    conexion.close()    

# Eliminar cuenta
def eliminar_cuenta(sitio_web):
    # Conectarse a la base de datos
    conexion = sqlite3.connect('database.db')
    cursor = conexion.cursor()    
    #Seleccionar la cuenta a eliminar
    cursor.execute('''
        DELETE FROM USUARIOS
        WHERE sitio_web = ?
    ''', (sitio_web,))
    conexion.commit()
    conexion.close()

# Actualizar contraseña y encriptar    
@encriptar_new
def actualizar_contraseña(sitio_web, nueva_contraseña):
    # Conectarse a la base de datos
    conexion = sqlite3.connect('database.db')
    cursor = conexion.cursor()
    # Seleccionar la tabla a modificar
    cursor.execute('''
        UPDATE usuarios
        SET contraseña = ?
        WHERE sitio_web = ?
    ''', (nueva_contraseña, sitio_web))
    conexion.commit()
    conexion.close()

# Actualizar contraseña o email
def actualizar_cuenta(resp, sitio_web):
    # Para garantizar que la respuesta sea válida
    if resp not in ('contraseña', 'email'):
        print("Respuesta no válida. Debe ser 'contraseña' o 'email'.")
        return
    # Sanitizar los datos
    if resp == 'contraseña':
        nueva_contraseña = generate_pass(10)
        actualizar_contraseña(nueva_contraseña, sitio_web)
        
    else:
        # Pedir nuevo email
        nuevo_email = input('Que correo desea asociar esta cuenta? ')
        # Conectarse a la base de datos
        conexion = sqlite3.connect('database.db')
        cursor = conexion.cursor()
        # Seleccionar la tabla a modificar
        cursor.execute('''
            UPDATE usuarios
            SET email = ?
            WHERE sitio_web = ?
        ''', (nuevo_email, sitio_web))
        conexion.commit()
        conexion.close()

def guardar_cuenta(sitio, email, contraseña):
    question = input('Desea guardar la contraseña? ')
    if question.lower() == 'si':
        # Conectar a la base de datos
        conexion = sqlite3.connect('database.db')
        cursor = conexion.cursor()
        # Insertar datos en la tabla
        cursor.execute('''
            INSERT INTO usuarios (sitio, email, contraseña)
            VALUES (?, ?, ?)
        ''', (sitio, email, contraseña))
        # Guardar los cambios
        conexion.commit()
        # Cerrar la conexión
        conexion.close()
    elif question.lower() == 'no':
        print('Okey...generemos otra para nueva!')
    else:
        print('Respuesta inválida. Por favor introduzca una respuesta válida. ')

# Mostrar cuentas desencriptadas
def ver_cuentas_desencriptadas():
    # Conectar a la base de datos
    conexion = sqlite3.connect('database.db')
    cursor = conexion.cursor()
    # Seleccionar todas las filas de la tabla usuarios
    cursor.execute('SELECT * FROM usuarios')
    # Fetchall recupera todos los datos de la tabla y las devuelve en forma de tupla 
    filas = cursor.fetchall()
    for fila in filas:
        # Desencriptar la contraseña (asumiendo que la contraseña está en la columna 3)
        contraseña_desencriptada = desencriptar_contraseña(fila[3])
        # Imprimir la fila con la contraseña desencriptada
        print(f"Fila: {fila}, Contraseña desencriptada: {contraseña_desencriptada}")
    conexion.close()
