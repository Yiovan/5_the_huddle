from fastapi import FastAPI, Header, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import sqlite3

app = FastAPI()

VALID_TOKENS = {
    "token_servicio_A": "servicio_A",
    "token_servicio_B": "servicio_B",
    "token_servicio_C": "servicio_C",
}

# Conecto con la base de datos (un archivo en la misma carpeta)
conn = sqlite3.connect("logs.db", check_same_thread=False)
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    service TEXT,
    severity TEXT,
    message TEXT,
    received_at TEXT
)
""")

# Un "modelo" para que FastAPI sepa qué datos esperar en el body del POST
class Log(BaseModel):
    timestamp: datetime
    service: str
    severity: str
    message: str

# Endpoint para recibir los logs
@app.post("/logs")
def receive_logs(logs: List[Log], Authorization: str = Header(None)):
    # --- Verificación del token (copiada aquí) ---
    if not Authorization or not Authorization.startswith("Token "):
        raise HTTPException(status_code=401, detail={"error": "Quién sos, bro?"})
    
    token = Authorization.split(" ")[1]
    if token not in VALID_TOKENS:
        raise HTTPException(status_code=401, detail={"error": "Quién sos, bro?"})
    
    now = datetime.utcnow().isoformat()
    
    for log_recibido in logs:
        # Guardo cada parte del log en una variable
        log_timestamp = log_recibido.timestamp.isoformat()
        log_service = log_recibido.service
        log_severity = log_recibido.severity
        log_message = log_recibido.message

        # Inserto el log en la tabla
        cursor.execute(
            "INSERT INTO logs (timestamp, service, severity, message, received_at) VALUES (?, ?, ?, ?, ?)",
            (log_timestamp, log_service, log_severity, log_message, now)
        )
    
    # "Guardo" los cambios en la base de datos
    conn.commit()
    
    # Devuelvo una respuesta para que el cliente sepa que todo salió bien
    return {"status": "ok", "logs_received": len(logs)}

# Endpoint para pedir los logs guardados
@app.get("/logs")
def get_logs(
    Authorization: str = Header(None),
    token: Optional[str]= Query(None),
    timestamp_start: Optional[str] = Query(None),
    timestamp_end: Optional[str] = Query(None),
    received_at_start: Optional[str] = Query(None),
    received_at_end: Optional[str] = Query(None)
):
    
    
    auth_value = Authorization
    if not auth_value and token:
        auth_value = f"token {token}"
    
    if not Authorization or not Authorization.startswith("Token "):
        raise HTTPException(status_code=401, detail={"error": "Quién sos, bro?"})
    
    token = Authorization.split(" ")[1]
    if token not in VALID_TOKENS:
        raise HTTPException(status_code=401, detail={"error": "Quién sos, bro?"})


    query = "SELECT * FROM logs WHERE 1=1"
    params = []

    if timestamp_start: 
        query = query + " AND timestamp >= ?"
        params.append(timestamp_start)
    if timestamp_end: 
        query = query + " AND timestamp <= ?"
        params.append(timestamp_end)
    if received_at_start:
        query = query + " AND received_at >= ?"
        params.append(received_at_start)
    if received_at_end:
        query = query + " AND received_at <= ?"
        params.append(received_at_end)

    query = query + " ORDER BY timestamp DESC LIMIT 100"
    
    cursor.execute(query, tuple(params))
    filas_de_logs = cursor.fetchall() 

    resultado_final = []
    
    for fila in filas_de_logs:
        log_dict = {
            "id": fila[0],
            "timestamp": fila[1],
            "service": fila[2],
            "severity": fila[3],
            "message": fila[4],
            "received_at": fila[5]
        }
        resultado_final.append(log_dict)
    
    return resultado_final
