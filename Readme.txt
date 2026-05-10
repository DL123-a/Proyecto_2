# Sistema de Recomendación (Base)

Este proyecto utiliza una base de datos de grafos (Neo4j) para recomendar usuarios
basándose en:

- Intereses en común
- Amigos en común

## Estructura

- db.py → conexión a la base de datos
- recommendation.py → lógica del algoritmo
- main.py → pruebas

## Qué falta implementar

- Crear nodos de Usuario e Intereses
- Crear relaciones (SIGUE, TIENE_INTERES)
- Insertar datos reales
- Mejorar el algoritmo de recomendación
- Agregar explicación de recomendaciones

## Idea principal

Se busca combinar:
- Filtrado basado en contenido (intereses)
- Grafos (relaciones entre usuarios)

