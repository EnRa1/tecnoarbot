"""
Recolección de tópicos y búsqueda de portales relacionados.
"""
import re
import time
from datetime import datetime, timezone, timedelta
from urllib.parse import quote

import feedparser
import requests

from config import FEEDS_SEMILLA, VENTANA_HORAS, MAX_FUENTES_A_BUSCAR

# Palabras vacías en inglés (las fuentes semilla son medios en inglés) para
# limpiar el título y quedarnos con los términos que realmente identifican
# la noticia. Un título completo como query es demasiado específico: casi
# ningún otro portal lo redacta igual, y Google News devuelve 0 resultados.
_STOPWORDS_EN = {
    "the", "a", "an", "and", "or", "of", "in", "on", "for", "to", "is", "are",
    "this", "that", "with", "at", "by", "from", "as", "it", "its", "be",
    "was", "were", "will", "can", "could", "should", "not", "no", "new",
    "how", "why", "what", "who", "your", "you", "we", "our", "their",
    "than", "into", "up", "out", "all", "just", "now", "still", "get",
}


def _simplificar_query(titulo, max_palabras=6):
    """Convierte un título largo/específico en términos de búsqueda más
    genéricos, para que otros portales que cubrieron lo mismo con otra
    redacción también aparezcan en los resultados."""
    limpio = re.sub(r"[^\w\s]", " ", titulo)  # saca : ? ¿ ! ( ) etc.
    palabras = limpio.split()
    relevantes = [p for p in palabras if p.lower() not in _STOPWORDS_EN and len(p) > 2]
    if not relevantes:
        relevantes = palabras
    return " ".join(relevantes[:max_palabras])


def _dentro_de_ventana(entry, horas):
    campo_fecha = entry.get("published_parsed") or entry.get("updated_parsed")
    if not campo_fecha:
        return False  # sin fecha confiable, se descarta
    fecha_pub = datetime.fromtimestamp(time.mktime(campo_fecha), tz=timezone.utc)
    limite = datetime.now(timezone.utc) - timedelta(hours=horas)
    return fecha_pub >= limite


def recolectar_topicos_semilla():
    """Recorre los feeds RSS semilla y devuelve tópicos de las últimas 24hs."""
    items = []
    for url in FEEDS_SEMILLA:
        try:
            feed = feedparser.parse(url)
        except Exception as e:
            print(f"  [aviso] no se pudo leer feed {url}: {e}")
            continue

        for entry in feed.entries:
            if not _dentro_de_ventana(entry, VENTANA_HORAS):
                continue
            items.append({
                "titulo": entry.title,
                "resumen": entry.get("summary", ""),
                "link": entry.link,
                "fuente": feed.feed.get("title", url),
            })
    return items


def _consultar_google_news(query, idioma, pais):
    query_con_fecha = f"{query} when:1d"
    url = (
        f"https://news.google.com/rss/search?q={quote(query_con_fecha)}"
        f"&hl={idioma}&gl={pais}&ceid={pais}:{idioma}"
    )
    try:
        feed = feedparser.parse(url)
    except Exception as e:
        print(f"  [aviso] falló búsqueda Google News ({idioma}/{pais}) para '{query}': {e}")
        return []

    return [
        {
            "titulo": entry.title,
            "link": entry.link,
            "fuente": entry.get("source", {}).get("title", "desconocida"),
        }
        for entry in feed.entries[:MAX_FUENTES_A_BUSCAR]
    ]


def buscar_portales_relacionados(titulo_original, idioma="en", pais="US"):
    """Busca la misma noticia en múltiples medios vía Google News RSS,
    limitado a publicaciones del último día.

    Por defecto busca en la edición en/US porque las fuentes semilla
    (TechCrunch, The Verge, Ars Technica, HN) son medios en inglés: buscar
    en la edición es/AR devuelve prácticamente 0 resultados para ese tipo
    de cobertura. Si no aparece nada, reintenta con el título completo
    (sin simplificar) antes de rendirse.
    """
    query = _simplificar_query(titulo_original)

    resultados = _consultar_google_news(query, idioma, pais)
    if resultados:
        return resultados

    # fallback: probar con el título completo, tal cual, por si la
    # simplificación quitó justo el término que sí matchea
    resultados = _consultar_google_news(titulo_original, idioma, pais)
    return resultados


def resolver_url_real(google_news_url):
    """Los links de Google News RSS son redirects; esto devuelve la URL final."""
    try:
        r = requests.get(
            google_news_url,
            allow_redirects=True,
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0"},
        )
        return r.url
    except Exception:
        return google_news_url
