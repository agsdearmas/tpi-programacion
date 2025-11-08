import os
from utilidades import normalizar_str, es_entero_valido

CSV_HEADERS = ('nombre','poblacion','superficie','continente')

def cargar_paises_desde_csv(ruta_csv: str) -> tuple:
    """
    Lee el CSV y retorna (lista_paises, lista_errores).
    Cada pais es dict: {'nombre':str,'poblacion':int,'superficie':int,'continente':str}
    Si detecta una linea de encabezado, la ignora automaticamente.
    """
    paises = []
    errores = []

    if not os.path.exists(ruta_csv):
        errores.append(f'No existe archivo: {ruta_csv}')
        return paises, errores

    with open(ruta_csv, 'r', encoding='utf-8') as f:
        lineas = f.readlines()

    if not lineas:
        errores.append('Archivo vacío')
        return paises, errores

    # Verificar si la primera linea es un header
    primera = lineas[0].strip().lower()
    tiene_header = False
    if primera.replace(' ', '') in (
        'nombre,poblacion,superficie,continente',
        'nombre,población,superficie,continente'
    ):
        tiene_header = True

    # Si tiene header, saltamos esa linea al procesar
    inicio = 1 if tiene_header else 0

    for idx, raw in enumerate(lineas[inicio:], start=inicio + 1):
        linea = raw.strip()
        if linea == '':
            continue
        partes = [p.strip() for p in linea.split(',')]
        if len(partes) != 4:
            errores.append(f'Linea {idx}: cantidad de columnas != 4 -> "{linea}"')
            continue

        nombre, poblacion_s, superficie_s, continente = partes
        nombre = normalizar_str(nombre)
        continente = normalizar_str(continente)

        if not nombre:
            errores.append(f'Linea {idx}: nombre vacío -> "{linea}"')
            continue
        if not es_entero_valido(poblacion_s) or not es_entero_valido(superficie_s):
            errores.append(f'Linea {idx}: población/superficie no enteros -> "{linea}"')
            continue

        paises.append({
            'nombre': nombre,
            'poblacion': int(poblacion_s),
            'superficie': int(superficie_s),
            'continente': continente
        })

    return paises, errores


def guardar_paises_en_csv(ruta_csv: str, lista_paises: list) -> bool:
    """
    Sobrescribe CSV con lista_paises.
    Devuelve True si escritura OK, False si no se pudo (ej. ruta invalida).
    """

    carpeta = os.path.dirname(os.path.abspath(ruta_csv))
    if not os.path.isdir(carpeta):
        return False

    with open(ruta_csv, 'w', encoding='utf-8') as f:
        for p in lista_paises:
            nombre = p['nombre']
            pob = str(p['poblacion'])
            sup = str(p['superficie'])
            cont = p['continente']
            f.write(f'{nombre},{pob},{sup},{cont}\n')
    return True


def agregar_pais(lista_paises: list, pais: dict) -> tuple:
    """
    Agrega un pais a la lista en memoria si no existe por nombre exacto.
    Retorna (True, mensaje) o (False, mensaje_error).
    """
    nombre = pais.get('nombre','').strip()
    if not nombre:
        return False, 'El nombre no puede estar vacío.'

    for p in lista_paises:
        if p['nombre'].lower() == nombre.lower():
            return False, f'El país "{nombre}" ya existe.'

    if not isinstance(pais.get('poblacion'), int) or not isinstance(pais.get('superficie'), int):
        return False, 'Población y superficie deben ser enteros.'

    pais['continente'] = pais.get('continente','').strip()
    lista_paises.append({
        'nombre': nombre,
        'poblacion': pais['poblacion'],
        'superficie': pais['superficie'],
        'continente': pais['continente']
    })
    return True, f'País "{nombre}" agregado.'


def actualizar_pais(lista_paises: list, nombre_buscar: str, nueva_pob: int, nueva_sup: int) -> tuple:
    """
    Actualiza poblacion y superficie de primer pais que coincida exactamente por nombre.
    Retorna (True,msg) o (False,msg).
    """
    if not nombre_buscar:
        return False, 'Nombre de búsqueda vacío.'
    for p in lista_paises:
        if p['nombre'].lower() == nombre_buscar.lower():
            p['poblacion'] = nueva_pob
            p['superficie'] = nueva_sup
            return True, f'País "{p["nombre"]}" actualizado.'
    return False, f'País "{nombre_buscar}" no encontrado.'


def buscar_paises(lista_paises: list, termino: str) -> list:
    """
    Busqueda por nombre (coincidencia parcial).
    Retorna lista de paises que cumplan.
    """
    termino = (termino or '').strip().lower()
    if termino == '':
        return []
    resultado = []
    for p in lista_paises:
        if termino in p['nombre'].lower():
            resultado.append(p)
    return resultado


def filtrar_por_continente(lista_paises: list, continente: str) -> list:
    continente = (continente or '').strip().lower()
    if continente == '':
        return []
    return [p for p in lista_paises if p['continente'].lower() == continente]


def filtrar_por_rango_poblacion(lista_paises: list, min_p: int, max_p: int) -> list:
    return [p for p in lista_paises if p['poblacion'] >= min_p and p['poblacion'] <= max_p]


def filtrar_por_rango_superficie(lista_paises: list, min_s: int, max_s: int) -> list:
    return [p for p in lista_paises if p['superficie'] >= min_s and p['superficie'] <= max_s]


def ordenar_paises(lista_paises: list, clave: str, descendente: bool=False) -> list:
    """
    Ordena por 'nombre', 'poblacion' o 'superficie'.
    No modifica la lista original: retorna copia ordenada.
    """
    if clave not in ('nombre', 'poblacion', 'superficie'):
        return lista_paises[:]

    # Se definen funciones auxiliares como claves de ordenamiento
    def clave_nombre(pais):
        return pais['nombre'].lower()

    def clave_generica(pais):
        return pais[clave]

    if clave == 'nombre':
        return sorted(lista_paises, key=clave_nombre, reverse=descendente)
    else:
        return sorted(lista_paises, key=clave_generica, reverse=descendente)


def estadisticas_basicas(lista_paises: list) -> dict:
    """
    Devuelve dict con:
    - mayor_poblacion: pais (dict)
    - menor_poblacion: pais (dict)
    - promedio_poblacion: float
    - promedio_superficie: float
    - cantidad_por_continente: dict
    """
    res = {
        'mayor_poblacion': None,
        'menor_poblacion': None,
        'promedio_poblacion': 0.0,
        'promedio_superficie': 0.0,
        'cantidad_por_continente': {}
    }
    if not lista_paises:
        return res

    mayor = lista_paises[0]
    menor = lista_paises[0]
    suma_p = 0
    suma_s = 0
    contador = 0
    por_cont = {}
    for p in lista_paises:
        if p['poblacion'] > mayor['poblacion']:
            mayor = p
        if p['poblacion'] < menor['poblacion']:
            menor = p
        suma_p += p['poblacion']
        suma_s += p['superficie']
        contador += 1
        cont = p['continente']
        por_cont[cont] = por_cont.get(cont, 0) + 1

    res['mayor_poblacion'] = mayor
    res['menor_poblacion'] = menor
    res['promedio_poblacion'] = suma_p / contador
    res['promedio_superficie'] = suma_s / contador
    res['cantidad_por_continente'] = por_cont
    return res
