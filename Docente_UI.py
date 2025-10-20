# Docente_UI.py
import ttkbootstrap as tb
from ttkbootstrap import ttk
from DB_Manager import obtener_docente_por_usuario


class VentanaDocente(tb.Toplevel):
    def __init__(self, master, usuario_docente: str = None):
        super().__init__(master)

        # --- Definir título dinámico ---
        nombre_para_titulo = "Docente"
        if usuario_docente:
            nombre_para_titulo = f"'{usuario_docente}'"

        # Intentar obtener el nombre real del docente desde la BD
        try:
            docente = obtener_docente_por_usuario(usuario_docente) if usuario_docente else None
            if docente and getattr(docente, "nombre", None):
                nombre_para_titulo = f"'{docente.nombre}'"
        except Exception:
            pass

        self.title(f"Docente - {nombre_para_titulo}")
        self.geometry("900x600")
        self.resizable(True, True)

        # --- Contenido simple de ejemplo ---
        contenedor = ttk.Frame(self, padding=20)
        contenedor.pack(fill="both", expand=True)

        etiqueta = ttk.Label(
            contenedor,
            text=f"Bienvenido al panel de {nombre_para_titulo}",
            font=("Segoe UI", 14, "bold")
        )
        etiqueta.pack(pady=40)

        ttk.Label(
            contenedor,
            text="Aquí se mostrarán las opciones del docente próximamente.",
            font=("Segoe UI", 11)
        ).pack(pady=10)
