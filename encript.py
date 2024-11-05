from cryptography.fernet import Fernet
import base64
def generar_key():
    key = Fernet.generate_key() #Generamos una clave
    with open('clave.key', 'wb') as key_file:   #La abrimos en modo lectura binaria
        key_file.write(key) #Escribimos la key en el archivo

def cargar_key():
    return open('clave.key', 'rb').read()

def encriptar_datos(datos):
    key = cargar_key()
    f = Fernet(key)
    encriptar = f.encrypt(datos.encode())
    return encriptar.decode()

# Función para desencriptar datos
def desencriptar_datos(contraseña_encriptada):
    try:
        key = cargar_key()
        f = Fernet(key)
        # Aquí no es necesario usar base64.urlsafe_b64decode
        contraseña_desencriptada = f.decrypt(contraseña_encriptada.encode()).decode()
        return contraseña_desencriptada
    except Exception as e:
        print("Error al desencriptar la contraseña:", e)
        return None
