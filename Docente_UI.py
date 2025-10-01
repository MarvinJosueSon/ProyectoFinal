# Docente_UI.py
import ttkbootstrap as tb
from ttkbootstrap import ttk

class VentanaDocente(tb.Toplevel):
    def __init__(self, master, cursos=None, estudiantes=None, usuario_docente=None):
        super().__init__(master)
        self.title("Docente")
        self.geometry("900x600")


        self.cursos = cursos or {}
        self.estudiantes = estudiantes or {}
        self.usuario_docente = usuario_docente

        contenedor = ttk.Frame(self, padding=16)
        contenedor.pack(fill="both", expand=True)

        titulo = "Panel del Docente"
        if self.usuario_docente:
            titulo += f" — {self.usuario_docente}"
        ttk.Label(contenedor, text=titulo, font=("Segoe UI", 16, "bold")).pack(anchor="w")
