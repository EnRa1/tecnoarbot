"""
Llamada al modelo Gemini, parseo de la respuesta y validaciones
(longitud, densidad de keyword, ubicación de enlaces) con reintento.
"""
import os
import re
import time

from google import genai

from config import (
    GEMINI_MODEL, PALABRAS_MIN, PALABRAS_MAX,
    DENSIDAD_KEYWORD_MIN, DENSIDAD_KEYWORD_MAX,
    MIN_ENLACES, MAX_ENLACES, MAX_REINTENTOS_REDACCION,
)

_client = None


def _get_client():
    global _client
    if _client is None:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("Falta la variable de entorno GEMINI_API_KEY")
        _client = genai.Client(api_key=api_key)
    return _client


def llamar_gemini(prompt, reintentos_red=3):
    """Llamada con backoff simple ante 429 / errores transitorios."""
    client = _get_client()
    ultimo_error = None
    for intento in range(reintentos_red):
        try:
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
            )
            return response.text
        except Exception as e:
            ultimo_error = e
            espera = 5 * (intento + 1)
            print(f"  [aviso] error llamando a Gemini ({e}), reintentando en {espera}s")
            time.sleep(espera)
    raise RuntimeError(f"Gemini falló tras {reintentos_red} intentos: {ultimo_error}")


# ---------- Parseo del XML de salida ----------

def _extraer_tag(texto, tag):
    m = re.search(fr"<{tag}>(.*?)</{tag}>", texto, re.DOTALL)
    return m.group(1).strip() if m else ""


def parsear_respuesta(texto):
    if "<descartar" in texto:
        m = re.search(r'razon="([^"]*)"', texto)
        return {"descartada": True, "razon": m.group(1) if m else "sin especificar"}

    return {
        "descartada": False,
        "titulo": _extraer_tag(texto, "titulo"),
        "bajada": _extraer_tag(texto, "bajada"),
        "cuerpo": _extraer_tag(texto, "cuerpo"),
        "fuentes": _extraer_tag(texto, "fuentes"),
        "enlaces_usados": _extraer_tag(texto, "enlaces_usados"),
    }


# ---------- Validaciones ----------

def calcular_densidad_keyword(cuerpo, keyword):
    palabras_totales = len(cuerpo.split()) or 1
    ocurrencias = len(re.findall(re.escape(keyword.lower()), cuerpo.lower()))
    densidad = (ocurrencias / palabras_totales) * 100
    return densidad, ocurrencias, palabras_totales


def validar_longitud_y_densidad(cuerpo, keyword):
    problemas = []
    densidad, ocurr, total = calcular_densidad_keyword(cuerpo, keyword)

    if not (PALABRAS_MIN <= total <= PALABRAS_MAX):
        problemas.append(f"longitud fuera de rango: {total} palabras (debe ser {PALABRAS_MIN}-{PALABRAS_MAX})")
    if not (DENSIDAD_KEYWORD_MIN <= densidad <= DENSIDAD_KEYWORD_MAX):
        problemas.append(f"densidad de keyword fuera de rango: {densidad:.2f}% (debe ser {DENSIDAD_KEYWORD_MIN}-{DENSIDAD_KEYWORD_MAX}%)")
    return problemas


def validar_enlaces(cuerpo):
    problemas = []

    for linea in cuerpo.split("\n"):
        if linea.strip().startswith("##") and re.search(r"\[.+?\]\(.+?\)", linea):
            problemas.append("hay un enlace dentro de un subtítulo H2")

    total_chars = len(cuerpo) or 1
    enlaces = re.findall(r"\[.+?\]\((https?://[^\)]+)\)", cuerpo)

    for match in re.finditer(r"\[.+?\]\((https?://[^\)]+)\)", cuerpo):
        posicion = match.start() / total_chars
        if posicion < 0.66:
            problemas.append(f"enlace fuera del último tercio (posición {posicion:.0%})")

    if not (MIN_ENLACES <= len(enlaces) <= MAX_ENLACES):
        problemas.append(f"cantidad de enlaces fuera de rango: {len(enlaces)} (debe ser {MIN_ENLACES}-{MAX_ENLACES})")

    parrafos = [p for p in cuerpo.split("\n\n") if p.strip()]
    for p in parrafos:
        if len(re.findall(r"\[.+?\]\(https?://[^\)]+\)", p)) > 1:
            problemas.append("hay un párrafo con más de un enlace")

    if len(enlaces) != len(set(enlaces)):
        problemas.append("hay una URL enlazada más de una vez")

    return problemas


