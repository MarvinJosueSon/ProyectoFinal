# Huella.py (versión persistente sin auto-reset)
# - Mantiene un solo puerto serie abierto (evita resets del Arduino por DTR/RTS)
# - Desactiva DTR/RTS tras abrir el puerto
# - Quita todos los cierres del puerto en cada operación
# - Misma API pública que usas en tu proyecto

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

# ---------------- Conexión persistente ----------------
_SER = None  # instancia global persistente


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


def _get_serial():
    """Abre (si hace falta) y devuelve la conexión persistente sin DTR/RTS."""
    global _SER
    if _SER and _SER.is_open:
        return _SER

    port = _detectar_puerto(PUERTO_SERIAL)
    s = serial.Serial(
        port,
        BAUD_RATE,
        timeout=TIMEOUT_S,
        write_timeout=TIMEOUT_S,
        rtscts=False,
        dsrdtr=False,
    )
    # Evitar auto-reset por líneas de control
    try:
        s.setDTR(False)
        s.setRTS(False)
    except Exception:
        pass

    time.sleep(TIEMPO_ESPERA_INICIAL)
    try:
        s.reset_input_buffer()
        s.reset_output_buffer()
    except Exception:
        pass

    _SER = s
    return _SER


def _reconectar():
    """Cierra (si está) y reabre el puerto de forma segura."""
    global _SER
    try:
        if _SER and _SER.is_open:
            _SER.close()
    except Exception:
        pass
    _SER = None
    return _get_serial()


# ---------------- Protocolo de alto nivel ----------------
def enrolar_huella_con_id(id_huella: int, timeout_total: int = 35) -> bool:
    """GUARDAR -> ENVIA_ID_GUARDAR -> <id> -> GUARDADO_EXITOSO"""
    if serial is None:
        raise RuntimeError("pyserial no está instalado. Ejecuta: pip install pyserial")

    ser = _get_serial()
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


def ping(timeout_total: int = 5) -> bool:
    """PING -> PONG"""
    ser = _get_serial()
    ser.write(b"PING\n")
    t0 = time.time()
    while time.time() - t0 < timeout_total:
        linea = ser.readline().decode("utf-8", errors="ignore").strip()
        if linea == "PONG":
            return True
    return False


def contar_huellas(timeout_total: int = 8) -> int:
    """CONTAR -> PYTHON_RESPUESTA:TOTAL=<n>  | -1 si no responde"""
    ser = _get_serial()
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


def listar_huellas_ids(timeout_total: int = 20) -> list[int]:
    """LISTAR -> ID:<n> ... FIN_LISTA"""
    ser = _get_serial()
    ids = []
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


def existe_huella(id_huella: int, timeout_total: int = 8) -> bool:
    """EXISTE -> ENVIA_ID_EXISTE -> <id> -> PYTHON_RESPUESTA:EXISTE/NO_EXISTE"""
    ser = _get_serial()
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


def borrar_huella_id(id_huella: int, timeout_total: int = 12) -> bool:
    """BORRAR_ID -> ENVIA_ID_BORRAR -> <id> -> PYTHON_RESPUESTA:BORRADO_OK/BORRADO_ERROR"""
    ser = _get_serial()
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


def borrar_todas_huellas(timeout_total: int = 25) -> bool:
    """BORRAR_TODO -> PYTHON_RESPUESTA:BORRADO_TODO_OK/BORRADO_TODO_ERROR"""
    ser = _get_serial()
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


def verificar_huella(timeout_total: int = 14):
    """
    Envía VERIFICAR y espera:
      - PYTHON_RESPUESTA:VERIFICADO_ID=<n>  -> (True, n)
      - PYTHON_RESPUESTA:SIN_COINCIDENCIA  -> (False, None)
    """
    if serial is None:
        raise RuntimeError("pyserial no está instalado. Ejecuta: pip install pyserial")

    ser = _get_serial()
    ser.write(b"VERIFICAR\n")
    t0 = time.time()
    while time.time() - t0 < timeout_total:
        linea = ser.readline().decode("utf-8", errors="ignore").strip()
        if not linea:
            continue
        if linea.startswith("PYTHON_RESPUESTA:VERIFICADO_ID="):
            try:
                n = int(linea.split("=", 1)[1])
                return True, n
            except Exception:
                return False, None
        if "PYTHON_RESPUESTA:SIN_COINCIDENCIA" in linea:
            return False, None
    return False, None


# ---------------- Utilidades opcionales ----------------
def cerrar_puerto():
    """Si necesitas cerrar el puerto manualmente (rara vez)."""
    global _SER
    try:
        if _SER and _SER.is_open:
            _SER.close()
    except Exception:
        pass
    _SER = None
