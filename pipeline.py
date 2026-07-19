"""
Pipeline principal — recolector y redactor automático de noticias tecno.ar
Corré con: python pipeline.py
Requiere la variable de entorno GEMINI_API_KEY.
"""
import time

from config import MAX_TOPICOS_POR_CORRIDA, MIN_FUENTES_POR_NOTICIA
from recoleccion import recolectar_topicos_semilla, buscar_portales_relacionados, resolver_url_real
from extraccion import extraer_articulo_completo, fecha_articulo_valida, truncar_articulo
from analisis import (
    cargar_historial, guardar_historial, elegir_topicos,
    filtrar_fuentes_relevantes, extraer_palabra_clave,
)
from enlaces_internos import cargar_enlaces_internos, formatear_enlaces_para_prompt, registrar_enlace_interno
from prompt import armar_prompt
from redaccion import redactar_con_reintentos
from guardado import guardar_nota_markdown
from datetime import datetime


def procesar_topico(topico, historial):
    print(f"\n→ Tópico: {topico['titulo']}")

    # 1. buscar cobertura en otros portales (últimas 24hs).
    #    internamente simplifica el título a términos clave antes de buscar,
    #    y hace fallback a en/US si la edición local no trae resultados.
    relacionados = buscar_portales_relacionados(topico["titulo"])
    time.sleep(1.5)  # cortesía con Google News

    if not relacionados:
        print("  descartado: sin cobertura adicional encontrada")
        return None

    # 2. extraer texto completo de cada portal
    articulos_completos = []
    for r in relacionados:
        url_real = resolver_url_real(r["link"])
        extraido = extraer_articulo_completo(url_real)
        time.sleep(1)  # cortesía con el sitio origen

        if not extraido:
            continue
        if not fecha_articulo_valida(extraido["fecha"]):
            print(f"  descartado por antigüedad: {r['fuente']}")
            continue

        articulos_completos.append({
            "fuente": r["fuente"],
            "url": url_real,
            "texto": truncar_articulo(extraido["texto"], max_palabras=600),
        })

    # 3. confirmar que realmente hablan del mismo hecho
    articulos_completos = filtrar_fuentes_relevantes(topico["titulo"], articulos_completos)

    if len(articulos_completos) < MIN_FUENTES_POR_NOTICIA:
        print(f"  descartado: solo {len(articulos_completos)} fuente(s) válida(s) (mínimo {MIN_FUENTES_POR_NOTICIA})")
        return None

    print(f"  {len(articulos_completos)} fuentes confirmadas: "
          f"{', '.join(a['fuente'] for a in articulos_completos)}")

    # 4. palabra clave
    keyword = extraer_palabra_clave(topico["titulo"], articulos_completos)
    print(f"  keyword: {keyword}")

    # 5. enlaces internos disponibles para este tema
    enlaces_internos = cargar_enlaces_internos(tema_keyword=keyword)
    enlaces_fmt = formatear_enlaces_para_prompt(enlaces_internos)

    # 6. armar prompt y redactar con Gemini (con validación + reintento)
    prompt_final = armar_prompt(keyword, articulos_completos, enlaces_fmt)
    nota = redactar_con_reintentos(prompt_final, keyword, enlaces_internos)

    if nota.get("descartada"):
        print(f"  descartado por el modelo: {nota['razon']}")
        return None

    # 7. guardar como Markdown
    archivo = guardar_nota_markdown(nota, keyword)
    print(f"  ✓ guardado en {archivo}")

    # 8. actualizar historial y registrar como enlace interno futuro
    historial.append({"titulo": topico["titulo"], "fecha": datetime.now().isoformat()})
    registrar_enlace_interno(nota["titulo"], f"https://tecno.ar/{archivo.split('/')[-1].replace('.md', '')}", keyword)

    return archivo


def correr_pipeline():
    print(f"=== Corrida iniciada: {datetime.now().isoformat()} ===")

    historial = cargar_historial()
    candidatos = recolectar_topicos_semilla()
    print(f"Candidatos recolectados (últimas 24hs): {len(candidatos)}")

    topicos = elegir_topicos(candidatos, historial, cantidad=MAX_TOPICOS_POR_CORRIDA)
    print(f"Tópicos seleccionados tras deduplicar: {len(topicos)}")

    notas_generadas = []
    for topico in topicos:
        try:
            resultado = procesar_topico(topico, historial)
            if resultado:
                notas_generadas.append(resultado)
            time.sleep(2)  # espaciar llamadas al LLM
        except Exception as e:
            print(f"  [error] falló el procesamiento de '{topico['titulo']}': {e}")
            continue

    guardar_historial(historial)

    print(f"\n=== Corrida finalizada: {len(notas_generadas)} notas generadas ===")
    for n in notas_generadas:
        print(f"  - {n}")

    return notas_generadas


if __name__ == "__main__":
    correr_pipeline()
