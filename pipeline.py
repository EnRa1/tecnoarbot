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

    articulos_completos = []

    # 1. SIEMPRE extraemos primero el artículo original de la fuente semilla
    #    (el link del RSS que originó el tópico). Esto garantiza que nunca
    #    nos quedemos sin nota solo porque Google News no encontró más
    #    cobertura: como mínimo, redactamos con esta fuente.
    extraido_principal = extraer_articulo_completo(topico["link"])
    if extraido_principal and fecha_articulo_valida(extraido_principal["fecha"]):
        articulos_completos.append({
            "fuente": topico["fuente"],
            "url": topico["link"],
            "texto": truncar_articulo(extraido_principal["texto"], max_palabras=600),
        })
        print(f"  fuente semilla extraída: {topico['fuente']}")
    else:
        print(f"  [aviso] no se pudo extraer la fuente semilla ({topico['fuente']}), "
              f"se intentará seguir solo con portales relacionados si aparecen")

    # 2. buscamos portales relacionados como COMPLEMENTO (opcional, no bloqueante).
    #    internamente simplifica el título a términos clave antes de buscar,
    #    y hace fallback a en/US si la edición local no trae resultados.
    relacionados = buscar_portales_relacionados(topico["titulo"])
    time.sleep(1.5)  # cortesía con Google News
    print(f"  {len(relacionados)} portales adicionales encontrados vía Google News")

    fallos_extraccion = 0
    fallos_fecha = 0
    urls_ya_incluidas = {a["url"] for a in articulos_completos}

    for r in relacionados:
        url_real = resolver_url_real(r["link"])
        if url_real in urls_ya_incluidas:
            continue  # evita duplicar la fuente semilla si Google News la vuelve a traer

        extraido = extraer_articulo_completo(url_real)
        time.sleep(1)  # cortesía con el sitio origen

        if not extraido:
            fallos_extraccion += 1
            continue
        if not fecha_articulo_valida(extraido["fecha"]):
            fallos_fecha += 1
            continue

        articulos_completos.append({
            "fuente": r["fuente"],
            "url": url_real,
            "texto": truncar_articulo(extraido["texto"], max_palabras=600),
        })
        urls_ya_incluidas.add(url_real)

    print(f"  portales adicionales: {len(articulos_completos) - (1 if extraido_principal else 0)} sumados, "
          f"{fallos_extraccion} sin texto útil, {fallos_fecha} descartados por fecha")

    # 3. de los portales ADICIONALES (no de la fuente semilla, que ya sabemos
    #    que es la correcta por definición), confirmamos que hablan del mismo
    #    hecho para no mezclar ruido temático
    if len(articulos_completos) > 1:
        principal = articulos_completos[0]
        adicionales_filtrados = filtrar_fuentes_relevantes(topico["titulo"], articulos_completos[1:])
        descartados = len(articulos_completos) - 1 - len(adicionales_filtrados)
        if descartados:
            print(f"  clustering: {descartados} portal(es) descartado(s) por no parecer la misma noticia")
        articulos_completos = [principal] + adicionales_filtrados

    if len(articulos_completos) < MIN_FUENTES_POR_NOTICIA:
        print(f"  descartado: no se logró extraer ninguna fuente utilizable")
        return None

    print(f"  redactando con {len(articulos_completos)} fuente(s): "
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
