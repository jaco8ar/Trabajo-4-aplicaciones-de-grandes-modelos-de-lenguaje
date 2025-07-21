import re
from fpdf import FPDF
from io import BytesIO

import unicodedata

def limpiar_unicode(texto):
    """
    Retira elementos que no son soportados en la construcción del PDF
    """

    return ''.join(c for c in texto if ord(c) < 256)

def contar_palabras(texto: str) -> int:
    """
    Cuenta las palabras en un texto después de limpiarlo:
    - Elimina signos de puntuación como comas, puntos, guiones, etc.
    - Elimina múltiples espacios y espacios al inicio/final.
    - Preserva letras con tildes y caracteres especiales como 'ñ'.

    Parámetros:
        texto (str): Texto del cual se quieren contar las palabras.

    Retorna:
        int: Número total de palabras limpias.
    """
    texto_limpio = re.sub(r"[.,!?;:\-\"\'()\[\]{}]", "", texto)
    texto_limpio = re.sub(r"\s+", " ", texto_limpio).strip()
    palabras = texto_limpio.split()
    return len(palabras)


def construir_contexto(datos_entrada: dict) -> str:
    """
    Construye un contexto en formato de lista con los datos del formulario,
    para ser usado como parte del prompt que genera o refina la historia.

    Parámetros:
        datos_entrada (dict): Diccionario con los datos del formulario.

    Retorna:
        str: Texto contextual con formato limpio.
    """
    contexto = "Esta es la información base de la historia:\n"
    for clave, valor in datos_entrada.items():
        clave_limpia = clave.replace('_', ' ').capitalize()
        if isinstance(valor, str) and valor.strip() == "":
            valor = "No especificado"
        contexto += f"- {clave_limpia}: {valor}\n"
    return contexto.strip()


class PDF(FPDF):
    """
    Clase personalizada basada en FPDF para estructurar el PDF
    con cabeceras, títulos de sección y cuerpo de texto.
    """

    def header(self):
        """
        Dibuja el encabezado de cada página del PDF.
        """
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Agente de Historias", ln=True, align="C")

    def chapter_title(self, title):
        """
        Agrega un título de sección al PDF.

        Args:
            title (str): Título de la sección.
        """
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, title, ln=True)

    def chapter_body(self, text):
        """
        Agrega un bloque de texto al PDF con salto de línea automático.

        Args:
            text (str): Texto del cuerpo de la sección.
        """
        self.set_font("Arial", "", 12)
        self.multi_cell(0, 10, text)


def exportar_a_pdf(historia: str, datos: dict) -> BytesIO:
    """
    Genera un archivo PDF que contiene los datos de entrada y la historia generada.

    Args:
        historia (str): Texto de la historia generada.
        datos (dict): Diccionario con los parámetros usados para crear la historia.

    Returns:
        BytesIO: Objeto en memoria que contiene el PDF listo para descargar.
    """
    pdf = PDF()
    pdf.add_page()

    pdf.chapter_title("Parámetros utilizados:")
    for clave, valor in datos.items():
        if isinstance(valor, list):
            valor = ", ".join(valor)
        pdf.chapter_body(f"{clave.capitalize()}: {valor}")

    pdf.chapter_title("Historia Generada:")
    pdf.chapter_body(limpiar_unicode(historia.replace("…", "...")))

    buffer = BytesIO()
    buffer.write(pdf.output(dest="S").encode("latin-1"))
    buffer.seek(0)
    return buffer