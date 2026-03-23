#  The Huddle - Servidor de Logging Distribuido

Este proyecto es una implementación para el desafío de logging de "The Huddle". Consiste en un sistema de logging distribuido compuesto por un servidor central y clientes simulados que envían logs a través de HTTP.

El objetivo es tener un punto centralizado que reciba, autentique, almacene y permita consultar logs de diferentes servicios.

##  Requisitos Previos

- Python 3.7+
- `pip` (el gestor de paquetes de Python)

##  Instalación y Configuración

1.  **Clona o descarga el repositorio.**

2.  **Navega al directorio del proyecto:**
    ```bash
    cd 5_the_huddle
    ```

3.  **(Opcional pero recomendado) Crea un entorno virtual:**
    ```bash
    python -m venv .venv
    ```
    Y actívalo:
    -   **Windows:** `.\.venv\Scripts\activate`
    -   **macOS/Linux:** `source .venv/bin/activate`

4.  **Instala las dependencias** desde `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

##  Ejecución del Sistema

Necesitarás dos terminales: una para el servidor y otra para el cliente.

### 1. Iniciar el Servidor Central

En la primera terminal, ejecuta el siguiente comando para iniciar el servidor FastAPI con `uvicorn`. La opción `--reload` hace que el servidor se reinicie automáticamente si detecta cambios en el código.

```bash
uvicorn main:app --reload
```

Deberías ver una salida similar a esta, indicando que el servidor está en funcionamiento:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx]
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 2. Ejecutar los Clientes Simulados

En la segunda terminal, ejecuta el script del cliente:

```bash
python client.py
```

Este script comenzará a simular los servicios "A", "B" y "C", enviando lotes de logs al servidor cada pocos segundos. Verás en la consola la salida de cada intento de envío.

```
Iniciando simulación de envío de logs...
Presiona CTRL+C para detener.
[servicio_A] Enviando 3 logs...
[servicio_A] Respuesta del servidor: 201 - {'status': 'ok', 'logs_received': 3}
[servicio_B] Enviando 5 logs...
[servicio_B] Respuesta del servidor: 201 - {'status': 'ok', 'logs_received': 5}
...
```

##  API Endpoints

### Enviar Logs

-   **Endpoint:** `POST /logs`
-   **Autenticación:** Requerida. Se debe enviar un `Authorization Header` con el formato `Token <TU_TOKEN>`.
-   **Body:** Un JSON con una lista de objetos de log.

    **Ejemplo de Body:**
    ```json
    [
        {
            "timestamp": "2026-03-19T18:30:00Z",
            "service": "servicio_A",
            "severity": "INFO",
            "message": "Operación completada."
        }
    ]
    ```

### Consultar Logs

-   **Endpoint:** `GET /logs`
-   **Autenticación:** Requerida (igual que en el POST).
-   **Query Parameters (opcionales):**
    -   `timestamp_start`: Filtra logs a partir de esta fecha (formato ISO).
    -   `timestamp_end`: Filtra logs hasta esta fecha.
    -   `received_at_start`: Filtra por fecha de recepción en el servidor.
    -   `received_at_end`: Filtra por fecha de recepción en el servidor.
    -   `limit`: Número máximo de logs a devolver (por defecto: 100).

-   **Ejemplo de consulta con `curl`:**
    ```bash
    curl -X GET "http://127.0.0.1:8000/logs?limit=5" -H "Authorization: Token token_servicio_A"
    ```
