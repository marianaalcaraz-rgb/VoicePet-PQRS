# Modulo de validaciones basicas para VoicePet
# Utiliza logica condicional simple

def validar_nombre(nombre):
    if len(nombre) >= 3 and len(nombre) <= 100:
        return True
    return False

def validar_tipo_documento(tipo):
    tipos_validos = ["CC", "TI", "CE", "PP", "NIT"]
    if tipo.upper() in tipos_validos:
        return True
    return False

def validar_numero_documento(numero):
    if numero.isdigit():
        if len(numero) >= 3 and len(numero) <= 15:
            return True
    return False

def validar_tipo_telefono(tipo):
    tipos_validos = ["Celular", "Fijo", "Corporativo", "Otro"]
    if tipo.capitalize() in tipos_validos:
        return True
    return False

def validar_telefono(numero):
    if numero.isdigit() and len(numero) == 10:
        return True
    return False

def validar_correo(correo):
    if "@" in correo and "." in correo:
        if len(correo) <= 254:
            return True
    return False

def validar_tipo_solicitud(tipo):
    tipos_validos = ["Peticion", "Queja", "Reclamo", "Sugerencia"]
    if tipo.capitalize() in tipos_validos:
        return True
    return False

def validar_canal(canal):
    canales = ["Presencial", "Correo electronico", "Pagina web", "Telefono", "Redes sociales", "Otro"]
    for c in canales:
        if c.lower() == canal.lower():
            return True
    return False

def validar_mascota(mascota):
    tipos = ["Perro", "Gato", "Otro"]
    if mascota.capitalize() in tipos:
        return True
    return False
