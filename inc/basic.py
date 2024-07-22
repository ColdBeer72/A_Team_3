from pathlib import Path

def read_markdown_file(markdown_file):
    """Devuelve el contenido de un archivo MarkDown.

    Args:
        markdown_file (string): Ruta y nombre del Archivo

    Returns:
        mdtext: Devuelve el contenido del archivo
    """
    return Path(markdown_file).read_text()

def prueba_vacia():
    pass