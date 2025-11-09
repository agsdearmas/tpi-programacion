import os
from consultas import (
    cargar_paises_desde_csv, guardar_paises_en_csv,
    agregar_pais, actualizar_pais, buscar_paises,
    filtrar_por_continente, filtrar_por_rango_poblacion,
    filtrar_por_rango_superficie, ordenar_paises, estadisticas_basicas
)
from utilidades import ruta_absoluta_relativa, _input_int

CSV_PATH = ruta_absoluta_relativa('dataset.csv')


def menu ():
        print("---------------------------")
        print("/ MENU DE OPCIONES /")
        print("---------------------------")
        print("1 -> Agregar pais")
        print("2 -> Actualizar pais")
        print("3 -> Buscar paises")
        print("4 -> Elegir tipo de filtro")
        print("5 -> Ordenar paises")
        print("6 -> Estadisticas basicas")
        print("7 -> Salir")
        print("---------------------------")


def manejador_de_filtros(filtro: str, paises: list) -> list:
    filtro = filtro.lower()
    error = None

    if filtro == "continente":
        print("=== FILTRAR POR CONTINENTE ===")
        continente = input("> Ingrese el continente: ").strip().lower()

        if continente == "":
            error = "Error: El continente no puede estar vacio.\n"
            return [], error

        resultados = filtrar_por_continente(paises, continente)
        if not resultados:
            error = "Error: No hay paises para ese continente.\n"
            return [], error
        return resultados, error

    elif filtro == "poblacion":
        print("=== FILTRAR POR RANGO DE POBLACION ===")
        min_p = _input_int("> Ingrese el minimo de poblacion: ")
        max_p = _input_int("> Ingrese el maximo de poblacion: ")

        if max_p < min_p:
            error = "Error: El maximo de poblacion no puede ser menor que el minimo."
            return [], error

        resultados = filtrar_por_rango_poblacion(paises, min_p, max_p)
        if not resultados:
            error = "Error: No hay paises dentro del rango indicado.\n"
            return [], error
        return resultados, error

    elif filtro == "superficie":
        print("=== FILTRAR POR RANGO DE SUPERFICIE ===")
        min_s = _input_int("> Ingrese la superficie minima (km²): ")
        max_s = _input_int("> Ingrese la superficie maxima (km²): ")

        if max_s < min_s:
            error = "Error: La superficie maxima no puede ser menor que la minima."
            return [], error

        resultados = filtrar_por_rango_superficie(paises, min_s, max_s)
        if not resultados:
            error = "Error: No hay paises dentro del rango indicado.\n"
            return [], error
        return resultados, error
    
    else:
        error = f"Error: Filtro desconocido '{filtro}'."
        return [], error