def validar_nota_completa(cuerpo, keyword):
    return validar_longitud_y_densidad(cuerpo, keyword) + validar_enlaces(cuerpo)


# ---------- Fallback de inserción manual de enlaces ----------

def insertar_enlaces_fallback(cuerpo, keyword, enlaces_disponibles, max_enlaces=3):
    """Red de seguridad: si el modelo no linkeó bien tras los reintentos,
    insertamos manualmente sobre las últimas apariciones de la keyword."""
    if not enlaces_disponibles:
        return cuerpo

    patron = re.compile(re.escape(keyword), re.IGNORECASE)
    matches = list(patron.finditer(cuerpo))

    matches_validos = []
    for m in matches:
        inicio_linea = cuerpo.rfind("\n", 0, m.start()) + 1
        fin_linea = cuerpo.find("\n", m.start())
        linea = cuerpo[inicio_linea: fin_linea if fin_linea != -1 else None]
        if not linea.strip().startswith("##"):
            matches_validos.append(m)

    if not matches_validos:
        return cuerpo  # la keyword no aparece fuera de subtítulos, no se puede enlazar

    ultimas = [m for m in matches_validos if m.start() / len(cuerpo) >= 0.66]
    if not ultimas:
        ultimas = matches_validos[-max_enlaces:]

    cuerpo_editado = cuerpo
    offset = 0
    ya_usadas = set()
    for m, enlace in zip(ultimas[:max_enlaces], enlaces_disponibles[:max_enlaces]):
        if enlace["url"] in ya_usadas:
            continue
        original = m.group(0)
        reemplazo = f"[{original}]({enlace['url']})"
        pos = m.start() + offset
        cuerpo_editado = cuerpo_editado[:pos] + reemplazo + cuerpo_editado[pos + len(original):]
        offset += len(reemplazo) - len(original)
        ya_usadas.add(enlace["url"])

    return cuerpo_editado


# ---------- Orquestador con reintentos ----------

def redactar_con_reintentos(prompt_base, keyword, enlaces_internos, max_intentos=MAX_REINTENTOS_REDACCION):
    prompt_actual = prompt_base

    for intento in range(max_intentos + 1):
        texto_respuesta = llamar_gemini(prompt_actual)
        parsed = parsear_respuesta(texto_respuesta)

        if parsed["descartada"]:
            return parsed

        problemas = validar_nota_completa(parsed["cuerpo"], keyword)
        if not problemas:
            return parsed

        print(f"  [reintento {intento+1}] problemas detectados: {problemas}")
        prompt_actual = (
            prompt_base
            + f"\n\nTU RESPUESTA ANTERIOR TENÍA ESTOS PROBLEMAS: {', '.join(problemas)}. "
              f"Corregilo manteniendo el resto de la nota igual y reenviá la nota "
              f"completa respetando el formato de salida pedido."
        )

    # último recurso: fallback determinístico de enlaces si ese fue el problema
    problemas_finales = validar_nota_completa(parsed["cuerpo"], keyword)
    if any("enlace" in p for p in problemas_finales):
        parsed["cuerpo"] = insertar_enlaces_fallback(parsed["cuerpo"], keyword, enlaces_internos)
        print("  [fallback] se insertaron enlaces manualmente")

    return parsed
