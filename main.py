from functs import *
from encript import generar_key, cargar_key
import sys

def main():
    # Verifica si existe el archivo de clave, si no, genera una nueva clave
    try:
        cargar_key()
    except FileNotFoundError:
        generar_key()

    while True:
        print('QUE TAREA DESEA REALIZAR? \n A. Generar nueva cuenta \n B. Ver cuentas \n C. Eliminar cuenta \n D. Actualizar cuenta \n E. Salir')
        resp = input('Seleccione una tarea.')
        if resp.upper() == 'A': 
            sitio = input('¿Dónde vas a guardar esta contraseña? ')
            email = input('¿Y el email? ')
            contraseña = generate_pass(10) 
            # Crear la base de datos y la tabla si no existen
            crear_database()    
            crear_tabla()
            # Insertar la cuenta en la base de datos
            insertar_cuenta(sitio, email, contraseña)
        elif resp.upper() == 'B':
            ver_cuentas()
            option = input('Desencriptar las contraseñas? \n (SI/NO) \n ')
            if option.upper() == 'SI':
                ver_cuentas_desencriptadas()
            else:
                pass
        elif resp.upper() == 'C':
            sitio = input('De que sitio es la cuenta a eliminar?')
            eliminar_cuenta(sitio)

        elif resp.upper() == 'D':
            resp = input('Desea cambiar una contraseña o email? ')
            if resp.lower() == 'contraseña':
                sitio = input('De que sitio es la cuenta? ')
                nueva_contraseña = generate_pass(10)
                actualizar_contraseña(sitio, nueva_contraseña)
                print('La contraseña se modificó correctamente.')
            else:
                sitio = input('De que sitio es la cuenta? ')
                actualizar_cuenta(resp, sitio)
                print('El email se modificó correctamente.')
        else:
            print('Saliendo del programa...')
            sys.exit()
            


if __name__ == '__main__':
    main()
