import os
from consultas import (
    cargar_paises_desde_csv, guardar_paises_en_csv,
    agregar_pais, actualizar_pais, buscar_paises,
    filtrar_por_continente, filtrar_por_rango_poblacion,
    filtrar_por_rango_superficie, ordenar_paises, estadisticas_basicas
)
from utilidades import normalizar_str, ruta_absoluta_relativa


CSV_BASE = ruta_absoluta_relativa('dataset.csv')


def _input_int(msg: str) -> int:
    while True:
        x = input(msg).strip()
        if x.isdigit():
            return int(x)
        print("error: ingresa un numero entero.")

def menu ():
        print("---------------------------")
        print("/ MENU DE OPCIONES /")
        print("---------------------------")
        print("1 -> Agregar pais")
        print("2 -> Actualizar pais")
        print("3 -> Buscar paises")
        print("4 -> Filtrar por continente")
        print("5 -> Filtrar por rango de poblacion")
        print("6 -> Filtrar por rango de superficie")
        print("7 -> Ordenar paises")
        print("8 -> Estadisticas basicas")
        print("9 -> Salir")
        print("---------------------------")
    

def menu_principal():
    CSV_PATH = os.path.join(os.path.dirname(__file__), "dataset.csv")


    paises, errores = cargar_paises_desde_csv(CSV_PATH)

    if paises and not isinstance(paises[0], dict):
        paises = [
            {
                "nombre": str(p[0]).strip(),
                "poblacion": int(p[1]),
                "superficie": int(p[2]),
                "continente": str(p[3]).strip(),
            }
            for p in paises
        ]
    menu()



    while True:
        
        opcion = input("Ingrese una opcion (1-9): ").strip()
        
        if not opcion.isdigit():
            print("Error... Debe ingresar un numero del 1 al 9.")
            continue
        
        opcion = int(opcion)
        
        if opcion == 9:
            print("Saliendo del programa...")
            break
        
        match opcion:
            case 1:
                print("=== AGREGAR PAIS ===")


                # pedir y limpiar nombre
                nombre = input("ingrese el nombre del pais: ").strip().lower()
                if nombre == "":
                    print("error: el nombre no puede estar vacio.")
                    continue
                
                # verificar si ya existe
                existe = False
                for p in paises:
                    if p["nombre"].lower() == nombre:
                        existe = True
                        break
                if existe:
                    print("el pais ya existe en la lista.")
                    continue
                
                # pedir numeros (enteros >= 1)
                poblacion = _input_int("ingrese la poblacion: ")
                superficie = _input_int("ingrese la superficie: ")

                # pedir continente
                continente = input("ingrese el continente: ").strip().lower()
                if continente == "":
                    print("error: el continente no puede estar vacio.")
                    continue
                
                # armar dict y agregar
                nuevo_pais = {
                    "nombre": nombre,
                    "poblacion": poblacion,
                    "superficie": superficie,
                    "continente": continente
                }

                ok, msg = agregar_pais(paises, nuevo_pais)
                print(msg)

                if ok:
                    if guardar_paises_en_csv(CSV_BASE, paises):
                        print("csv guardado correctamente.")
                    else:
                        print("no se pudo guardar el csv.")
                        
    
            case 2:
                print("=== ACTUALIZAR PAIS ===")

                # pedir nombre exacto del pais a actualizar
                nombre = input("ingrese el nombre del pais: ").strip().lower()
                if nombre == "":
                    print("error: el nombre no puede estar vacio.")
                    continue

                # buscar el pais en la lista
                encontrado = False
                pais_actual = None
                for p in paises:
                    if p["nombre"].lower() == nombre:
                        encontrado = True
                        pais_actual = p
                        break

                if not encontrado:
                    print("no existe un pais con ese nombre.")
                    continue

                # mostrar datos actuales como referencia
                print(f"datos actuales -> poblacion: {pais_actual['poblacion']} | superficie: {pais_actual['superficie']}")

                # pedir nuevos valores (enteros > 0)
                nueva_pob = _input_int("nueva poblacion: ")
                nueva_sup = _input_int("nueva superficie: ")

                # aplicar actualizacion usando consultas.py
                ok, msg = actualizar_pais(paises, nombre, nueva_pob, nueva_sup)
                print(msg)

                # si se actualizo, guardar csv
                if ok:
                    if guardar_paises_en_csv(CSV_BASE, paises):
                        print("csv guardado correctamente.")
                    else:
                        print("no se pudo guardar el csv.")
                        
            case 3:
                print("=== BUSCAR PAISES ===")

                # pedir término de búsqueda
                termino = input("Ingrese parte o todo el nombre del pais a buscar: ").strip().lower()
                if termino == "":
                    print("Error: el término no puede estar vacío.")
                    continue

                # llamar a la función de consultas
                resultados = buscar_paises(paises, termino)

                # si no se encontró nada
                if not resultados:
                    print("No se encontraron países que coincidan con la búsqueda.")
                    continue

                # mostrar resultados
                print(f"Se encontraron {len(resultados)} país(es):")
                for p in resultados:
                    print(f"- {p['nombre'].title()} | Población: {p['poblacion']} | Superficie: {p['superficie']} | Continente: {p['continente']}")


            case 4:
                print("=== FILTRAR POR CONTINENTE ===")

                # pedir continente
                continente = input("ingrese el continente: ").strip().lower()
                if continente == "":
                    print("error: el continente no puede estar vacio.")
                    continue

                # consultar
                resultados = filtrar_por_continente(paises, continente)

                # sin resultados
                if not resultados:
                    print("no hay paises para ese continente.")
                    continue

                # mostrar
                print(f"se encontraron {len(resultados)} pais(es) en '{continente}':")
                for p in resultados:
                    print(f"- {p['nombre'].title()} | poblacion: {p['poblacion']} | superficie: {p['superficie']} | cont: {p['continente']}")

            case 5:
                print("=== FILTRAR POR RANGO DE POBLACION ===")

                # pedir rango minimo
                min_p = _input_int("ingrese el minimo de poblacion: ")
                # pedir rango maximo
                max_p = _input_int("ingrese el maximo de poblacion: ")

                # validar que el max sea mayor o igual al min
                if max_p < min_p:
                    print("error: el maximo no puede ser menor que el minimo.")
                    continue

                # llamar a la funcion del modulo consultas
                resultados = filtrar_por_rango_poblacion(paises, min_p, max_p)

                # si no devuelve nada
                if not resultados:
                    print("no hay paises dentro del rango indicado.")
                    continue

                # mostrar los paises encontrados
                print(f"se encontraron {len(resultados)} pais(es) entre {min_p} y {max_p} habitantes:")
                for p in resultados:
                    print(f"- {p['nombre'].title()} | poblacion: {p['poblacion']} | superficie: {p['superficie']} | continente: {p['continente']}")

            case 6:
                print("=== FILTRAR POR RANGO DE SUPERFICIE ===")

                # pedir rango minimo
                min_s = _input_int("ingrese la superficie minima (km²): ")
                # pedir rango maximo
                max_s = _input_int("ingrese la superficie maxima (km²): ")

                # validar que el maximo no sea menor que el minimo
                if max_s < min_s:
                    print("error: la superficie maxima no puede ser menor que la minima.")
                    continue

                # llamar a la funcion de consultas
                resultados = filtrar_por_rango_superficie(paises, min_s, max_s)

                # si no hay resultados
                if not resultados:
                    print("no se encontraron paises dentro del rango indicado.")
                    continue

                # mostrar resultados
                print(f"se encontraron {len(resultados)} pais(es) con superficie entre {min_s} y {max_s} km²:")
                for p in resultados:
                    print(f"- {p['nombre'].title()} | poblacion: {p['poblacion']} | superficie: {p['superficie']} | continente: {p['continente']}")
                    

            case 7:
                print("=== ORDENAR PAISES ===")

                # pedir criterio de ordenamiento
                print("1 -> Nombre")
                print("2 -> Poblacion")
                print("3 -> Superficie")
                criterio = input("elegi el criterio de ordenamiento (1-3): ").strip()

                if criterio not in ("1", "2", "3"):
                    print("error: opcion invalida.")
                    continue

                # preguntar el tipo de orden
                orden = input("ordenar de forma descendente? (s/n): ").strip().lower()

                if orden == "s":
                    descendente = True
                else:
                    descendente = False

                # definir la clave de orden segun la opcion elegida
                if criterio == "1":
                    clave = "nombre"
                elif criterio == "2":
                    clave = "poblacion"
                else:
                    clave = "superficie"

                # ordenar llamando a la funcion del otro archivo
                lista_ordenada = ordenar_paises(paises, clave, descendente)

                # mostrar los resultados
                
                if descendente:
                    tipo_orden = "DESC"
                else:
                    tipo_orden = "ASC"
                    
                print(f"\nPAISES ORDENADOS POR {clave.upper()} {tipo_orden}")

                for p in lista_ordenada:
                    print(f"- {p['nombre'].title()} | poblacion: {p['poblacion']} | superficie: {p['superficie']} | continente: {p['continente']}")
                    

            case 7:
                print("=== ORDENAR PAISES ===")

                # mostrar opciones de criterio
                print("1 -> Nombre")
                print("2 -> Poblacion")
                print("3 -> Superficie")

                # pedir el criterio al usuario
                criterio = input("Elegí el criterio de ordenamiento (1-3): ").strip()

                # validar que la opcion sea correcta
                if criterio not in ("1", "2", "3"):
                    print("Error: opción inválida.")
                    continue

                # preguntar si quiere ordenar de forma descendente
                orden = input("¿Ordenar de forma descendente? (s/n): ").strip().lower()

                # decidir si el orden es descendente o ascendente
                if orden == "s":
                    descendente = True
                else:
                    descendente = False

                # definir la clave de orden segun la opcion elegida
                if criterio == "1":
                    clave = "nombre"
                elif criterio == "2":
                    clave = "poblacion"
                else:
                    clave = "superficie"

                # llamar a la funcion que ordena los paises
                lista_ordenada = ordenar_paises(paises, clave, descendente)

                # definir texto para mostrar si es ASC o DESC
                if descendente:
                    tipo_orden = "DESC"
                else:
                    tipo_orden = "ASC"

                # mostrar encabezado
                print()
                print("PAISES ORDENADOS POR", clave.upper(), tipo_orden)
                print()

                # recorrer y mostrar los paises ordenados
                for p in lista_ordenada:
                    print("- Nombre:", p["nombre"].title())
                    print("  Poblacion:", p["poblacion"])
                    print("  Superficie:", p["superficie"])
                    print("  Continente:", p["continente"])
                    print("---------------------------")


            case 8:
                print("=== ESTADISTICAS BASICAS ===")
                stats = estadisticas_basicas(paises)

                print("Total de paises:", len(paises))
                print("Promedio de poblacion:", stats["promedio_poblacion"])
                print("Promedio de superficie:", stats["promedio_superficie"])

                mayor = stats["mayor_poblacion"]
                menor = stats["menor_poblacion"]

                print("País con mayor población:", mayor["nombre"], "-", mayor["poblacion"])
                print("País con menor población:", menor["nombre"], "-", menor["poblacion"])

                print("Cantidad por continente:")
                for continente, cantidad in stats["cantidad_por_continente"].items():
                    print(" ", continente, ":", cantidad)




if __name__ == "__main__":
    menu_principal()

