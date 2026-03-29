"""
Simulador de dispositivo IoT - Práctica de Arquitectura IoT
Equipo: [Nombre del equipo]
Descripción: Simula sensores de temperatura, humedad y calidad del aire
             y envía datos periódicamente a una capa Fog/Cloud via HTTP
"""

import json
import random
import time
import datetime
import math
import urllib.request
import urllib.parse
import urllib.error

# ============================================================
# CONFIGURACIÓN DEL DISPOSITIVO
# ============================================================
DEVICE_CONFIG = {
    "device_id": "sensor-node-001",
    "device_type": "environmental_monitor",
    "location": "Edificio A - Laboratorio 3",
    "firmware": "v1.2.0",
    # URL del servidor fog/cloud receptor
    # Cambia esto por tu endpoint real
    "endpoint_url": "http://localhost:5000/api/telemetry",
    # Intervalo de envío en segundos
    "send_interval": 10,
}

# ============================================================
# SIMULACIÓN DE SENSORES
# ============================================================
class SensorSimulator:
    """Simula lecturas de sensores físicos con variación realista."""

    def __init__(self):
        self.base_temp = 22.0       # Temperatura base en °C
        self.base_hum = 55.0        # Humedad base en %
        self.base_co2 = 400.0       # CO2 base en ppm
        self.base_light = 300.0     # Luz base en lux
        self._tick = 0

    def _noise(self, magnitude=1.0):
        """Genera ruido gaussiano para simular variación del sensor."""
        return random.gauss(0, magnitude)

    def _drift(self, base, amplitude, speed=0.05):
        """Simula deriva lenta del sensor (onda sinusoidal + ruido)."""
        return base + amplitude * math.sin(self._tick * speed) + self._noise(0.3)

    def read_all(self):
        """Lee todos los sensores y retorna un diccionario con los datos."""
        self._tick += 1
        hora = datetime.datetime.now().hour

        # Temperatura sube en horas de actividad (8-18h)
        temp_offset = 3.0 if 8 <= hora <= 18 else 0.0
        temperature = round(self._drift(self.base_temp + temp_offset, 2.5), 2)

        # Humedad inversamente relacionada con temperatura
        humidity = round(self._drift(self.base_hum - (temperature - self.base_temp) * 0.5, 3.0), 2)
        humidity = max(20.0, min(95.0, humidity))

        # CO2 sube si hay "personas" (horas de actividad)
        co2_offset = 200.0 if 8 <= hora <= 18 else 0.0
        co2 = round(self._drift(self.base_co2 + co2_offset, 50.0, speed=0.03), 1)
        co2 = max(350.0, co2)

        # Luz solar simulada
        if 6 <= hora <= 20:
            luz_solar = max(0, 500 * math.sin(math.pi * (hora - 6) / 14))
        else:
            luz_solar = 0
        light_level = round(luz_solar + self.base_light * 0.2 + self._noise(10), 1)
        light_level = max(0, light_level)

        # Estado del dispositivo
        battery = round(100 - (self._tick * 0.01), 1)
        battery = max(0, battery)

        return {
            "temperature_c": temperature,
            "humidity_pct": humidity,
            "co2_ppm": co2,
            "light_lux": light_level,
            "battery_pct": battery,
        }

# ============================================================
# CREACIÓN DEL PAYLOAD
# ============================================================
def build_payload(sensor_data: dict) -> dict:
    """
    Construye el paquete de datos completo que se enviará.
    Incluye metadatos del dispositivo + lecturas de sensores.
    """
    return {
        "device_id": DEVICE_CONFIG["device_id"],
        "device_type": DEVICE_CONFIG["device_type"],
        "location": DEVICE_CONFIG["location"],
        "firmware": DEVICE_CONFIG["firmware"],
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "timestamp_local": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "sensors": sensor_data,
        "protocol": "HTTP/1.1",
        "schema_version": "1.0",
    }

# ============================================================
# ENVÍO DE DATOS (HTTP POST)
# ============================================================
def send_data(payload: dict) -> dict:
    """
    Envía el payload al servidor fog/cloud via HTTP POST.
    Retorna la respuesta del servidor o un error.
    """
    url = DEVICE_CONFIG["endpoint_url"]
    data = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Content-Type": "application/json",
            "X-Device-ID": DEVICE_CONFIG["device_id"],
            "X-API-Version": "1.0",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            body = response.read().decode("utf-8")
            return {
                "success": True,
                "status_code": response.status,
                "response": body,
            }
    except urllib.error.HTTPError as e:
        return {"success": False, "error": f"HTTP {e.code}: {e.reason}"}
    except urllib.error.URLError as e:
        return {"success": False, "error": f"URL Error: {e.reason}"}
    except Exception as e:
        return {"success": False, "error": str(e)}

# ============================================================
# LOOP PRINCIPAL
# ============================================================
def main():
    print("=" * 60)
    print("  Simulador de Dispositivo IoT")
    print(f"  Device ID : {DEVICE_CONFIG['device_id']}")
    print(f"  Endpoint  : {DEVICE_CONFIG['endpoint_url']}")
    print(f"  Intervalo : {DEVICE_CONFIG['send_interval']}s")
    print("=" * 60)
    print()

    sensor = SensorSimulator()
    iteration = 0

    while True:
        iteration += 1
        print(f"[Ciclo #{iteration}] {datetime.datetime.now().strftime('%H:%M:%S')}")

        # 1. Leer sensores
        sensor_data = sensor.read_all()
        print(f"  Temp: {sensor_data['temperature_c']}°C  |  "
              f"Hum: {sensor_data['humidity_pct']}%  |  "
              f"CO2: {sensor_data['co2_ppm']} ppm  |  "
              f"Luz: {sensor_data['light_lux']} lux  |  "
              f"Batería: {sensor_data['battery_pct']}%")

        # 2. Construir payload
        payload = build_payload(sensor_data)

        # 3. Enviar al servidor
        result = send_data(payload)
        if result["success"]:
            print(f"  Envío OK (HTTP {result['status_code']})")
        else:
            print(f"  ERROR al enviar: {result['error']}")
            # Guardar localmente si no hay conexión (buffer offline)
            with open("buffer_offline.jsonl", "a") as f:
                f.write(json.dumps(payload) + "\n")
            print("  Datos guardados en buffer_offline.jsonl")

        print()
        time.sleep(DEVICE_CONFIG["send_interval"])

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nSimulador detenido por el usuario.")
