# 📖 Conceptos Clave para Estudiar

Este proyecto, aunque pequeño, implementa varios conceptos fundamentales en el desarrollo de software moderno. Aquí tienes una guía de estudio basada en el código que hemos construido.

---

## 1. Backend y APIs

### REST (Representational State Transfer)
Es el estilo arquitectónico sobre el que construiste tu API. Se basa en la comunicación cliente-servidor sin estado a través del protocolo HTTP.
- **Recursos:** Todo es un recurso (en tu caso, los logs). Cada recurso tiene una URL única (ej: `/logs`).
- **Verbos HTTP:** Usaste `POST` para crear nuevos logs y `GET` para leerlos. Otros verbos comunes son `PUT` (actualizar) y `DELETE` (borrar).

### FastAPI
Es el framework que usaste para construir el servidor. Sus características clave son:
- **Alto Rendimiento:** Es muy rápido gracias a su base (Starlette y Pydantic).
- **Tipado de Python:** Usa los "type hints" de Python (ej: `name: str`) para validar, serializar y documentar automáticamente los datos de la API.
- **Inyección de Dependencias:** Usaste `Depends()` para la base de datos (`get_db`) y la autenticación (`verify_token`). Este es un patrón poderoso que hace el código más modular y fácil de testear. El sistema se encarga de "inyectar" el resultado de una función en otra.
- **Documentación Automática:** FastAPI genera una documentación interactiva de tu API (normalmente en `/docs` y `/redoc`) que es increíblemente útil para probar los endpoints.

### Uvicorn
Es un servidor web ASGI (Asynchronous Server Gateway Interface). Es el "motor" que ejecuta tu aplicación FastAPI y le permite manejar muchas conexiones de manera eficiente y asíncrona.

## 2. Arquitectura y Patrones

### Modelo Cliente-Servidor
La arquitectura fundamental de tu proyecto. El **servidor** (`main.py`) ofrece un servicio (la API de logging), y el **cliente** (`client.py`) consume ese servicio. Están desacoplados y se comunican a través de una red (en este caso, en tu propia máquina).

### Logging Distribuido
Es el problema que resolviste. En lugar de que cada servicio guarde sus logs en un archivo local (lo cual es un caos en sistemas con muchos microservicios), los envían a un **punto centralizado**. Esto facilita enormemente la búsqueda, el análisis y la monitorización.

### Autenticación basada en Tokens
Es el mecanismo de seguridad que implementaste.
- **Flujo:** El cliente presenta un "secreto" (el token) en cada solicitud. El servidor valida ese token contra una lista de tokens permitidos.
- **Stateless (sin estado):** A diferencia de las sesiones, el servidor no necesita recordar nada sobre el cliente entre solicitudes. Toda la información necesaria para la autenticación está en la propia solicitud (el token).
- **HTTP Header `Authorization`:** Es el lugar estándar para enviar credenciales como los tokens. El formato `Token <valor>` o `Bearer <valor>` es muy común.

## 3. Base de Datos

### SQLite
Es un motor de base de datos SQL auto-contenido, sin servidor. Funciona con un simple archivo (`logs.db` en tu caso). Es perfecto para aplicaciones pequeñas, prototipos o desarrollo local porque no requiere ninguna configuración.

### SQL (Structured Query Language)
El lenguaje que usaste para interactuar con la base de datos.
- **`CREATE TABLE`:** Define la estructura de una tabla y sus columnas.
- **`INSERT INTO`:** Añade nuevas filas (registros) a una tabla.
- **`SELECT ... FROM ... WHERE`:** Consulta y filtra datos de una tabla.
- **Parámetros (`?`):** Es **crucial** usar parámetros en lugar de formatear strings directamente en la consulta (`f"SELECT * FROM logs WHERE service = '{service_name}'"`). Esto previene un tipo de ataque muy común y peligroso llamado **Inyección SQL**.

## 4. Python

### Entornos Virtuales (`venv`)
Una de las mejores prácticas en Python. Crea un entorno aislado para cada proyecto, con sus propias dependencias. Esto evita conflictos entre las librerías que necesitan diferentes proyectos.

### `requests`
La librería estándar de facto en Python para hacer solicitudes HTTP. Es muy potente y fácil de usar, como viste en `client.py`.

### `if __name__ == "__main__":`
Esta construcción asegura que el código dentro de este bloque solo se ejecute cuando el archivo es ejecutado directamente (`python client.py`), y no cuando es importado por otro script. Es fundamental para crear scripts reutilizables.
