# ==============================================================================
# PROYECTO: VoicePet - Gestor de PQRS (UdeA)
# ==============================================================================

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Configuracion de rutas robustas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CARPETA_DATOS = os.path.join(BASE_DIR, "data")
CARPETA_SALIDA = os.path.join(BASE_DIR, "images", "analitica")
os.makedirs(CARPETA_SALIDA, exist_ok=True)

# 2. Carga y consolidacion de los archivos planos
archivos_pqrs = ["Peticion.txt", "Queja.txt", "Reclamo.txt", "Sugerencia.txt"]
columnas = [
    "id", "nombre_completo", "tipo_documento", "numero_documento",
    "tipo_telefono", "telefono_contacto", "correo_electronico", "direccion",
    "tipo_solicitud", "fecha_radicacion", "canal_recepcion", "asunto_titulo",
    "descripcion_detallada", "tipo_mascota", "campus_relacionado",
    "fecha_maxima_respuesta", "estado_peticion", "usuario_registro"
]

dfs = []
for nombre in archivos_pqrs:
    ruta = os.path.join(CARPETA_DATOS, nombre)
    if os.path.exists(ruta):
        try:
            df_temp = pd.read_csv(ruta, sep="|", dtype=str, encoding="utf-8", on_bad_lines="skip")
            if len(df_temp.columns) == len(columnas):
                df_temp.columns = columnas
                dfs.append(df_temp)
        except Exception as e:
            print(f"[!] Error leyendo {nombre}: {e}")

if not dfs:
    print("[ERROR] No se encontraron archivos de datos validos en 'data/'.")
    exit()

df = pd.concat(dfs, ignore_index=True)

# 3. Tratamiento y calculo de metricas
df["fecha_radicacion"] = pd.to_datetime(df["fecha_radicacion"], errors="coerce")
df["fecha_maxima_respuesta"] = pd.to_datetime(df["fecha_maxima_respuesta"], errors="coerce")
df["tipo_mascota"] = df["tipo_mascota"].fillna("Otro").str.strip().str.capitalize()
df["estado_peticion"] = df["estado_peticion"].fillna("Registrada").str.strip()
df["canal_recepcion"] = df["canal_recepcion"].fillna("Otro").str.strip()
df["campus_relacionado"] = df["campus_relacionado"].fillna("Otro").str.strip()

# Calculo de dias de plazo legal
df["dias_plazo"] = (df["fecha_maxima_respuesta"] - df["fecha_radicacion"]).dt.days
promedio_dias_entero = int(np.round(df["dias_plazo"].dropna().mean())) if not df["dias_plazo"].dropna().empty else 30

# Clasificacion de semaforo de control normativo (fecha de corte de auditoria)
fecha_corte = pd.to_datetime("2026-10-31 23:59:59")
def calcular_semaforo(row):
    if row["estado_peticion"] == "Solucionada":
        return "Resuelta a Tiempo"
    dias_restantes = (row["fecha_maxima_respuesta"] - fecha_corte).days
    if dias_restantes < 0:
        return "Vencida (> 30 dias)"
    elif dias_restantes <= 5:
        return "Alerta (<= 5 dias)"
    return "En Plazo Ordinario"

df["semaforo_sla"] = df.apply(calcular_semaforo, axis=1)

# 4. Diseno y renderizado del panel (300 DPI)
plt.style.use("seaborn-v0_8-whitegrid")
fig = plt.figure(figsize=(18, 11), dpi=300)
fig.patch.set_facecolor("#FAFAFC")

# Paleta corporativa VoicePet
AZUL_OSCURO = "#003366"
AZUL_ACERO = "#005691"
NARANJA_PET = "#F58220"
VERDE_OK = "#2E7D32"
ROJO_ALERTA = "#C62828"

# Grafico 1: Tarjeta KPI Promedio Obligatorio
ax1 = plt.subplot2grid((2, 3), (0, 0))
ax1.set_facecolor("#F0F4F8")
ax1.text(0.5, 0.62, f"{promedio_dias_entero}", fontsize=50, fontweight="bold",
         color=AZUL_OSCURO, ha="center", va="center")
ax1.text(0.5, 0.38, "DIAS PROMEDIO RESPUESTA\n(Plazo Legal de Tramite)",
         fontsize=11, fontweight="bold", color=AZUL_ACERO, ha="center", va="center")
ax1.text(0.5, 0.18, f"Total solicitudes auditadas: {len(df):,}", fontsize=10,
         color="#555555", ha="center", va="center")
ax1.axis("off")
ax1.set_title("KPI 1: Indicador Obligatorio SLA", fontsize=12, fontweight="bold", color=AZUL_OSCURO)

