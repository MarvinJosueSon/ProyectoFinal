# Base.py
import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap import ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from CargarGuardar import (
    guardar_cursos, cargar_cursos,
    guardar_docentes, cargar_docentes,
    guardar_carreras, cargar_carreras,
    guardar_estudiantes, cargar_estudiantes
)
from Admin_UI import VentanaAdministrador
from Docente_UI import VentanaDocente

import os
print("CWD =>", os.getcwd())
print("docentes.txt ABS =>", os.path.abspath("docentes.txt"))
from CargarGuardar import cargar_docentes
d = cargar_docentes()
print("Usuarios leídos:", [getattr(x, "usuario", None) for x in d.values()])
print("Contraseñas:", [getattr(x, "contrasena", None) for x in d.values()])

class TarjetaLogin(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=24, style="card")
        self.ventana_administrador = None
        self.ventana_docente = None
        self.cursos = cargar_cursos()
        self.docentes = cargar_docentes()
        self.carreras = cargar_carreras()
        self.estudiantes = cargar_estudiantes()
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
        ttk.Checkbutton(self, text="Mostrar", variable=self.ver_contrasena, command=self.alternar_contrasena, bootstyle=SECONDARY).grid(row=2, column=2, sticky="w", padx=(0,6))
        marco_botones = ttk.Frame(self)
        marco_botones.grid(row=3, column=0, columnspan=3, pady=(12,0))
        ttk.Button(marco_botones, text="Entrar", bootstyle=PRIMARY, command=self.entrar).pack(side="left", padx=4)
        ttk.Button(marco_botones, text="Limpiar", bootstyle=INFO, command=self.limpiar).pack(side="left", padx=4)
        ttk.Button(marco_botones, text="Salir", bootstyle=DANGER, command=self.salir).pack(side="left", padx=4)
        self.entrada_contrasena.bind("<Return>", lambda e: self.entrar())

    def alternar_contrasena(self):
        self.entrada_contrasena.configure(show="" if self.ver_contrasena.get() else "*")

    def entrar(self):
        from CargarGuardar import cargar_docentes

        usuario = self.entrada_usuario.get().strip()
        contrasena = self.entrada_contrasena.get().strip()

        if not usuario or not contrasena:
            messagebox.showwarning("Atención", "Ingresa el usuario y la contraseña.")
            return


        if usuario == "admin" and contrasena == "123":
            self.abrir_administrador()
            return


        self.docentes = cargar_docentes()


        for d in self.docentes.values():

            if d.usuario.strip() == usuario and d.contrasena.strip() == contrasena:
                self.abrir_docente(usuario)
                return

        messagebox.showerror("Error", "Credenciales incorrectas.")

    def _credenciales_en_archivo(self, usuario, contrasena):
        try:
            with open("docentes.txt", "r", encoding="utf-8") as f:
                for ln in f:
                    ln = ln.strip()
                    if not ln:
                        continue
                    partes = ln.split("|")
                    if len(partes) >= 5:
                        # formato: codigo|nombre|id_huella|usuario|contrasena
                        if partes[3] == usuario and partes[4] == contrasena:
                            return True
        except FileNotFoundError:
            pass
        return False
    def abrir_administrador(self):
        if self.ventana_administrador and self.ventana_administrador.winfo_exists():
            self.ventana_administrador.deiconify(); self.ventana_administrador.lift(); self.ventana_administrador.focus_force()
            return
        self.ventana_administrador = VentanaAdministrador(
            self,
            self.cursos, self.docentes, self.carreras, self.estudiantes,
            guardar_cursos, guardar_docentes, guardar_carreras, guardar_estudiantes,
            on_docentes_actualizados=self.actualizar_docentes
        )
        self.ventana_administrador.protocol("WM_DELETE_WINDOW", lambda: (self.ventana_administrador.destroy(), setattr(self, "ventana_administrador", None)))

    def actualizar_docentes(self, nuevos_dic):
        self.docentes = nuevos_dic

    def abrir_docente(self, usuario_docente):
        if self.ventana_docente and self.ventana_docente.winfo_exists():
            self.ventana_docente.deiconify(); self.ventana_docente.lift(); self.ventana_docente.focus_force()
            return
        self.ventana_docente = VentanaDocente(self, self.cursos, self.estudiantes, usuario_docente)
        self.ventana_docente.protocol("WM_DELETE_WINDOW", lambda: (self.ventana_docente.destroy(), setattr(self, "ventana_docente", None)))

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
