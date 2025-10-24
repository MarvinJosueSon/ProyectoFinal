#Base.py
import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap import ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from DB_Manager import init_db, obtener_docente_por_usuario_y_contrasena
from Admin_UI import VentanaAdministrador
from Docente_UI import VentanaDocente

class TarjetaLogin(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=24, style="card")
        self.ventana_administrador = None
        self.ventana_docente = None
        init_db()  # Asegura tablas creadas
        self.construir()

    def construir(self):
        ttk.Label(self, text="Ingreso al sistema", font=("Segoe UI", 16, "bold")).grid(row=0, column=0, columnspan=3, pady=(0,12))
        ttk.Label(self, text="Usuario").grid(row=1, column=0, sticky="e", padx=6, pady=6)
        ttk.Label(self, text="Contraseña").grid(row=2, column=0, sticky="e", padx=6, pady=6)

        self.entrada_usuario = ttk.Entry(self, width=28)
        self.entrada_contrasena = ttk.Entry(self, show="*", width=28)
        self.entrada_usuario.grid(row=1, column=1, padx=6, pady=6)
        self.entrada_contrasena.grid(row=2, column=1, padx=6, pady=6)

        self.ver_contrasena = tk.BooleanVar(value=False)
        ttk.Checkbutton(self, text="Mostrar", variable=self.ver_contrasena,
                        command=self.alternar_contrasena, bootstyle=SECONDARY).grid(row=2, column=2, sticky="w", padx=(0,6))

        marco_botones = ttk.Frame(self)
        marco_botones.grid(row=3, column=0, columnspan=3, pady=(12,0))
        ttk.Button(marco_botones, text="Entrar", bootstyle=PRIMARY, command=self.entrar).pack(side="left", padx=4)
        ttk.Button(marco_botones, text="Limpiar", bootstyle=INFO, command=self.limpiar).pack(side="left", padx=4)
        ttk.Button(marco_botones, text="Salir", bootstyle=DANGER, command=self.salir).pack(side="left", padx=4)

        self.entrada_contrasena.bind("<Return>", lambda e: self.entrar())

    def alternar_contrasena(self):
        self.entrada_contrasena.configure(show="" if self.ver_contrasena.get() else "*")

    def entrar(self):
        usuario = self.entrada_usuario.get().strip()
        contrasena = self.entrada_contrasena.get().strip()

        if not usuario or not contrasena:
            messagebox.showwarning("Atención", "Ingresa el usuario y la contraseña.")
            return

        # Admin fijo
        if usuario == "admin" and contrasena == "123":
            self.abrir_administrador()
            return
        if usuario == "Tello" and contrasena == "123":
            self.abrir_administrador()
            return
        if usuario == "Castillo" and contrasena == "123":
            self.abrir_administrador()
            return
        # Docente en BD
        docente = obtener_docente_por_usuario_y_contrasena(usuario, contrasena)
        if docente:
            self.abrir_docente(usuario)
            return

        messagebox.showerror("Error", "Credenciales incorrectas o inexistentes.")

    def abrir_administrador(self):
        if self.ventana_administrador and self.ventana_administrador.winfo_exists():
            self.ventana_administrador.deiconify(); self.ventana_administrador.lift(); self.ventana_administrador.focus_force()
            return
        self.ventana_administrador = VentanaAdministrador(self)
        self.ventana_administrador.protocol(
            "WM_DELETE_WINDOW",
            lambda: (self.ventana_administrador.destroy(), setattr(self, "ventana_administrador", None))
        )

    def abrir_docente(self, usuario_docente):
        if self.ventana_docente and self.ventana_docente.winfo_exists():
            self.ventana_docente.deiconify(); self.ventana_docente.lift(); self.ventana_docente.focus_force()
            return
        # Nota: tu VentanaDocente actual solo recibe (master) o (master, usuario). Ajusta si tu firma difiere.
        try:
            self.ventana_docente = VentanaDocente(self, usuario_docente)
        except TypeError:
            # fallback si tu VentanaDocente solo acepta (master)
            self.ventana_docente = VentanaDocente(self)

        self.ventana_docente.protocol(
            "WM_DELETE_WINDOW",
            lambda: (self.ventana_docente.destroy(), setattr(self, "ventana_docente", None))
        )

    def limpiar(self):
        self.entrada_usuario.delete(0, tk.END)
        self.entrada_contrasena.delete(0, tk.END)
        self.entrada_usuario.focus_set()

    def salir(self):
        self.winfo_toplevel().destroy()


class AplicacionLogin(tb.Window):
    def __init__(self):
        super().__init__(themename="flatly")
        self.title("Login")
        self.geometry("520x320")
        self.resizable(False, False)
        contenedor = ttk.Frame(self, padding=16)
        contenedor.pack(fill="both", expand=True)
        ttk.Label(contenedor, text="Sistema de Asistencia", font=("Segoe UI", 12, "bold")).pack(pady=(0,8))
        tarjeta = TarjetaLogin(contenedor)
        tarjeta.pack(expand=True)


if __name__ == "__main__":
    AplicacionLogin().mainloop()
