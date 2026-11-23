# ==============================================================================
# PROYECTO: VoicePet - Gestor de PQRS (Universidad de Antioquia)
# MODULO: Formularios CLI, Radicacion, Consultas y Estados
# ==============================================================================

import time
from datetime import datetime, timedelta
import validaciones
import archivos
import reportes


def formulario_registro_pqrs(usuario_activo: dict, fn_limpiar=None):
    """
    Formulario interactivo de radicación paso a paso.
    Asigna consecutivo independiente, calcula fechas y emite comprobante ASCII a 120 columnas.
    """
    if fn_limpiar:
        fn_limpiar()
        
    print("=" * 120)
    print("FORMULARIO OFICIAL DE RADICACION PQRS - VOICEPET UDEA".center(120))
    print("=" * 120)

    # 1. TIPO DE SOLICITUD
    print("\n[PASO 1 de 4] Clasificacion de la Solicitud")
    print("  1. Peticion\n  2. Queja\n  3. Reclamo\n  4. Sugerencia")
    
    mapa_solicitudes = {"1": "Peticion", "2": "Queja", "3": "Reclamo", "4": "Sugerencia"}
    while True:
        opc = input("Seleccione el tipo de trámite (1-4): ").strip()
        if opc in mapa_solicitudes:
            tipo_solicitud = mapa_solicitudes[opc]
            break
        print("  [!] Opcion invalida. Digite un numero del 1 al 4.")

    id_registro = archivos.obtener_siguiente_id(tipo_solicitud)
    print(f"  -> Consecutivo asignado para {tipo_solicitud}: #{id_registro}")

    # 2. DATOS DEL SOLICITANTE
    print("\n[PASO 2 de 4] Datos del Solicitante")

    while True:
        nombre = input("  • Nombre completo (3 a 100 caracteres, solo letras): ")
        valido, res = validaciones.validar_nombre_completo(nombre)
        if valido:
            nombre_completo = res
            break
        print(f"    [!] {res}")

    print("    Tipos permitidos: CC, TI, CE, PP, NIT")
    while True:
        tipo_doc_in = input("  • Tipo de documento: ")
        valido, res = validaciones.validar_tipo_documento(tipo_doc_in)
        if valido:
            tipo_documento = res
            break
        print(f"    [!] {res}")

    while True:
        num_doc_in = input("  • Numero de documento (3 a 15 digitos): ")
        valido, res = validaciones.validar_numero_documento(num_doc_in)
        if valido:
            numero_documento = res
            break
        print(f"    [!] {res}")

    print("    Tipos de linea: Celular, Fijo, Corporativo, Otro")
    while True:
        t_tel_in = input("  • Tipo de telefono: ")
        valido, res = validaciones.validar_tipo_telefono(t_tel_in)
        if valido:
            tipo_telefono = res
            break
        print(f"    [!] {res}")

    while True:
        tel_in = input("  • Telefono de contacto (10 digitos exactos): ")
        valido, res = validaciones.validar_telefono_contacto(tel_in)
        if valido:
            telefono_contacto = res
            break
        print(f"    [!] {res}")

    while True:
        correo_in = input("  • Correo electronico (usuario@dominio.ext): ")
        valido, res = validaciones.validar_correo_electronico(correo_in)
        if valido:
            correo_electronico = res
            break
        print(f"    [!] {res}")

    dir_in = input("  • Direccion de residencia (Opcional - Enter para omitir): ")
    direccion = validaciones.validar_direccion(dir_in)

    # 3. DETALLE DEL TRAMITE Y MASCOTA
    print("\n[PASO 3 de 4] Detalle del Tramite y Paciente")
    
    print("  Canales de atencion disponibles:")
    for i, c in enumerate(validaciones.CANALES_RECEPCION, 1):
        print(f"    {i}. {c}")
    while True:
        c_in = input(f"  • Seleccione canal de recepcion (1-{len(validaciones.CANALES_RECEPCION)}): ").strip()
        if c_in.isdigit() and 1 <= int(c_in) <= len(validaciones.CANALES_RECEPCION):
            canal_recepcion = validaciones.CANALES_RECEPCION[int(c_in) - 1]
            break
        print("    [!] Seleccion invalida.")

    while True:
        asunto_in = input("  • Asunto o titulo (5 a 150 caracteres): ")
        valido, res = validaciones.validar_asunto(asunto_in)
        if valido:
            asunto_titulo = res
            break
        print(f"    [!] {res}")

    while True:
        desc_in = input("  • Descripcion detallada (minimo 20 caracteres):\n    > ")
        valido, res = validaciones.validar_descripcion(desc_in)
        if valido:
            descripcion_detallada = res
            break
        print(f"    [!] {res}")

    print("  Tipo de mascota:\n    1. Perro\n    2. Gato\n    3. Otro")
    mapa_mascotas = {"1": "Perro", "2": "Gato", "3": "Otro"}
    while True:
        m_in = input("  • Seleccione mascota (1-3): ").strip()
        if m_in in mapa_mascotas:
            tipo_mascota = mapa_mascotas[m_in]
            break
        print("    [!] Opcion invalida.")

    print("  Campus UdeA relacionado:")
    for idx, sede in enumerate(validaciones.CAMPUS_VALIDOS, 1):
        print(f"    {idx}. {sede}")
    while True:
        s_in = input(f"  • Seleccione campus (1-{len(validaciones.CAMPUS_VALIDOS)}): ").strip()
        if s_in.isdigit():
            valido, res = validaciones.validar_campus(int(s_in))
            if valido:
                campus_relacionado = res
                break
        print("    [!] Opcion no valida.")

    # 4. TIEMPOS Y PERSISTENCIA
    print("\n[PASO 4 de 4] Guardando en base de datos plana...")
    ahora = datetime.now()
    fecha_radicacion = ahora.strftime("%Y-%m-%d %H:%M:%S")
    fecha_maxima = (ahora + timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")
    
    registro_dict = {
        "id": id_registro,
        "nombre_completo": nombre_completo,
        "tipo_documento": tipo_documento,
        "numero_documento": numero_documento,
        "tipo_telefono": tipo_telefono,
        "telefono_contacto": telefono_contacto,
        "correo_electronico": correo_electronico,
        "direccion": direccion,
        "tipo_solicitud": tipo_solicitud,
        "fecha_radicacion": fecha_radicacion,
        "canal_recepcion": canal_recepcion,
        "asunto_titulo": asunto_titulo,
        "descripcion_detallada": descripcion_detallada,
        "tipo_mascota": tipo_mascota,
        "campus_relacionado": campus_relacionado,
        "fecha_maxima_respuesta": fecha_maxima,
        "estado_peticion": "Registrada",
        "usuario_registro": usuario_activo["usuario"]
    }

    if archivos.guardar_pqrs(registro_dict):
        ruta_archivo = archivos.exportar_radicado_individual(registro_dict)
        print("\n" + "=" * 120)
        print("RADICACION EXITOSA".center(120))
        print("=" * 120)
        print(f"[OK] Registro almacenado en: data/{tipo_solicitud}.txt")
        print(f"[OK] Comprobante físico exportado en: {ruta_archivo}\n")
        print(archivos.generar_radicado_ascii(registro_dict))
    else:
        print("\n[ERROR CRITICO] Ocurrio un fallo al guardar la informacion en el disco.")

    input("\nPresione Enter para regresar al Menu Principal...")


def consultar_pqrs(fn_limpiar=None):
    """Consulta y muestra el comprobante ASCII de una solicitud por ID."""
    if fn_limpiar:
        fn_limpiar()
        
    print("=" * 80)
    print("CONSULTA DE RADICADOS PQRS - VOICEPET".center(80))
    print("=" * 80)
    
    tipo = input("\nIngrese tipo de solicitud (Peticion/Queja/Reclamo/Sugerencia): ").strip().capitalize()
    valido, tipo_normalizado = validaciones.validar_tipo_solicitud(tipo)
    if not valido:
        print(f"[!] {tipo_normalizado}")
        time.sleep(2)
        return

    id_buscar = input("Ingrese el numero de ID o radicado a consultar: ").strip()
    if not id_buscar.isdigit():
        print("[!] El ID debe ser un numero entero.")
        time.sleep(2)
        return

    todas = reportes.cargar_todas_las_pqrs()
    encontrada = None
    for r in todas:
        if r["tipo_solicitud"].lower() == tipo_normalizado.lower() and str(r["id"]) == id_buscar:
            encontrada = r
            break

    if encontrada:
        print("\n[OK] Registro localizado:\n")
        print(archivos.generar_radicado_ascii(encontrada))
    else:
        print(f"\n[!] No se encontro ningun registro para {tipo_normalizado} con el ID #{id_buscar}.")
    
    input("\nPresione Enter para continuar...")


def registrar_cambio_estado(fn_limpiar=None):
    """Permite transicionar el estado de Registrada a En proceso o Solucionada."""
    if fn_limpiar:
        fn_limpiar()
        
    print("=" * 80)
    print("ACTUALIZACION DE ESTADO DE PQRS - VOICEPET".center(80))
    print("=" * 80)
    
    tipo = input("\nIngrese el tipo de solicitud (Peticion/Queja/Reclamo/Sugerencia): ").strip().capitalize()
    valido, tipo_solicitud = validaciones.validar_tipo_solicitud(tipo)
    if not valido:
        print(f"[!] {tipo_solicitud}")
        time.sleep(1.5)
        return

    id_pqrs = input("Ingrese el ID de la solicitud a modificar: ").strip()
    if not id_pqrs.isdigit():
        print("[!] El ID debe ser numerico.")
        time.sleep(1.5)
        return

    print("\nEstados permitidos:\n  1. En proceso\n  2. Solucionada")
    opc = input("Seleccione el nuevo estado (1-2): ").strip()
    
    mapa_estados = {"1": "En proceso", "2": "Solucionada"}
    if opc not in mapa_estados:
        print("[!] Opcion no valida.")
        time.sleep(1.5)
        return

    nuevo_estado = mapa_estados[opc]
    if archivos.actualizar_estado(id_pqrs, tipo_solicitud, nuevo_estado):
        print(f"\n[OK] Solicitud {tipo_solicitud} #{id_pqrs} actualizada a: '{nuevo_estado}'.")
    else:
        print(f"\n[!] No se encontro el radicado en data/{tipo_solicitud}.txt.")
    
    input("\nPresione Enter para continuar...")