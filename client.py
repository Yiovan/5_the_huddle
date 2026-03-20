import requests
import random
import time
from datetime import datetime

URL = "http://127.0.0.1:8000/logs"

TOKENS = {
    "servicio_A": "token_servicio_A",
    "servicio_B": "token_servicio_B",
    "servicio_C": "token_servicio_C",
}

SEVERITIES = ["INFO", "DEBUG", "ERROR", "WARNING"]
MESSAGES = [
    "Todo funcionando correctamente",
    "Consulta lenta detectada",
    "Error al conectar con la base de datos",
    "Timeout en servicio externo",
    "Memoria alta",
]

if __name__ == "__main__":
    print("Iniciando cliente... Presiona CTRL+C para parar.")

    while True:
        lista_de_servicios = ["servicio_A", "servicio_B", "servicio_C"]
        
        for nombre_del_servicio in lista_de_servicios:
            print("---")
            print("Turno del servicio:", nombre_del_servicio)

            mi_token = TOKENS[nombre_del_servicio]
            headers = {"Authorization": "Token " + mi_token}

            logs_para_enviar = []
            
            numero_de_logs = random.randint(1, 5)
            print("Voy a generar", numero_de_logs, "logs.")

            for i in range(numero_de_logs):
                un_log = {
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                    "service": nombre_del_servicio,
                    "severity": random.choice(SEVERITIES),
                    "message": random.choice(MESSAGES)
                }
                logs_para_enviar.append(un_log)

            try:
                print("Enviando los logs al servidor...")
                response = requests.post(URL, json=logs_para_enviar, headers=headers)
                
                response.raise_for_status()
                
                print("Respuesta del servidor:", response.status_code)

            except Exception as e:
                print("!!! Hubo un error:", e)

            time.sleep(1)
        
        print("\n--- Ronda terminada, esperando 10 segundos... ---\n")
        time.sleep(10)