def menu_principal():
    paises = cargar_paises_desde_csv(CSV_PATH)
    menu()

    while True:
        opcion = input("> Ingrese una opcion (1-7): ").strip()

        if not opcion.isdigit():
            print("Error: Debe ingresar un numero del 1 al 7.\n")
            continue

        opcion = int(opcion)

        if opcion == 7:
            print("Saliendo del programa...")
            break

        match opcion:
            case 1:
                print("=== AGREGAR PAIS ===")
                nombre = input("> Ingrese el nombre del pais: ").strip().lower()
                if nombre == "":
                    print("Error: El nombre no puede estar vacio.\n")
                    continue

                # Verificar si el pais ya existe en la lista
                existe = False
                for p in paises:
                    if p["nombre"].lower() == nombre:
                        existe = True
                        break
                if existe:
                    print("Error: El pais ya existe en la lista.\n")
                    continue

                # Pedir numeros enteros positivos y continente
                poblacion = _input_int("> Ingrese la poblacion: ")
                superficie = _input_int("> Ingrese la superficie: ")
                continente = input("> Ingrese el continente: ").strip().lower()

                if continente == "":
                    print("Error: El continente no puede estar vacio.")
                    continue

                nuevo_pais = {
                    "nombre": nombre,
                    "poblacion": poblacion,
                    "superficie": superficie,
                    "continente": continente
                }
                ok, msg = agregar_pais(paises, nuevo_pais)

                if ok:
                    if guardar_paises_en_csv(CSV_PATH, paises):
                        print("CSV guardado correctamente.\n")
                    else:
                        print("Error: No se pudo guardar el csv.\n")
                else:
                    print(msg)

            case 2:
                print("=== ACTUALIZAR PAIS ===")
                nombre = input("> Ingrese el nombre del pais: ").strip().lower()
                if nombre == "":
                    print("Error: El nombre no puede estar vacio.\n")
                    continue

                # Buscar el pais en la lista
                encontrado = False
                pais_actual = None
                for p in paises:
                    if p["nombre"].lower() == nombre:
                        encontrado = True
                        pais_actual = p
                        break

                if not encontrado:
                    print("Error: El pais no se encuentra en el registro.\n")
                    continue

                # Mostrar datos actuales como referencia
                print(f"datos actuales -> poblacion: {pais_actual['poblacion']} | superficie: {pais_actual['superficie']}")

                nueva_pob = _input_int("> Nueva poblacion: ")
                nueva_sup = _input_int("> Nueva superficie: ")
                ok, msg = actualizar_pais(paises, nombre, nueva_pob, nueva_sup)

                if ok:
                    if guardar_paises_en_csv(CSV_PATH, paises):
                        print("CSV guardado correctamente.\n")
                    else:
                        print("Error: No se pudo guardar el csv.\n")
                else:
                    print(msg)

            case 3:
                print("=== BUSCAR PAISES ===")
                termino = input("> Ingrese parte o todo el nombre del pais a buscar: ").strip().lower()
                if termino == "":
                    print("Error: El término no puede estar vacío.\n")
                    continue

                resultados = buscar_paises(paises, termino)

                if not resultados:
                    print("Error: No se encontraron países que coincidan con la búsqueda.\n")
                    continue

                print(f"Se encontraron {len(resultados)} país(es):")
                for p in resultados:
                    print(f"- {p['nombre'].title()} | Población: {p['poblacion']} | Superficie: {p['superficie']} | Continente: {p['continente']}")


            case 4:
                print("=== ELEGIR TIPO DE FILTRO ===")
                print("1. Continente")
                print("2. Rango de Población")
                print("3. Rango de Superficie")

                filtro_opcion = input("> Ingrese la opción de filtro (1-3): ").strip()

                match filtro_opcion:
                    case "1":
                        filtro_str = "continente"
                        tipo_filtro_display = "continente"
                    case "2":
                        filtro_str = "poblacion"
                        tipo_filtro_display = "población"
                    case "3":
                        filtro_str = "superficie"
                        tipo_filtro_display = "superficie"
                    case _:
                        print("Error: Opción de filtro no válida.\n")
                        continue

                # Llamar a la funcion manejadora con el filtro elegido
                resultados, error = manejador_de_filtros(filtro_str, paises)

                if not resultados:
                    print(error)
                    continue

                print(f"\nSe encontraron {len(resultados)} pais(es) para el filtro de {tipo_filtro_display}:")
                for p in resultados:
                    print(f"- {p['nombre'].title()} | Población: {p['poblacion']} | Superficie: {p['superficie']} | Continente: {p['continente']}")


            case 5:
                print("=== ORDENAR PAISES ===")
                # Pedir criterio de ordenamiento
                print("1 -> Nombre")
                print("2 -> Poblacion")
                print("3 -> Superficie")
                criterio = input("> Ingrese el criterio de ordenamiento (1-3): ").strip()

                if criterio not in ("1", "2", "3"):
                    print("Error: Opcion invalida.\n")
                    continue

                # Pedir el tipo de orden
                orden = input("> Desea ordenar de forma descendente? (S/N): ").strip().lower()

                if orden == "s":
                    descendente = True
                    tipo_orden = "DESC"
                else:
                    descendente = False
                    tipo_orden = "ASC"

                # Definir la clave de orden segun la opcion elegida
                if criterio == "1":
                    clave = "nombre"
                elif criterio == "2":
                    clave = "poblacion"
                else:
                    clave = "superficie"

                lista_ordenada = ordenar_paises(paises, clave, descendente)
                print(f"\nPaises ordenados por: {clave.upper()} {tipo_orden}")

                for p in lista_ordenada:
                    print(f"- {p['nombre'].title()} | Población: {p['poblacion']} | Superficie: {p['superficie']} | Continente: {p['continente']}")


            case 6:
                print("=== ESTADISTICAS BASICAS ===")
                stats = estadisticas_basicas(paises)

                print("Total de paises:", len(paises))
                print("Promedio de poblacion:", stats["promedio_poblacion"])
                print("Promedio de superficie:", stats["promedio_superficie"])

                mayor = stats["mayor_poblacion"]
                menor = stats["menor_poblacion"]

                print("País con mayor población:", mayor["nombre"], "-", mayor["poblacion"])
                print("País con menor población:", menor["nombre"], "-", menor["poblacion"])

                print("Cantidad de paises por continente:")
                for continente, cantidad in stats["cantidad_por_continente"].items():
                    print(" ", continente, ":", cantidad)


if __name__ == "__main__":
    menu_principal()
