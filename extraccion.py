"""
Extracción del texto completo de cada portal + validación de antigüedad.
"""
import json
from datetime import datetime, timezone, timedelta

import trafilatura

from config import VENTANA_HORAS, MIN_CHARS_ARTICULO_VALIDO


def extraer_articulo_completo(url):
    """Devuelve {'texto': str, 'fecha': str|None} o None si falla la extracción."""
    try:
        descargado = trafilatura.fetch_url(url)
        if not descargado:
            return None

        resultado_json = trafilatura.extract(
            descargado,
            include_comments=False,
            include_tables=False,
            favor_precision=True,
            with_metadata=True,
            output_format="json",
        )
        if not resultado_json:
            return None

        data = json.loads(resultado_json)
        texto = data.get("text", "") or ""
        if len(texto) < MIN_CHARS_ARTICULO_VALIDO:
            return None

        return {"texto": texto, "fecha": data.get("date")}
    except Exception as e:
        print(f"  [aviso] no se pudo extraer {url}: {e}")
        return None


def fecha_articulo_valida(fecha_str, horas=VENTANA_HORAS):
    """trafilatura suele extraer solo el día (no la hora exacta), por eso
    se da un margen extra de 24hs para no descartar por error."""
    if not fecha_str:
        return True  # sin metadata de fecha, no descartamos solo por eso
    try:
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        limite = datetime.now(timezone.utc) - timedelta(hours=horas + 24)
        return fecha >= limite
    except ValueError:
        return True


def truncar_articulo(texto, max_palabras=600):
    """Recorta artículos muy largos para no comer el presupuesto de tokens."""
    palabras = texto.split()
    return " ".join(palabras[:max_palabras])
