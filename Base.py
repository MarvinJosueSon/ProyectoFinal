import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap import ttk
from ttkbootstrap.constants import *
from tkinter import messagebox

class TarjetaLogin(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=24, style="card")
        self._construir()

    def _construir(self):
        ttk.Label(self, text="Ingreso al sistema", font=("Segoe UI", 16, "bold")).grid(row=0, column=0, columnspan=3, pady=(0,12))
        ttk.Label(self, text="Usuario").grid(row=1, column=0, sticky="e", padx=6, pady=6)
        ttk.Label(self, text="Contraseña").grid(row=2, column=0, sticky="e", padx=6, pady=6)

        self.entrada_usuario = ttk.Entry(self, width=28)
        self.entrada_contrasena = ttk.Entry(self, show="*", width=28)
        self.entrada_usuario.grid(row=1, column=1, padx=6, pady=6)
        self.entrada_contrasena.grid(row=2, column=1, padx=6, pady=6)

        self.ver_contrasena = tk.BooleanVar(value=False)
        boton_ver = ttk.Checkbutton(self, text="Mostrar", variable=self.ver_contrasena, command=self._alternar_contrasena, bootstyle=SECONDARY)
        boton_ver.grid(row=2, column=2, sticky="w", padx=(0,6))

        panel_botones = ttk.Frame(self)
        panel_botones.grid(row=3, column=0, columnspan=3, pady=(12,0))
        ttk.Button(panel_botones, text="Entrar", bootstyle=PRIMARY, command=self._entrar).pack(side="left", padx=4)
        ttk.Button(panel_botones, text="Limpiar", bootstyle=INFO, command=self._limpiar).pack(side="left", padx=4)
        ttk.Button(panel_botones, text="Salir", bootstyle=DANGER, command=self._salir).pack(side="left", padx=4)

        self.entrada_contrasena.bind("<Return>", lambda e: self._entrar())

    def _alternar_contrasena(self):
        self.entrada_contrasena.configure(show="" if self.ver_contrasena.get() else "*")

    def _entrar(self):
        usuario = self.entrada_usuario.get().strip()
        contrasena = self.entrada_contrasena.get().strip()
        if not usuario or not contrasena:
            messagebox.showwarning("Atención", "Ingresa el usuario y la contraseña.")
            return
        if usuario == "admin" and contrasena == "123":
            self._abrir_admin()
            return
        if usuario == "docente" and contrasena == "123":
            messagebox.showinfo("Acceso", "Ingreso de docente correcto.")
            return
        messagebox.showerror("Error", "Credenciales incorrectas.")

    def _abrir_admin(self):
        admin_win = tb.Toplevel(self)
        admin_win.title("Panel Administrador")
        admin_win.geometry("900x600")
        marco = ttk.Frame(admin_win, padding=16)
        marco.pack(fill="both", expand=True)
        ttk.Label(marco, text="Panel del Administrador", font=("Segoe UI", 16, "bold")).pack(anchor="w")

    def _limpiar(self):
        self.entrada_usuario.delete(0, tk.END)
        self.entrada_contrasena.delete(0, tk.END)
        self.entrada_usuario.focus_set()

    def _salir(self):
        self.winfo_toplevel().destroy()

class AppLogin(tb.Window):
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
    AppLogin().mainloop()
