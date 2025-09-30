import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap import ttk
from ttkbootstrap.constants import *
from tkinter import messagebox

class LoginCard(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=24, style="card")
        self._build()

    def _build(self):
        ttk.Label(self, text="Ingreso al sistema", font=("Segoe UI", 16, "bold")).grid(row=0, column=0, columnspan=3, pady=(0,12))
        ttk.Label(self, text="Usuario").grid(row=1, column=0, sticky="e", padx=6, pady=6)
        ttk.Label(self, text="Contraseña").grid(row=2, column=0, sticky="e", padx=6, pady=6)

        self.e_usuario = ttk.Entry(self, width=28)
        self.e_pass = ttk.Entry(self, show="*", width=28)
        self.e_usuario.grid(row=1, column=1, padx=6, pady=6)
        self.e_pass.grid(row=2, column=1, padx=6, pady=6)

        self.var_ver = tk.BooleanVar(value=False)
        chk = ttk.Checkbutton(self, text="Mostrar", variable=self.var_ver, command=self._toggle_pass, bootstyle=SECONDARY)
        chk.grid(row=2, column=2, sticky="w", padx=(0,6))

        btns = ttk.Frame(self)
        btns.grid(row=3, column=0, columnspan=3, pady=(12,0))
        ttk.Button(btns, text="Entrar", bootstyle=PRIMARY, command=self._login).pack(side="left", padx=4)
        ttk.Button(btns, text="Limpiar", bootstyle=INFO, command=self._limpiar).pack(side="left", padx=4)
        ttk.Button(btns, text="Salir", bootstyle=DANGER, command=self._salir).pack(side="left", padx=4)

        self.e_pass.bind("<Return>", lambda e: self._login())

    def _toggle_pass(self):
        self.e_pass.configure(show="" if self.var_ver.get() else "*")

    def _login(self):
        usuario = self.e_usuario.get().strip()
        if not usuario:
            messagebox.showwarning("Atención", "Ingresa el usuario y la contraseña.")
            return
        messagebox.showinfo("Acceso", "Esto es solo la interfaz. ")

    def _limpiar(self):
        self.e_usuario.delete(0, tk.END)
        self.e_pass.delete(0, tk.END)
        self.e_usuario.focus_set()

    def _salir(self):
        self.winfo_toplevel().destroy()

class LoginApp(tb.Window):
    def __init__(self):
        super().__init__(themename="flatly")
        self.title("Login")
        self.geometry("520x320")
        self.resizable(False, False)

        cont = ttk.Frame(self, padding=16)
        cont.pack(fill="both", expand=True)

        ttk.Label(cont, text="Sistema de Asistencia", font=("Segoe UI", 12, "bold")).pack(pady=(0,8))
        card = LoginCard(cont)
        card.pack(expand=True)

if __name__ == "__main__":
    LoginApp().mainloop()