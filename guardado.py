"""
Guardado de las noticias redactadas como archivos Markdown.
"""
import re
import unicodedata
from datetime import datetime
from pathlib import Path

from config import OUTPUT_DIR


def _slugify(texto):
    texto = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    texto = re.sub(r"[^\w\s-]", "", texto.lower())
    return re.sub(r"[-\s]+", "-", texto).strip("-")[:60]


def guardar_nota_markdown(nota, keyword):
    Path(OUTPUT_DIR).mkdir(exist_ok=True)

    fecha = datetime.now().strftime("%Y-%m-%d")
    slug = _slugify(nota["titulo"])
    filename = f"{OUTPUT_DIR}/{fecha}-{slug}.md"

    frontmatter = (
        "---\n"
        f"titulo: \"{nota['titulo']}\"\n"
        f"fecha: {fecha}\n"
        f"keyword: {keyword}\n"
        "---\n\n"
    )

    contenido = (
        frontmatter
        + f"# {nota['titulo']}\n\n"
        + f"*{nota['bajada']}*\n\n"
        + nota["cuerpo"] + "\n\n"
        + "## Fuentes\n" + nota["fuentes"] + "\n"
    )

    Path(filename).write_text(contenido, encoding="utf-8")
    return filename
