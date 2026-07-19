"""
Manejo del inventario de enlaces internos de tecno.ar.
"""
import json
from pathlib import Path

from config import ENLACES_INTERNOS_PATH, ENLACES_INTERNOS_A_OFRECER


def cargar_enlaces_internos(tema_keyword=None, cantidad=ENLACES_INTERNOS_A_OFRECER):
    path = Path(ENLACES_INTERNOS_PATH)
    if not path.exists():
        return []

    todos = json.loads(path.read_text(encoding="utf-8"))

    if tema_keyword:
        relevantes = [
            e for e in todos
            if tema_keyword.lower() in e.get("tema", "").lower()
            or tema_keyword.lower() in e.get("titulo", "").lower()
        ]
        if len(relevantes) >= 3:
            return relevantes[:cantidad]

    # fallback: los más recientes en general (se asume orden de más nuevo a más viejo)
    return todos[:cantidad]


def registrar_enlace_interno(titulo, url, tema):
    path = Path(ENLACES_INTERNOS_PATH)
    todos = json.loads(path.read_text(encoding="utf-8")) if path.exists() else []

    todos.insert(0, {"titulo": titulo, "url": url, "tema": tema})
    todos = todos[:200]  # mantener el archivo acotado

    path.write_text(json.dumps(todos, indent=2, ensure_ascii=False), encoding="utf-8")


def formatear_enlaces_para_prompt(enlaces):
    if not enlaces:
        return "(no hay enlaces internos disponibles todavía, no incluyas enlaces internos en esta nota)"
    return "\n".join(f"- {e['titulo']} → {e['url']}" for e in enlaces)
