"""
Configuración general del pipeline de noticias tecno.ar
"""

# --- Feeds RSS semilla (fuente inicial de tópicos) ---
FEEDS_SEMILLA = [
    "https://techcrunch.com/feed/",
    "https://www.theverge.com/rss/index.xml",
    "https://hnrss.org/frontpage",
    "https://feeds.arstechnica.com/arstechnica/index",
]

# --- Parámetros de recolección ---
VENTANA_HORAS = 24              # solo noticias de las últimas 24hs
MAX_TOPICOS_POR_CORRIDA = 6     # cantidad de noticias a redactar por corrida
MIN_FUENTES_POR_NOTICIA = 2     # mínimo de portales con texto completo válido
MAX_FUENTES_A_BUSCAR = 6        # cuántos portales pedirle a Google News por tópico
MIN_CHARS_ARTICULO_VALIDO = 300 # descartar extracciones vacías/rotas

# --- Parámetros de redacción ---
PALABRAS_MIN = 500
PALABRAS_MAX = 700
DENSIDAD_KEYWORD_MIN = 1.0      # porcentaje
DENSIDAD_KEYWORD_MAX = 2.5
MAX_REINTENTOS_REDACCION = 2

# --- Parámetros de enlaces ---
MIN_ENLACES = 2
MAX_ENLACES = 4
ENLACES_INTERNOS_A_OFRECER = 8

# --- Modelo Gemini ---
GEMINI_MODEL = "gemini-2.5-flash"  # capa gratuita: 10 RPM / 250K TPM / 1500 RPD

# --- Archivos de estado (persisten entre corridas vía git commit) ---
HISTORIAL_PATH = "historial_publicadas.json"
ENLACES_INTERNOS_PATH = "enlaces_internos.json"
OUTPUT_DIR = "noticias"
