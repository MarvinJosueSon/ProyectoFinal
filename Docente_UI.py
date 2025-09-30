# Docente_UI.py
import ttkbootstrap as tb
from ttkbootstrap import ttk

class VentanaDocente(tb.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Docente")
        self.geometry("900x600")
        contenedor = ttk.Frame(self, padding=16)
        contenedor.pack(fill="both", expand=True)
        ttk.Label(contenedor, text="Panel del Docente", font=("Segoe UI", 16, "bold")).pack(anchor="w")
