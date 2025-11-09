# 🌍 TPI | Gestión de Datos de Países en Python

## Descripción del Programa

Este proyecto es el **Trabajo Práctico Integrador (TPI)** de la asignatura **Programación 1**.

Consiste en una aplicación de consola desarrollada en **Python** cuyo objetivo principal es la **gestión, consulta y análisis estadístico** de un *dataset* de países. El sistema utiliza una **Lista de Diccionarios** como estructura de datos central y está diseñado bajo el principio de **modularización** para separar la lógica de negocio de la interfaz de usuario.

### Funcionalidades Clave:

* **Persistencia:** Carga inicial de datos desde un archivo **CSV** y guardado automático de los cambios al salir.
* **Gestión de Registros (CRUD):** Permite **agregar** nuevos países y **actualizar** los datos de población, superficie o continente de los existentes.
* **Consultas:** Implementa **búsquedas por nombre** (parciales y no sensibles a mayúsculas/minúsculas) y **filtros** por Continente o por Rangos Numéricos (Población/Superficie).
* **Análisis:** Ofrece funciones avanzadas de **ordenamiento** por múltiples criterios y cálculo de **estadísticas básicas** (promedios, extremos y cantidad por continente).

---

## 🚀 Instrucciones de Uso

### Requisitos Previos

* **Python 3.x** (Versión 3.6 o superior).
* El archivo de datos **`dataset.csv`** debe estar presente en el mismo directorio raíz que los archivos Python, de no ser asi, se crea al iniciar el proyecto.

### Estructura del Proyecto

El código está organizado en tres módulos principales para separar responsabilidades:

| Archivo | Responsabilidad |
| :--- | :--- |
| **`main.py`** | Control de Flujo, Menú de opciones e Interacción con el usuario. |
| **`consultas.py`** | **Lógica de Negocio:** Implementación de todos los algoritmos de CRUD, Filtros, Ordenamiento y Estadísticas. |
| **`utilidades.py`** | **Funciones de Apoyo:** Validación de entradas numéricas (`_input_int`) y normalización de textos. |

### Ejecución del Programa

1.  **Navegación:** Abre tu terminal y navega hasta el directorio raíz del proyecto.
2.  **Inicio:** Ejecuta la aplicación usando el siguiente comando:

    ```bash
    python main.py
    ```
3.  **Interacción:** El sistema cargará los datos y presentará el menú. Las modificaciones se guardarán automáticamente al elegir la opción **7 (Salir)**.

---

## ⌨️ Ejemplos de Entradas y Salidas

El programa opera con el siguiente menú principal:
1 -> Agregar pais 2 -> Actualizar pais 3 -> Buscar paises 4 -> Elegir tipo de filtro 5 -> Ordenar paises 6 -> Estadisticas basicas 7 -> Salir

### Ejemplo 1: Opción 4 (Filtro por Rango Numérico)

Esta secuencia de entradas demuestra la validación de rango y la ejecución del filtro.

| Entrada del Usuario | Descripción | Salida (Extracto) |
| :--- | :--- | :--- |
| `4` | Elegir tipo de filtro. | `1 -> Por Continente | 2 -> Por Rango Numérico` |
| `2` | Elegir Rango Numérico. | `1 -> Por Poblacion | 2 -> Por Superficie` |
| `1` | Elegir Rango de Población. | `> Ingrese Poblacion MINIMA:` |
| `20000000` | Mínimo (20 millones) | `> Ingrese Poblacion MAXIMA:` |
| `50000000` | Máximo (50 millones) | `--- PAISES FILTRADOS ---` |
| | | `- Colombia | Población: 52000000 | ...` (Ejemplo) |
| | | `- España | Población: 47000000 | ...` (Ejemplo) |

### Ejemplo 2: Opción 6 (Estadísticas Básicas)

Esta opción genera un informe de resumen del *dataset*.

| Entrada del Usuario | Descripción | Salida (Completa) |
| :--- | :--- | :--- |
| `6` | Elegir Estadísticas Básicas. | `=== ESTADISTICAS BASICAS ===` |
| | | `Total de paises: [Cantidad]` |
| | | `Promedio de poblacion: [Valor Promedio]` |
| | | `Promedio de superficie: [Valor Promedio]` |
| | | `País con mayor población: [Nombre] - [Valor]` |
| | | `País con menor población: [Nombre] - [Valor]` |
| | | `Cantidad de paises por continente:` |
| | | `  America : [Cantidad]` |
| | | `  Asia : [Cantidad]` |
| | | `  Europa : [Cantidad]` |

---

## 🧑‍💻 Participación de los Integrantes

El proyecto fue desarrollado en colaboración por los siguientes integrantes:

| Integrante | Contribución Principal |
| :--- | :--- |
| **[De Armas Agustin]** | Diseño y desarrollo de la **Persistencia (CSV)**. Implementación de funciones **CRUD**. Diseño y desarrollo de los algoritmos de **Ordenamiento** (Múltiples Criterios) y **Estadísticas Básicas**.|
| **[Hugo Insaurralde]** | Implementación de la estructura del **`main.py`** y manejo de filtros. Implementación de módulo **`utilidades.py`** (Validaciones y Normalización). Diseño del control y manejo de errores.|

---