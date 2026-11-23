# Modulo de gestion de archivos y persistencia tabular para VoicePet
import os

# Detecta la carpeta raiz del proyecto sin importar desde donde abras la terminal
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARPETA_DATOS = os.path.join(BASE_DIR, "data")
CARPETA_RADICADOS = os.path.join(BASE_DIR, "radicados")

ENCABEZADO_PQRS = (
    "id|nombre_completo|tipo_documento|numero_documento|tipo_telefono|"
    "telefono_contacto|correo_electronico|direccion|tipo_solicitud|"
    "fecha_radicacion|canal_recepcion|asunto_titulo|descripcion_detallada|"
    "tipo_mascota|campus_relacionado|fecha_maxima_respuesta|estado_peticion|usuario_registro\n"
)

def asegurar_directorios():
    """Verifica y crea las carpetas necesarias si no existen."""
    if not os.path.exists(CARPETA_DATOS):
        os.makedirs(CARPETA_DATOS)
    if not os.path.exists(CARPETA_RADICADOS):
        os.makedirs(CARPETA_RADICADOS)

def obtener_ruta(tipo_solicitud):
    """Retorna la ruta absoluta del archivo segun el tipo de tramite."""
    return os.path.join(CARPETA_DATOS, tipo_solicitud.capitalize() + ".txt")

def cargar_usuarios():
    """Lee el archivo Usuarios.txt y retorna una lista de diccionarios con las credenciales."""
    asegurar_directorios()
    ruta_usuarios = os.path.join(CARPETA_DATOS, "Usuarios.txt")
    usuarios = []
    
    if not os.path.exists(ruta_usuarios):
        return usuarios

    archivo = open(ruta_usuarios, "r", encoding="utf-8")
    lineas = archivo.readlines()
    archivo.close()

    for linea in lineas[1:]:
        datos = linea.strip().split("|")
        if len(datos) >= 6:
            usuarios.append({
                "usuario": datos[0].strip(),
                "nombre_completo": datos[1].strip(),
                "correo_institucional": datos[2].strip(),
                "contrasena": datos[3].strip(),
                "rol": datos[4].strip(),
                "estado": datos[5].strip()
            })
    return usuarios

def obtener_siguiente_id(tipo_solicitud):
    """Calcula el siguiente ID consecutivo leyendo el ultimo registro existente."""
    asegurar_directorios()
    ruta = obtener_ruta(tipo_solicitud)
    if not os.path.exists(ruta):
        return 1
    
    archivo = open(ruta, "r", encoding="utf-8")
    lineas = archivo.readlines()
    archivo.close()
    
    ultimo_id = 0
    for linea in lineas[1:]:
        linea_limpia = linea.strip()
        if linea_limpia:
            datos = linea_limpia.split("|")
            if datos[0].isdigit():
                num = int(datos[0])
                if num > ultimo_id:
                    ultimo_id = num
    return ultimo_id + 1

def guardar_pqrs(datos):
    """Agrega un nuevo registro al archivo plano correspondiente."""
    asegurar_directorios()
    ruta = obtener_ruta(datos["tipo_solicitud"])
    existe = os.path.exists(ruta)
    
    archivo = open(ruta, "a", encoding="utf-8")
    if not existe or os.path.getsize(ruta) == 0:
        archivo.write(ENCABEZADO_PQRS)
    
    linea = (
        str(datos["id"]) + "|" +
        datos["nombre_completo"] + "|" +
        datos["tipo_documento"] + "|" +
        datos["numero_documento"] + "|" +
        datos["tipo_telefono"] + "|" +
        datos["telefono_contacto"] + "|" +
        datos["correo_electronico"] + "|" +
        datos["direccion"] + "|" +
        datos["tipo_solicitud"] + "|" +
        datos["fecha_radicacion"] + "|" +
        datos["canal_recepcion"] + "|" +
        datos["asunto_titulo"] + "|" +
        datos["descripcion_detallada"] + "|" +
        datos["tipo_mascota"] + "|" +
        datos["campus_relacionado"] + "|" +
        datos["fecha_maxima_respuesta"] + "|" +
        datos["estado_peticion"] + "|" +
        datos["usuario_registro"] + "\n"
    )
    archivo.write(linea)
    archivo.close()
    return True

