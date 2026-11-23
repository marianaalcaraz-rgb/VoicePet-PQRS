# Modulo de calculo de metricas y consolidacion para VoicePet
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARPETA_DATOS = os.path.join(BASE_DIR, "data")
NOMBRES_ARCHIVOS = ["Peticion.txt", "Queja.txt", "Reclamo.txt", "Sugerencia.txt"]

def cargar_todas_las_pqrs():
    """Extrae todas las PQRS de los cuatro archivos y las retorna como lista de diccionarios."""
    registros = []
    for nombre in NOMBRES_ARCHIVOS:
        ruta = os.path.join(CARPETA_DATOS, nombre)
        if os.path.exists(ruta):
            archivo = open(ruta, "r", encoding="utf-8")
            lineas = archivo.readlines()
            archivo.close()
            
            for linea in lineas[1:]:
                partes = linea.strip().split("|")
                if len(partes) >= 18:
                    registros.append({
                        "id": partes[0],
                        "nombre_completo": partes[1],
                        "tipo_documento": partes[2],
                        "numero_documento": partes[3],
                        "tipo_telefono": partes[4],
                        "telefono_contacto": partes[5],
                        "correo_electronico": partes[6],
                        "direccion": partes[7],
                        "tipo_solicitud": partes[8],
                        "fecha_radicacion": partes[9],
                        "canal_recepcion": partes[10],
                        "asunto_titulo": partes[11],
                        "descripcion_detallada": partes[12],
                        "tipo_mascota": partes[13],
                        "campus_relacionado": partes[14],
                        "fecha_maxima_respuesta": partes[15],
                        "estado_peticion": partes[16],
                        "usuario_registro": partes[17]
                    })
    return registros

def calcular_promedio_dias_respuesta():
    """Calcula el promedio entero de dias de respuesta concedidos segun norma (30 dias)."""
    registros = cargar_todas_las_pqrs()
    if not registros:
        return 30
    
    total_dias = 0
    cantidad = 0
    for r in registros:
        try:
            formato = "%Y-%m-%d %H:%M:%S"
            f_ini = datetime.strptime(r["fecha_radicacion"], formato)
            f_fin = datetime.strptime(r["fecha_maxima_respuesta"], formato)
            diferencia = f_fin - f_ini
            total_dias += diferencia.days
            cantidad += 1
        except Exception:
            continue
            
    if cantidad == 0:
        return 30
    return total_dias // cantidad

def obtener_resumen_estadistico():
    """Agrupa los datos para el modulo de metricas por consola y preparacion para Power BI."""
    registros = cargar_todas_las_pqrs()
    total = len(registros)
    
    mascotas = {"Perro": 0, "Gato": 0, "Otro": 0}
    estados = {"Registrada": 0, "En proceso": 0, "Solucionada": 0}
    tipos = {"Peticion": 0, "Queja": 0, "Reclamo": 0, "Sugerencia": 0}
    
    for r in registros:
        m = r.get("tipo_mascota", "Otro").capitalize()
        mascotas[m] = mascotas.get(m, 0) + 1
        
        e = r.get("estado_peticion", "Registrada")
        estados[e] = estados.get(e, 0) + 1
        
        t = r.get("tipo_solicitud", "Peticion").capitalize()
        tipos[t] = tipos.get(t, 0) + 1
        
    return {
        "total": total,
        "promedio_dias": calcular_promedio_dias_respuesta(),
        "mascotas": mascotas,
        "estados": estados,
        "tipos": tipos
    }
