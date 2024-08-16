from cryptography.fernet import Fernet
import base64

# Generar clave y guardarla en un archivo
def generar_key():
    key = Fernet.generate_key()
    with open('clave.key', 'wb') as key_file:
        key_file.write(key)

# Cargar clave desde un archivo
def cargar_key():
    return open('clave.key', 'rb').read()

# Encriptar datos
def encriptar_datos(datos):
    key = cargar_key()
    f = Fernet(key)
    encrypted_data = f.encrypt(datos.encode())
    return base64.urlsafe_b64encode(encrypted_data).decode()  # Convertir a cadena

# Encriptar
def encriptar(func):
    def wrapper(sitio, email, contraseña):
        contraseña_encriptada = encriptar_datos(contraseña)
        return func(sitio, email, contraseña_encriptada)
    return wrapper

# Enctriptar solo contraseña
def encriptar_new(func):
    def wrapper(sitio, nueva_contraseña):
        contraseña_encriptada = encriptar_datos(nueva_contraseña)
        return func(sitio, contraseña_encriptada)
    return wrapper

# Desencriptar contraseña
def desencriptar_contraseña(contraseña_encriptada):
    try:
        key = cargar_key()
        f = Fernet(key)
        # Convertir de cadena a bytes
        encrypted_data = base64.urlsafe_b64decode(contraseña_encriptada)  
        contraseña_desencriptada = f.decrypt(encrypted_data).decode()
        return contraseña_desencriptada
    except Exception as e:
        print("Error al desencriptar la contraseña:", e)
        return None
