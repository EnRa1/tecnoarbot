"""
Recolección de tópicos y búsqueda de portales relacionados.
"""
import time
from datetime import datetime, timezone, timedelta
from urllib.parse import quote

import feedparser
import requests

from config import FEEDS_SEMILLA, VENTANA_HORAS, MAX_FUENTES_A_BUSCAR


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


def buscar_portales_relacionados(query, idioma="es", pais="AR"):
    """Busca la misma noticia en múltiples medios vía Google News RSS,
    limitado a publicaciones del último día."""
    query_con_fecha = f"{query} when:1d"
    url = (
        f"https://news.google.com/rss/search?q={quote(query_con_fecha)}"
        f"&hl={idioma}&gl={pais}&ceid={pais}:{idioma}"
    )
    try:
        feed = feedparser.parse(url)
    except Exception as e:
        print(f"  [aviso] falló búsqueda Google News para '{query}': {e}")
        return []

    resultados = []
    for entry in feed.entries[:MAX_FUENTES_A_BUSCAR]:
        resultados.append({
            "titulo": entry.title,
            "link": entry.link,
            "fuente": entry.get("source", {}).get("title", "desconocida"),
        })
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
