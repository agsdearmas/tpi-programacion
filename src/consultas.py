def cargar_paises_desde_csv(ruta_csv: str) -> tuple:
    """
    Lee el CSV y retorna (lista_paises, lista_errores).
    Cada país es dict: {'nombre':str,'poblacion':int,'superficie':int,'continente':str}
    Si detecta una línea de encabezado, la ignora automáticamente.
    """
    pass


def guardar_paises_en_csv(ruta_csv: str, lista_paises: list) -> bool:
    """
    Sobrescribe CSV con lista_paises.
    Devuelve True si escritura OK, False si no se pudo (p.ej. ruta inválida).
    """
    pass


def agregar_pais(lista_paises: list, pais: dict) -> tuple:
    """
    Agrega un país a la lista en memoria si no existe por nombre exacto.
    Retorna (True, mensaje) o (False, mensaje_error).
    No usa excepciones.
    """
    pass


def actualizar_pais(lista_paises: list, nombre_buscar: str, nueva_pob: int, nueva_sup: int) -> tuple:
    """
    Actualiza poblacion y superficie de primer país que coincida exactamente por nombre.
    Retorna (True,msg) o (False,msg).
    """
    pass


def buscar_paises(lista_paises: list, termino: str) -> list:
    """
    Búsqueda por nombre (coincidencia parcial, case-insensitive).
    Retorna lista de países que cumplan.
    """
    pass


def filtrar_por_continente(lista_paises: list, continente: str) -> list:
    pass


def filtrar_por_rango_poblacion(lista_paises: list, min_p: int, max_p: int) -> list:
    pass


def filtrar_por_rango_superficie(lista_paises: list, min_s: int, max_s: int) -> list:
    pass


def ordenar_paises(lista_paises: list, clave: str, descendente: bool=False) -> list:
    """
    Ordena por 'nombre','poblacion' o 'superficie'.
    No modifica la lista original: retorna copia ordenada.
    """
    pass


def estadisticas_basicas(lista_paises: list) -> dict:
    """
    Devuelve dict con:
    - mayor_poblacion: país (dict)
    - menor_poblacion: país (dict)
    - promedio_poblacion: float
    - promedio_superficie: float
    - cantidad_por_continente: dict
    """
    pass