# Grafico 2: Dona de distribucion por especie
ax2 = plt.subplot2grid((2, 3), (0, 1))
conteo_mascotas = df["tipo_mascota"].value_counts()
wedges, texts, autotexts = ax2.pie(
    conteo_mascotas.values,
    labels=conteo_mascotas.index,
    autopct="%1.1f%%",
    startangle=140,
    colors=[AZUL_OSCURO, NARANJA_PET, "#78909C"][:len(conteo_mascotas)],
    textprops=dict(color=AZUL_OSCURO, fontweight="bold"),
    wedgeprops=dict(width=0.4, edgecolor="white", linewidth=2)
)
plt.setp(autotexts, size=10, weight="bold", color="white")
ax2.set_title("KPI 2: Proporcion por Paciente (Mascota)", fontsize=12, fontweight="bold", color=AZUL_OSCURO)

# Grafico 3: Balance por Estado Operativo
ax3 = plt.subplot2grid((2, 3), (0, 2))
conteo_estados = df["estado_peticion"].value_counts()
colores_est = [VERDE_OK if e == "Solucionada" else (NARANJA_PET if e == "En proceso" else AZUL_ACERO) for e in conteo_estados.index]
barras_est = ax3.bar(conteo_estados.index, conteo_estados.values, color=colores_est, edgecolor="#333333", linewidth=0.5)
ax3.set_ylabel("Cantidad de PQRS", fontsize=10, fontweight="bold", color=AZUL_OSCURO)
for b in barras_est:
    h = b.get_height()
    ax3.annotate(f"{int(h)}", (b.get_x() + b.get_width() / 2., h / 2),
                 ha="center", va="center", fontsize=11, color="white", fontweight="bold")
ax3.set_title("KPI 3: Tasa de Resolucion por Estados", fontsize=12, fontweight="bold", color=AZUL_OSCURO)

# Grafico 4: Ingreso por Canal de Recepcion
ax4 = plt.subplot2grid((2, 3), (1, 0))
conteo_canales = df["canal_recepcion"].value_counts().sort_values(ascending=True)
ax4.barh(conteo_canales.index, conteo_canales.values, color=AZUL_ACERO, edgecolor=AZUL_OSCURO)
for idx, val in enumerate(conteo_canales.values):
    ax4.text(val + (max(conteo_canales.values) * 0.02), idx, f"{val}", va="center", fontsize=9, fontweight="bold", color=AZUL_OSCURO)
ax4.set_title("KPI 4: PQRS por Canal de Ingreso", fontsize=12, fontweight="bold", color=AZUL_OSCURO)

# Grafico 5: Top 5 Sedes / Campus UdeA con mayor demanda
ax5 = plt.subplot2grid((2, 3), (1, 1))
conteo_campus = df["campus_relacionado"].str.replace("Campus Medellín - ", "").value_counts().head(5).sort_values(ascending=True)
ax5.barh(conteo_campus.index, conteo_campus.values, color="#00838F", edgecolor="#004D40")
for idx, val in enumerate(conteo_campus.values):
    ax5.text(val + (max(conteo_campus.values) * 0.02), idx, f"{val}", va="center", fontsize=9, fontweight="bold", color=AZUL_OSCURO)
ax5.set_title("KPI 5: Top 5 Campus Universitarios", fontsize=12, fontweight="bold", color=AZUL_OSCURO)

# Grafico 6: Semáforo de Control Normativo (SLA)
ax6 = plt.subplot2grid((2, 3), (1, 2))
conteo_sla = df["semaforo_sla"].value_counts()
mapa_colores = {
    "Resuelta a Tiempo": VERDE_OK,
    "En Plazo Ordinario": AZUL_ACERO,
    "Alerta (<= 5 dias)": NARANJA_PET,
    "Vencida (> 30 dias)": ROJO_ALERTA
}
colores_sla = [mapa_colores.get(s, "#757575") for s in conteo_sla.index]
ax6.bar(conteo_sla.index, conteo_sla.values, color=colores_sla, edgecolor="#333333", linewidth=0.5)
ax6.tick_params(axis="x", rotation=25)
ax6.set_ylabel("Cantidad", fontsize=10, fontweight="bold", color=AZUL_OSCURO)
for p in ax6.patches:
    h = p.get_height()
    if h > 0:
        ax6.annotate(f"{int(h)}", (p.get_x() + p.get_width() / 2., h / 2),
                     ha="center", va="center", fontsize=10, color="white", fontweight="bold")
ax6.set_title("KPI 6: Semaforo de Cumplimiento Legal", fontsize=12, fontweight="bold", color=AZUL_OSCURO)

# Encabezado principal
plt.suptitle("VOICEPET UdeA - TABLERO MAESTRO DE GESTION ANALITICA Y KPIS",
             fontsize=15, fontweight="bold", color=AZUL_OSCURO, y=0.98)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

# 5. Guardado del archivo
ruta_guardado = os.path.join(CARPETA_SALIDA, "Dashboard_KPIs_VoicePet.png")
plt.savefig(ruta_guardado, format="png", dpi=300)
plt.close()

print(f"\n[OK] Informe KPI's Generado exitosamente.")
print(f"    Informe Grafico generado en:\n     -> {ruta_guardado}")