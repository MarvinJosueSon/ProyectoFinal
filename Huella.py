# Huella.py
# Autodetección de puerto + protocolo GUARDAR/ENVIA_ID_GUARDAR/GUARDADO_EXITOSO
# Ahora también: PING, CONTAR, LISTAR, EXISTE, BORRAR_ID, BORRAR_TODO

import time

try:
    import serial
    from serial.tools import list_ports
except ImportError:
    serial = None
    list_ports = None

PUERTO_SERIAL = None   # None => autodetectar
BAUD_RATE = 9600
TIMEOUT_S = 1
TIEMPO_ESPERA_INICIAL = 2

VID_PID_CONOCIDOS = {
    ("2341", "0043"),  # Arduino UNO R3
    ("2341", "0001"),  # Arduino UNO
    ("2A03", "0043"),  # Arduino (otra variante)
    ("1A86", "7523"),  # CH340/CH341
    ("1A86", "55D4"),  # CH9102
    ("10C4", "EA60"),  # CP210x
}

def _listar_puertos():
    if list_ports is None:
        return []
    puertos = []
    for p in list_ports.comports():
        vid = f"{p.vid:04X}" if p.vid is not None else ""
        pid = f"{p.pid:04X}" if p.pid is not None else ""
        puertos.append((p.device, p.description or "", vid, pid))
    return puertos

def _detectar_puerto(preferido: str | None = None) -> str:
    if serial is None:
        raise RuntimeError("pyserial no está instalado. Ejecuta: pip install pyserial")

    disponibles = _listar_puertos()
    if not disponibles:
        raise RuntimeError(
            "No se encontró ningún puerto serie.\n"
            "• Conecta el Arduino\n• Cierra el Monitor Serie\n• Instala driver CH340/CP210x si es necesario"
        )

    if preferido:
        for dev, _, _, _ in disponibles:
            if dev.upper() == preferido.upper():
                return dev

    for dev, _, vid, pid in disponibles:
        if (vid, pid) in VID_PID_CONOCIDOS:
            return dev

    return disponibles[0][0]

def _abrir_serial():
    port = _detectar_puerto(PUERTO_SERIAL)
    try:
        ser = serial.Serial(port, BAUD_RATE, timeout=TIMEOUT_S)
    except Exception as e:
        disponibles = _listar_puertos()
        det = "\n".join(f" - {d} ({desc}) VID:PID={vid}:{pid}" for d, desc, vid, pid in disponibles) or " (sin puertos)"
        raise RuntimeError(f"No se pudo abrir {port}. Detalle: {e}\nPuertos disponibles:\n{det}")
    time.sleep(TIEMPO_ESPERA_INICIAL)
    ser.reset_input_buffer()
    ser.reset_output_buffer()
    return ser

# ---------------- ENROLAR (ya existente) ----------------
def enrolar_huella_con_id(id_huella: int, timeout_total: int = 35) -> bool:
    """GUARDAR -> ENVIA_ID_GUARDAR -> <id> -> GUARDADO_EXITOSO"""
    if serial is None:
        raise RuntimeError("pyserial no está instalado. Ejecuta: pip install pyserial")

    ser = None
    try:
        ser = _abrir_serial()
        ser.write(b"GUARDAR\n")
        t0 = time.time()
        pid_enviado = False

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

# ---------------- NUEVAS UTILIDADES ----------------
def ping(timeout_total: int = 5) -> bool:
    """PING -> PONG"""
    ser = None
    try:
        ser = _abrir_serial()
        ser.write(b"PING\n")
        t0 = time.time()
        while time.time() - t0 < timeout_total:
            linea = ser.readline().decode("utf-8", errors="ignore").strip()
            if linea == "PONG":
                return True
        return False
    finally:
        if ser and ser.is_open:
            ser.close()

