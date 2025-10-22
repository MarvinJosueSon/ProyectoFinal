# Huella.py
import time
try:
    import serial
except ImportError:
    raise ImportError("Instala pyserial: pip install pyserial")

PUERTO_SERIAL = "COM5"
BAUD_RATE = 9600
TIMEOUT_S = 1
TIEMPO_ESPERA_INICIAL = 2

def enrolar_huella_con_id(id_huella: int, timeout_total: int = 35) -> bool:
    """Envía GUARDAR -> espera ENVIA_ID_GUARDAR -> manda id -> valida GUARDADO_EXITOSO."""
    ser = None
    try:
        ser = serial.Serial(PUERTO_SERIAL, BAUD_RATE, timeout=TIMEOUT_S)
        time.sleep(TIEMPO_ESPERA_INICIAL)
        ser.reset_input_buffer(); ser.reset_output_buffer()

        ser.write(b"GUARDAR\n")
        t0 = time.time(); pid_enviado = False

        while time.time() - t0 < timeout_total:
            linea = ser.readline().decode("utf-8", errors="ignore").strip()
            if not linea:
                continue
            if "PYTHON_INSTRUCCION" in linea and "ENVIA_ID_GUARDAR" in linea and not pid_enviado:
                ser.write(f"{id_huella}\n".encode("utf-8"))
                pid_enviado = True
            if linea.startswith("PYTHON_RESPUESTA:"):
                if "GUARDADO_EXITOSO" in linea:
                    return True
                if "GUARDADO_FALLIDO" in linea or "ID_INVALIDO" in linea:
                    return False
        return False
    finally:
        if ser and ser.is_open:
            ser.close()
