
from functs import *
from encript import *
import sys

def main():
    try:
        cargar_key()
    except FileNotFoundError:
        generar_key()

    while True:
        print("¿Qué tarea desea realizar?")
        print("A. Generar nueva cuenta \n B. Ver cuentas \n C. Eliminar cuenta \n D.Actualizar contraseña \n E. Salir")
        resp = input("Seleccione una tarea. ")
        if resp.upper() == "A":
            crear_database()
            crear_tabla()
            guardar_cuenta()
        elif resp.upper() == 'B':
            ver_cuentas()
        elif resp.upper() == 'C':
            cuenta = input('¿Qué cuenta desea eliminar?')
            eliminar_cuenta(cuenta)
        elif resp.upper() == 'D':
            cuenta_actualizar = input('¿Qué cuenta desea actualizar?')
            actualizar_cuenta(cuenta_actualizar)
        elif resp.upper() == 'E':
            print('Saliendo del programa...')
            sys.exit()
        else:
            print('Elija una opción válida.')

if __name__ == '__main__':
    main()