def contar_huellas(timeout_total: int = 8) -> int:
    """CONTAR -> PYTHON_RESPUESTA:TOTAL=<n>  | -1 si no responde"""
    ser = None
    try:
        ser = _abrir_serial()
        ser.write(b"CONTAR\n")
        t0 = time.time()
        while time.time() - t0 < timeout_total:
            linea = ser.readline().decode("utf-8", errors="ignore").strip()
            if linea.startswith("PYTHON_RESPUESTA:TOTAL="):
                try:
                    return int(linea.split("=", 1)[1])
                except Exception:
                    return -1
        return -1
    finally:
        if ser and ser.is_open:
            ser.close()

def listar_huellas_ids(timeout_total: int = 20) -> list[int]:
    """LISTAR -> ID:<n> ... FIN_LISTA"""
    ser = None
    ids = []
    try:
        ser = _abrir_serial()
        ser.write(b"LISTAR\n")
        t0 = time.time()
        while time.time() - t0 < timeout_total:
            linea = ser.readline().decode("utf-8", errors="ignore").strip()
            if not linea:
                continue
            if linea == "FIN_LISTA":
                break
            if linea.startswith("ID:"):
                try:
                    ids.append(int(linea.split(":", 1)[1]))
                except Exception:
                    pass
        return ids
    finally:
        if ser and ser.is_open:
            ser.close()

def existe_huella(id_huella: int, timeout_total: int = 8) -> bool:
    """EXISTE -> ENVIA_ID_EXISTE -> <id> -> PYTHON_RESPUESTA:EXISTE/NO_EXISTE"""
    ser = None
    try:
        ser = _abrir_serial()
        ser.write(b"EXISTE\n")
        t0 = time.time()
        pid_enviado = False
        while time.time() - t0 < timeout_total:
            linea = ser.readline().decode("utf-8", errors="ignore").strip()
            if not linea:
                continue
            if "PYTHON_INSTRUCCION" in linea and "ENVIA_ID_EXISTE" in linea and not pid_enviado:
                ser.write(f"{int(id_huella)}\n".encode("utf-8"))
                pid_enviado = True
            if linea.startswith("PYTHON_RESPUESTA:"):
                if "EXISTE" in linea:
                    return True
                if "NO_EXISTE" in linea:
                    return False
        return False
    finally:
        if ser and ser.is_open:
            ser.close()

def borrar_huella_id(id_huella: int, timeout_total: int = 12) -> bool:
    """BORRAR_ID -> ENVIA_ID_BORRAR -> <id> -> PYTHON_RESPUESTA:BORRADO_OK/BORRADO_ERROR"""
    ser = None
    try:
        ser = _abrir_serial()
        ser.write(b"BORRAR_ID\n")
        t0 = time.time()
        pid_enviado = False
        while time.time() - t0 < timeout_total:
            linea = ser.readline().decode("utf-8", errors="ignore").strip()
            if not linea:
                continue
            if "PYTHON_INSTRUCCION" in linea and "ENVIA_ID_BORRAR" in linea and not pid_enviado:
                ser.write(f"{int(id_huella)}\n".encode("utf-8"))
                pid_enviado = True
            if linea.startswith("PYTHON_RESPUESTA:"):
                if "BORRADO_OK" in linea:
                    return True
                if "BORRADO_ERROR" in linea or "NO_EXISTE" in linea:
                    return False
        return False
    finally:
        if ser and ser.is_open:
            ser.close()

def borrar_todas_huellas(timeout_total: int = 25) -> bool:
    """BORRAR_TODO -> PYTHON_RESPUESTA:BORRADO_TODO_OK/BORRADO_TODO_ERROR"""
    ser = None
    try:
        ser = _abrir_serial()
        ser.write(b"BORRAR_TODO\n")
        t0 = time.time()
        while time.time() - t0 < timeout_total:
            linea = ser.readline().decode("utf-8", errors="ignore").strip()
            if linea.startswith("PYTHON_RESPUESTA:"):
                if "BORRADO_TODO_OK" in linea:
                    return True
                if "BORRADO_TODO_ERROR" in linea:
                    return False
        return False
    finally:
        if ser and ser.is_open:
            ser.close()
