# Huella.py
# Autodetección de puerto + protocolo GUARDAR/ENVIA_ID_GUARDAR/GUARDADO_EXITOSO

import time

try:
    import serial
    from serial.tools import list_ports
except ImportError:
    serial = None
    list_ports = None

# Si quieres forzar uno manualmente, pon por ej. "COM7"
PUERTO_SERIAL = None   # None => autodetectar
BAUD_RATE = 9600
TIMEOUT_S = 1
TIEMPO_ESPERA_INICIAL = 2

# VID:PID comunes (Arduino oficial y clones)
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

    # 1) Si nos pasaron uno preferido y existe, úsalo
    if preferido:
        for dev, _, _, _ in disponibles:
            if dev.upper() == preferido.upper():
                return dev

    # 2) Coincidencia por VID:PID conocidos
    for dev, _, vid, pid in disponibles:
        if (vid, pid) in VID_PID_CONOCIDOS:
            return dev

    # 3) Si no hay coincidencia, el primero disponible
    return disponibles[0][0]

def _abrir_serial():
    port = _detectar_puerto(PUERTO_SERIAL)
    try:
        ser = serial.Serial(port, BAUD_RATE, timeout=TIMEOUT_S)
    except Exception as e:
        # Mostrar puertos para diagnóstico
        disponibles = _listar_puertos()
        det = "\n".join(f" - {d} ({desc}) VID:PID={vid}:{pid}" for d, desc, vid, pid in disponibles) or " (sin puertos)"
        raise RuntimeError(f"No se pudo abrir {port}. Detalle: {e}\nPuertos disponibles:\n{det}")
    time.sleep(TIEMPO_ESPERA_INICIAL)
    ser.reset_input_buffer()
    ser.reset_output_buffer()
    return ser

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
            # print("ARDUINO:", linea)  # descomenta para debug
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
