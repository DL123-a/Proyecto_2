# Sistema de Recomendación de Usuarios

Este proyecto implementa un sistema de recomendación de usuarios utilizando una base de datos de grafos (Neo4j). El sistema genera sugerencias de perfiles basándose en intereses compartidos y conexiones dentro de la red social, permitiendo descubrir nuevos usuarios relevantes para seguir.

## Características

* Recomendación de usuarios basada en intereses en común.
* Recomendación basada en amigos en común.
* Sistema de puntuación para priorizar sugerencias relevantes.
* Explicación de las recomendaciones generadas.
* Gestión de usuarios, intereses y relaciones mediante una interfaz gráfica desarrollada con Streamlit.
* Persistencia de datos utilizando Neo4j.

## Estructura del Proyecto

* `db.py` → Conexión y operaciones sobre Neo4j.
* `recommendation.py` → Algoritmo de recomendación.
* `seed_data.py` → Generación y carga de datos iniciales.
* `Interfaz.py` → Interfaz gráfica desarrollada con Streamlit.
* `main.py` → Pruebas rápidas del sistema.
* `male.txt` → Dataset de nombres masculinos.
* `female.txt` → Dataset de nombres femeninos.
* `hobbies.csv` → Dataset de hobbies e intereses.

## Modelo de Datos

### Nodos

**Usuario**

* name
* username

**Interes**

* name

### Relaciones

* `(Usuario)-[:SIGUE]->(Usuario)`
* `(Usuario)-[:TIENE_INTERES]->(Interes)`

## Algoritmo de Recomendación

El sistema identifica usuarios con intereses compartidos y conexiones indirectas dentro del grafo.

Puntaje utilizado:

```text
(intereses_comunes × 2) + (amigos_en_comun × 3)
```

Los usuarios se ordenan según este puntaje y se muestran las mejores recomendaciones disponibles.

## Generación de Datos

La base de datos se genera automáticamente a partir de datasets reales de nombres e intereses.

Durante la generación:

* Se crean usuarios utilizando nombres reales.
* Se generan usernames únicos automáticamente.
* Se asignan intereses a cada usuario.
* Se crean comunidades basadas en intereses.
* Se generan relaciones sociales entre usuarios.
* Se favorecen conexiones dentro de las mismas comunidades para producir amigos en común y recomendaciones más relevantes.

## Tecnologías Utilizadas

* Python
* Neo4j
* Cypher
* Streamlit

## Ejecución

### 1. Iniciar Neo4j

Asegurarse de que la instancia de Neo4j se encuentre en ejecución.

### 2. Cargar la base de datos

```bash
python seed_data.py
```

### 3. Ejecutar la interfaz

```bash
streamlit run Interfaz.py
```

## Idea Principal

El proyecto combina dos enfoques ampliamente utilizados en sistemas de recomendación:

* Filtrado basado en contenido (intereses compartidos).
* Recomendación basada en grafos (amigos en común y relaciones sociales).

Esto permite generar recomendaciones más relevantes y personalizadas dentro de una red social.
