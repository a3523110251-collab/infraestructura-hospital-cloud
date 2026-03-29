"""
Servidor receptor Fog/Cloud - Capa de recepción IoT
Descripción: Recibe, valida y almacena los datos enviados por
             el dispositivo IoT simulado.
"""

import json
import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

# Almacenamiento en memoria de los datos recibidos (para demo)
received_data = []

class TelemetryHandler(BaseHTTPRequestHandler):
    """Manejador HTTP para recibir datos de telemetría IoT."""

    def do_POST(self):
        if self.path == "/api/telemetry":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)

            try:
                payload = json.loads(body.decode("utf-8"))
                # Validar campos obligatorios
                required = ["device_id", "timestamp", "sensors"]
                if not all(k in payload for k in required):
                    self._respond(400, {"error": "Payload incompleto"})
                    return

                # Registrar recepción
                received_data.append({
                    "received_at": datetime.datetime.utcnow().isoformat() + "Z",
                    "device_id": payload["device_id"],
                    "sensors": payload["sensors"],
                })

                print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] "
                      f"Datos recibidos de {payload['device_id']}: "
                      f"T={payload['sensors']['temperature_c']}°C  "
                      f"H={payload['sensors']['humidity_pct']}%  "
                      f"CO2={payload['sensors']['co2_ppm']}ppm")

                self._respond(200, {
                    "status": "ok",
                    "message": "Telemetría registrada",
                    "received_at": datetime.datetime.utcnow().isoformat() + "Z",
                    "total_records": len(received_data),
                })

            except json.JSONDecodeError:
                self._respond(400, {"error": "JSON inválido"})
        else:
            self._respond(404, {"error": "Ruta no encontrada"})

    def do_GET(self):
        if self.path == "/api/telemetry":
            self._respond(200, {"records": received_data, "count": len(received_data)})
        elif self.path == "/health":
            self._respond(200, {"status": "healthy", "records": len(received_data)})
        else:
            self._respond(404, {"error": "Ruta no encontrada"})

    def _respond(self, status: int, body: dict):
        response = json.dumps(body).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)

    def log_message(self, format, *args):
        pass  # Silenciar logs HTTP por defecto


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 5000), TelemetryHandler)
    print("=" * 55)
    print("  Servidor Fog/Cloud - Receptor IoT")
    print("  Escuchando en http://0.0.0.0:5000")
    print("  GET  /api/telemetry → ver todos los datos")
    print("  POST /api/telemetry → recibir telemetría")
    print("  GET  /health        → estado del servidor")
    print("=" * 55)
    print()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")
