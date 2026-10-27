# Prueba Técnica: Sistema de Votaciones

## Descripción del proyecto

Crear una **API RESTful** para gestionar un sistema de votaciones. El sistema debe:

- Manejar votantes y candidatos.
- Asegurar que cada votante pueda emitir **un único voto**.
- Proporcionar estadísticas sobre los resultados de la votación.

**Tiempo de entrega:** 1 día

---

## Requisitos técnicos

### 1. Lenguajes permitidos

Python, Java, Node.js o PHP.

### 2. Base de datos

- **SQL:** MySQL o PostgreSQL
- **NoSQL:** MongoDB

### 3. Modelo de datos

#### Voter (Votante)

| Campo       | Tipo     | Descripción                                   |
|-------------|----------|-----------------------------------------------|
| `id`        | ID       | Único, autogenerado                           |
| `name`      | string   | Nombre del votante (obligatorio)              |
| `email`     | string   | Correo electrónico único (obligatorio)        |
| `has_voted` | boolean  | Indica si ya votó (por defecto: `false`)      |

#### Candidate (Candidato)

| Campo   | Tipo    | Descripción                                  |
|---------|---------|----------------------------------------------|
| `id`    | ID      | Único, autogenerado                          |
| `name`  | string  | Nombre del candidato (obligatorio)           |
| `party` | string  | Partido político (opcional)                  |
| `votes` | integer | Número de votos recibidos (por defecto: `0`) |

#### Vote (Voto)

| Campo          | Tipo     | Descripción                          |
|----------------|----------|--------------------------------------|
| `id`           | ID       | Único, autogenerado                  |
| `voter_id`     | relación | ID del votante                       |
| `candidate_id` | relación | ID del candidato seleccionado        |

### 4. Restricciones

- Un votante **no puede** ser registrado como candidato, y viceversa.
- Cada votante puede emitir **un único voto**.
- Los votos deben contarse correctamente en las estadísticas.

---

## Endpoints

### Votantes

| Método   | Ruta            | Descripción                        |
|----------|-----------------|------------------------------------|
| `POST`   | `/voters`       | Registrar un nuevo votante         |
| `GET`    | `/voters`       | Obtener la lista de votantes       |
| `GET`    | `/voters/{id}`  | Obtener detalles de un votante     |
| `DELETE` | `/voters/{id}`  | Eliminar un votante                |

### Candidatos

| Método   | Ruta                | Descripción                        |
|----------|---------------------|------------------------------------|
| `POST`   | `/candidates`       | Registrar un nuevo candidato       |
| `GET`    | `/candidates`       | Obtener la lista de candidatos     |
| `GET`    | `/candidates/{id}`  | Obtener detalles de un candidato   |
| `DELETE` | `/candidates/{id}`  | Eliminar un candidato              |

### Votos

| Método | Ruta                 | Descripción                                              |
|--------|----------------------|----------------------------------------------------------|
| `POST` | `/votes`             | Emitir un voto (registra `voter_id` y `candidate_id`)    |
| `GET`  | `/votes`             | Obtener todos los votos emitidos                         |
| `GET`  | `/votes/statistics`  | Obtener estadísticas de la votación                      |

**`/votes/statistics` debe retornar:**

- Total de votos por candidato.
- Porcentaje de votos por candidato.
- Total de votantes que han votado.

---

## Validaciones

### 1. Votantes y candidatos

- Verificar que un votante no sea candidato, y viceversa.

### 2. Emisión de votos

- Comprobar que el votante no haya votado previamente.
- Validar que el `candidate_id` sea válido.

### 3. Integridad de los datos

- Actualizar automáticamente `has_voted` del votante al emitir un voto.
- Incrementar el conteo de `votes` del candidato seleccionado.

---

## Extras opcionales

1. Autenticación básica o con **JWT** para proteger los endpoints.
2. **Filtrado y paginación** en las listas de votantes y candidatos.

---

## Criterios de evaluación

1. Correcto funcionamiento de los endpoints.
2. Uso de validaciones y manejo de errores.
3. Estructura y organización del código.
4. Uso de patrones RESTful.
5. Documentación básica de la API (Swagger o README).

---

## Entrega

- Subir el código a un **repositorio público en GitHub**.
- Incluir un archivo `README.md` con:
  - Instrucciones para ejecutar el proyecto localmente.
  - Ejemplos de uso de la API (Postman o curl).
  - Capturas de las estadísticas generadas.