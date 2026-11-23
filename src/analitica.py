# ==============================================================================
# PROYECTO: VoicePet - Gestor de PQRS (Universidad de Antioquia)
# MODULO: Metricas de Gestion y Pipeline ETL con Pandas
# ==============================================================================

import os
import reportes


def mostrar_modulo_estadisticas(fn_limpiar=None):
    """Muestra en terminal el balance de gestion y la metrica entera de 30 dias."""
    if fn_limpiar:
        fn_limpiar()
        
    resumen = reportes.obtener_resumen_estadistico()
    
    print("=" * 80)
    print("TABLERO DE CONTROL Y METRICAS DEL SISTEMA - VOICEPET".center(80))
    print("=" * 80)
    
    print(f"\n• Total de radicados consolidados en base de datos : {resumen['total']}")
    print(f"• Promedio normativo de dias para respuesta legal  : {resumen['promedio_dias']} dias (Valor entero)")
    
    if resumen["total"] > 0:
        print("\n--- DISTRIBUCION POR PACIENTE (MASCOTA) ---")
        for mascota, cant in resumen["mascotas"].items():
            porcentaje = (cant / resumen["total"]) * 100
            print(f"  - {mascota:<10}: {cant:4d} registros ({porcentaje:5.1f}%)")

        print("\n--- DISTRIBUCION POR TIPO DE DOCUMENTO ---")
        for tipo, cant in resumen["tipos"].items():
            porcentaje = (cant / resumen["total"]) * 100
            print(f"  - {tipo:<12}: {cant:4d} registros ({porcentaje:5.1f}%)")

        print("\n--- BALANCE POR ESTADO DE GESTION ---")
        for estado, cant in resumen["estados"].items():
            porcentaje = (cant / resumen["total"]) * 100
            print(f"  - {estado:<12}: {cant:4d} registros ({porcentaje:5.1f}%)")
    else:
        print("\n[INFO] No hay registros suficientes en 'data/' para graficar distribuciones.")
        
    print("=" * 80)
    input("\nPresione Enter para volver al menu...")


def exportar_capa_pandas():
    """
    Lee los 4 archivos planos directamente con Pandas, computa indicadores avanzados
    y exporta la tabla de hechos consolidada lista para Power BI.
    """
    try:
        import pandas as pd
        import numpy as np
    except ImportError:
        print("\n[!] Pandas no esta instalado en este entorno.")
        print("    Para usar esta funcion instale la libreria con: pip install pandas openpyxl")
        input("Presione Enter para continuar...")
        return

    print("\n" + "=" * 60)
    print("      GENERANDO CAPA ANALITICA CON PANDAS (VOICEPET)")
    print("=" * 60)

    archivos_origen = {
        "Peticion": "data/Peticion.txt",
        "Queja": "data/Queja.txt",
        "Reclamo": "data/Reclamo.txt",
        "Sugerencia": "data/Sugerencia.txt"
    }

    if not os.path.exists("data"):
        archivos_origen = {k: f"../{v}" for k, v in archivos_origen.items()}

    lista_df = []
    columnas_estandar = [
        "id", "nombre_completo", "tipo_documento", "numero_documento",
        "tipo_telefono", "telefono_contacto", "correo_electronico", "direccion",
        "tipo_solicitud", "fecha_radicacion", "canal_recepcion", "asunto_titulo",
        "descripcion_detallada", "tipo_mascota", "campus_relacionado",
        "fecha_maxima_respuesta", "estado_peticion", "usuario_registro"
    ]

    for tipo, ruta in archivos_origen.items():
        if os.path.exists(ruta):
            try:
                df_temp = pd.read_csv(ruta, sep="|", dtype=str, encoding="utf-8", on_bad_lines="skip")
                if len(df_temp.columns) == len(columnas_estandar):
                    df_temp.columns = columnas_estandar
                    lista_df.append(df_temp)
            except Exception as e:
                print(f"[!] Error leyendo {ruta}: {e}")

    if not lista_df:
        print("[!] No se encontraron registros para procesar.")
        input("Presione Enter para continuar...")
        return

    df_consolidado = pd.concat(lista_df, ignore_index=True)

    print("-> Limpiando datos y computando semaforo SLA...")
    df_consolidado["fecha_radicacion"] = pd.to_datetime(df_consolidado["fecha_radicacion"], errors="coerce")
    df_consolidado["fecha_maxima_respuesta"] = pd.to_datetime(df_consolidado["fecha_maxima_respuesta"], errors="coerce")
    
    df_consolidado["dias_plazo"] = (df_consolidado["fecha_maxima_respuesta"] - df_consolidado["fecha_radicacion"]).dt.days
    promedio_dias_entero = int(np.round(df_consolidado["dias_plazo"].dropna().mean()))

    conteo_mascotas = df_consolidado["tipo_mascota"].str.capitalize().value_counts().to_dict()
    conteo_estados = df_consolidado["estado_peticion"].value_counts().to_dict()

    carpeta_salida = "data_analitica"
    if not os.path.exists("data"):
        carpeta_salida = "../data_analitica"
    os.makedirs(carpeta_salida, exist_ok=True)

    ruta_csv_bi = os.path.join(carpeta_salida, "VoicePet_Consolidado_BI.csv")
    df_consolidado.to_csv(ruta_csv_bi, sep="|", index=False, encoding="utf-8")

    print("\n[OK] Pipeline ETL finalizado exitosamente:")
    print(f"     Total registros procesados : {len(df_consolidado)}")
    print(f"     Promedio dias respuesta    : {promedio_dias_entero} dias")
    print(f"     Distribucion de pacientes  : {conteo_mascotas}")
    print(f"     Estados de solicitudes     : {conteo_estados}")
    print(f"\n[OK] Archivo exportado para Power BI en: {ruta_csv_bi}")
    print("=" * 60)
    input("\nPresione Enter para volver al menu...")