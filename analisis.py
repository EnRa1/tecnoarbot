"""
Deduplicación contra historial, clustering de fuentes por similitud,
y extracción automática de la palabra clave.
"""
import json
import re
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from config import HISTORIAL_PATH, MAX_TOPICOS_POR_CORRIDA

STOPWORDS_ES = {
    "el", "la", "los", "las", "de", "del", "en", "y", "a", "que", "un", "una",
    "por", "con", "para", "su", "es", "se", "al", "lo", "como", "más", "o",
    "sobre", "sus", "le", "ya", "fue", "ha", "han", "este", "esta",
}


# ---------- Historial / deduplicación ----------

def cargar_historial():
    path = Path(HISTORIAL_PATH)
    if path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))
        limite = datetime.now() - timedelta(days=7)
        return [h for h in data if datetime.fromisoformat(h["fecha"]) > limite]
    return []


def guardar_historial(historial):
    Path(HISTORIAL_PATH).write_text(
        json.dumps(historial, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def _similitud(a, b):
    try:
        vect = TfidfVectorizer().fit([a, b])
        m = vect.transform([a, b])
        return cosine_similarity(m[0], m[1])[0][0]
    except ValueError:
        return 0.0  # textos vacíos o solo stopwords


def ya_fue_publicada(titulo, historial, umbral=0.5):
    return any(_similitud(titulo, h["titulo"]) >= umbral for h in historial)


def elegir_topicos(candidatos, historial, cantidad=MAX_TOPICOS_POR_CORRIDA):
    elegidos = []
    for c in candidatos:
        if len(elegidos) >= cantidad:
            break
        if not ya_fue_publicada(c["titulo"], historial):
            elegidos.append(c)
    return elegidos


# ---------- Clustering de fuentes (confirmar que hablan de lo mismo) ----------

def son_la_misma_noticia(texto_a, texto_b, umbral=0.30):
    return _similitud(texto_a[:1500], texto_b[:1500]) >= umbral


def filtrar_fuentes_relevantes(titulo_topico, articulos):
    """Descarta artículos que Google News trajo por ruido temático."""
    relevantes = []
    for art in articulos:
        if son_la_misma_noticia(titulo_topico, art["texto"]):
            relevantes.append(art)
    return relevantes


# ---------- Palabra clave ----------

def extraer_palabra_clave(titulo, articulos_completos):
    texto = titulo + " " + " ".join(a["texto"][:500] for a in articulos_completos)
    palabras = re.findall(r"[a-záéíóúñ]{4,}", texto.lower())
    palabras = [p for p in palabras if p not in STOPWORDS_ES]
    conteo = Counter(palabras)

    palabras_titulo = set(re.findall(r"[a-záéíóúñ]{4,}", titulo.lower()))
    candidatos = [(p, c) for p, c in conteo.most_common(15) if p in palabras_titulo]

    if candidatos:
        return candidatos[0][0]
    if conteo:
        return conteo.most_common(1)[0][0]
    return titulo.split()[0].lower() if titulo else "tecnologia"
