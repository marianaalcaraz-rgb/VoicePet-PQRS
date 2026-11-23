# ==============================================================================
# PROYECTO: VoicePet - Gestor de PQRS (Universidad de Antioquia)
# MODULO: Control de Acceso, Seguridad y Sesion
# ==============================================================================

import sys
import time
import archivos

# Variable de estado que custodia al funcionario activo
SESION_ACTUAL = None


def obtener_sesion():
    """Retorna el diccionario del usuario activo en el sistema."""
    global SESION_ACTUAL
    return SESION_ACTUAL


def cerrar_sesion():
    """Limpia la sesion activa al cerrar el sistema."""
    global SESION_ACTUAL
    SESION_ACTUAL = None


def modulo_login(fn_limpiar=None, fn_banner=None) -> bool:
    """
    Gestiona la autenticacion contra 'data/Usuarios.txt'.
    Aplica regla defensiva: 3 intentos maximos y bloqueo por 10 segundos.
    """
    global SESION_ACTUAL
    intentos = 0
    segundos_bloqueo = 10

    usuarios = archivos.cargar_usuarios()
    if not usuarios:
        print("\n[ERROR CRITICO] No se encontro o esta vacia la base de datos Usuarios.txt.")
        print("Verifique que el archivo exista dentro del directorio 'data/'.")
        return False

    while intentos < 3:
        if fn_limpiar:
            fn_limpiar()
        if fn_banner:
            fn_banner()
            
        print("          >>> CONTROL DE ACCESO AL SISTEMA - CREDENCIALES UDEA <<<\n")

        identificador = input("1. Ingrese Usuario o Correo institucional : ").strip()
        clave = input("2. Ingrese Contraseña                      : ").strip()

        for u in usuarios:
            coincide_user = u["usuario"].lower() == identificador.lower()
            coincide_correo = u["correo_institucional"].lower() == identificador.lower()
            
            if (coincide_user or coincide_correo) and u["contrasena"] == clave:
                if u["estado"].strip().lower() == "activo":
                    SESION_ACTUAL = u
                    print(f"\n[OK] Acceso concedido. Bienvenido(a), {u['nombre_completo']} ({u['rol']}).")
                    time.sleep(1.2)
                    return True
                else:
                    print("\n[DENEGADO] El usuario existe pero se encuentra inactivo en el sistema.")
                    time.sleep(2)
                    return False

        intentos += 1
        restantes = 3 - intentos
        print("\n[ERROR] Credenciales incorrectas.")
        
        if restantes > 0:
            print(f"Le quedan {restantes} intento(s) antes del bloqueo de seguridad.")
            time.sleep(1.5)
        else:
            print("\n[BLOQUEO DE SEGURIDAD] Se superaron los 3 intentos permitidos.")
            for s in range(segundos_bloqueo, 0, -1):
                sys.stdout.write(f"\rConsola bloqueada por seguridad. Espere {s:02d} segundos para reintentar...")
                sys.stdout.flush()
                time.sleep(1)
            print("\n\n[INFO] Bloqueo finalizado. Reiniciando contador de intentos...")
            intentos = 0
            time.sleep(1)

    return False