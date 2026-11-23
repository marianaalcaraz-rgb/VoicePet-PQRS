# ==============================================================================
# PROYECTO: VoicePet - Gestor de PQRS (Universidad de Antioquia)
# MODULO: main.py (Orquestador Principal, Identidad Visual y CLI)
# ==============================================================================

import os
import sys
import time

# Capa de integracion modular (desacoplada)
import archivos
import seguridad
import tramites
import analitica


def limpiar_pantalla():
    """Limpia la terminal en entornos Windows, Linux y macOS."""
    os.system("cls" if os.name == "nt" else "clear")


def mostrar_banner():
    """Imprime el isotipo y banner oficial de VoicePet en consola."""
    banner = r"""
                  ((( ( ) )))
                 ((( /   \ )))
                 _.-(\___/)-._
               .'      |      '.
              /  /^\   |  /\_/\  \
             |  /o o\  | ( o.o )  |
             |  \ w /  |  > ^ <   |
              \  /-\_  |  / _ \  /
               '._____..._____.'

 __     __ ___  ___  ____  _____   ____  _____  _____ 
 \ \   / // _ \|_ _|/ ___|| ____| |  _ \| ____||_   _|
  \ \ / /| | | || || |    |  _|   | |_) |  _|    | |  
   \ V / | |_| || || |___ | |___  |  __/| |___   | |  
    \_/   \___/|___|\____||_____| |_|   |_____|  |_|  
-------------------------------------------------------
 SISTEMA VETERINARIO INTELIGENTE | Tu voz, su mejor cuidado
    """
    print(banner)


def menu_principal():
    """Menu interactivo que enruta las operaciones hacia los modulos correspondientes."""
    sesion = seguridad.obtener_sesion()

    while True:
        limpiar_pantalla()
        mostrar_banner()
        print(f" OPERADOR ACTIVO: {sesion['nombre_completo']}")
        print(f" ROL: {sesion['rol']} | USUARIO: @{sesion['usuario']}")
        print("-" * 75)
        print("  1. Registrar nueva PQRS (Peticion, Queja, Reclamo, Sugerencia)")
        print("  2. Consultar estado de PQRS (Vista comprobante)")
        print("  3. Registrar cambio de estado en PQRS")
        print("  4. Metricas y estadisticas basicas (Consola)")
        print("  5. Exportar Capa Analitica Avanzada (Pandas / Power BI)")
        print("  6. Cerrar sesion y salir")
        print("-" * 75)

        opcion = input("Seleccione una operacion (1-6): ").strip()

        if opcion == "1":
            tramites.formulario_registro_pqrs(sesion, limpiar_pantalla)
        elif opcion == "2":
            tramites.consultar_pqrs(limpiar_pantalla)
        elif opcion == "3":
            tramites.registrar_cambio_estado(limpiar_pantalla)
        elif opcion == "4":
            analitica.mostrar_modulo_estadisticas(limpiar_pantalla)
        elif opcion == "5":
            analitica.exportar_capa_pandas()
        elif opcion == "6":
            print(f"\nCerrando sesion de @{sesion['usuario']}...")
            seguridad.cerrar_sesion()
            time.sleep(1)
            break
        else:
            print("\n[!] Opcion invalida. Digite un numero del 1 al 6.")
            time.sleep(1.2)


def main():
    """Punto de arranque del sistema."""
    try:
        archivos.asegurar_directorios()
        if seguridad.modulo_login(limpiar_pantalla, mostrar_banner):
            menu_principal()
    except KeyboardInterrupt:
        print("\n\n[INFO] Ejecucion finalizada por el usuario (Ctrl + C). Saliendo...")
        sys.exit(0)


if __name__ == "__main__":
    main()