def generar_radicado_ascii(datos):
    """Genera el texto del comprobante formateado a exactamente 120 caracteres de ancho."""
    ancho = 120
    borde = "+" + "-" * (ancho - 2) + "+"

    def fila(texto, alinear="izq"):
        espacio = ancho - 4
        if alinear == "centro":
            contenido = texto.center(espacio)
        elif alinear == "der":
            contenido = texto.rjust(espacio)
        else:
            contenido = texto.ljust(espacio)
        return "| " + contenido + " |"

    lineas = [
        borde,
        fila("UNIVERSIDAD DE ANTIOQUIA - PROGRAMA DE ATENCION VETERINARIA", "centro"),
        fila("SISTEMA DE GESTION VOICEPET", "centro"),
        fila("COMPROBANTE FORMAL DE RADICACION PQRS", "centro"),
        borde,
        fila("RADICADO No: " + datos["tipo_solicitud"].upper() + "-" + str(datos["id"]).zfill(6) + "     ESTADO: " + datos["estado_peticion"]),
        fila("FECHA RADICACION: " + datos["fecha_radicacion"] + "     FECHA LIMITE: " + datos["fecha_maxima_respuesta"]),
        fila("USUARIO RESPONSABLE: @" + datos["usuario_registro"]),
        borde,
        fila("DATOS DEL SOLICITANTE:"),
        fila("  Nombre    : " + datos["nombre_completo"]),
        fila("  Documento : " + datos["tipo_documento"] + " " + datos["numero_documento"]),
        fila("  Contacto  : " + datos["telefono_contacto"] + " (" + datos["tipo_telefono"] + ")"),
        fila("  Correo    : " + datos["correo_electronico"]),
        fila("  Direccion : " + datos["direccion"]),
        borde,
        fila("DATOS DEL TRAMITE Y PACIENTE:"),
        fila("  Tipo Solicitud : " + datos["tipo_solicitud"] + "     Canal Recepcion : " + datos["canal_recepcion"]),
        fila("  Tipo Mascota   : " + datos["tipo_mascota"] + "         Campus Afectado : " + datos["campus_relacionado"]),
        borde,
        fila("RESUMEN DEL ASUNTO:"),
        fila("  " + datos["asunto_titulo"][:110]),
        borde,
        fila("NOTA: La institucion dispone de 30 dias calendario para dar respuesta formal.", "centro"),
        borde
    ]
    return "\n".join(lineas)

def exportar_radicado_individual(datos):
    """Guarda el comprobante de texto en la carpeta radicados/ y retorna la ruta del archivo."""
    asegurar_directorios()
    nombre_archivo = "Radicado_" + datos["tipo_solicitud"] + "_" + str(datos["id"]).zfill(6) + ".txt"
    ruta_salida = os.path.join(CARPETA_RADICADOS, nombre_archivo)
    
    contenido = generar_radicado_ascii(datos)
    archivo = open(ruta_salida, "w", encoding="utf-8")
    archivo.write(contenido)
    archivo.close()
    return ruta_salida

def guardar_comprobante(datos):
    """Alias compatible con versiones anteriores."""
    return exportar_radicado_individual(datos)

def actualizar_estado(id_pqrs, tipo_solicitud, nuevo_estado):
    """Modifica el campo de estado de un registro buscando por su ID."""
    asegurar_directorios()
    ruta = obtener_ruta(tipo_solicitud)
    if not os.path.exists(ruta):
        return False
        
    archivo = open(ruta, "r", encoding="utf-8")
    lineas = archivo.readlines()
    archivo.close()
    
    actualizado = False
    archivo_escritura = open(ruta, "w", encoding="utf-8")
    
    for linea in lineas:
        datos = linea.split("|")
        if datos[0].strip() == str(id_pqrs).strip() and datos[0].strip() != "id":
            if len(datos) >= 17:
                datos[16] = nuevo_estado
                linea = "|".join(datos)
                if not linea.endswith("\n"):
                    linea += "\n"
                actualizado = True
        archivo_escritura.write(linea)
            
    archivo_escritura.close()
    return actualizado