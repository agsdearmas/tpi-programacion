import os


def es_entero_valido(valor: str) -> bool:
    """Valida que 'valor' represente un entero no negativo."""
    if valor is None:
        return False
    valor = valor.strip()
    if valor == '':
        return False
    if valor.startswith('-'):
        return False
    return valor.isdigit()

def normalizar_str(s: str) -> str:
    """Normaliza strings eliminando espacios y capitalizando nombre."""
    if s is None:
        return ''
    return s.strip()

def ruta_absoluta_relativa(archivo_relativo: str) -> str:
    """Devuelve ruta absoluta partiendo del modulo actual."""
    base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, archivo_relativo)