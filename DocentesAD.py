# DocentesAD.py
import tkinter as tk
from ttkbootstrap import ttk
from tkinter import messagebox
from Clases import Docente
from DB_Manager import (
    listar_docentes, obtener_docente_por_codigo,
    insertar_docente, actualizar_docente, eliminar_docente
)

class DocentesAD(ttk.Frame):
    def __init__(self, master, docentes=None, guardar_docentes_cb=None, on_docentes_actualizados=None):
        super().__init__(master, padding=12)
        self._construir()

    def _construir(self):
        marco_doc = ttk.Frame(self)
        marco_doc.pack(fill="x", pady=(0,8))

        ttk.Label(marco_doc, text="Código:").grid(row=0, column=0, sticky="e", padx=6, pady=6)
        ttk.Label(marco_doc, text="Nombre:").grid(row=1, column=0, sticky="e", padx=6, pady=6)
        ttk.Label(marco_doc, text="ID Huella:").grid(row=2, column=0, sticky="e", padx=6, pady=6)
        ttk.Label(marco_doc, text="Usuario:").grid(row=0, column=2, sticky="e", padx=6, pady=6)
        ttk.Label(marco_doc, text="Contraseña:").grid(row=1, column=2, sticky="e", padx=6, pady=6)

        self.entrada_codigo_doc = ttk.Entry(marco_doc, width=22)
        self.entrada_nombre_doc = ttk.Entry(marco_doc, width=22)
        self.entrada_huella_doc = ttk.Entry(marco_doc, width=22)
        self.entrada_usuario_doc = ttk.Entry(marco_doc, width=22)
        self.entrada_contrasena_doc = ttk.Entry(marco_doc, width=22, show="*")

        self.entrada_codigo_doc.grid(row=0, column=1, padx=6, pady=6)
        self.entrada_nombre_doc.grid(row=1, column=1, padx=6, pady=6)
        self.entrada_huella_doc.grid(row=2, column=1, padx=6, pady=6)
        self.entrada_usuario_doc.grid(row=0, column=3, padx=6, pady=6)
        self.entrada_contrasena_doc.grid(row=1, column=3, padx=6, pady=6)

        # Botones
        marco_botones_doc = ttk.Frame(self)
        marco_botones_doc.pack(fill="x", pady=(8,8))
        ttk.Button(marco_botones_doc, text="Guardar Docente", bootstyle="success", command=self.guardar_docente).pack(side="left", padx=4)
        ttk.Button(marco_botones_doc, text="Actualizar", bootstyle="secondary", command=self.actualizar_docente).pack(side="left", padx=4)
        ttk.Button(marco_botones_doc, text="Eliminar Docente", bootstyle="danger", command=self.eliminar_docente).pack(side="left", padx=4)
        ttk.Button(marco_botones_doc, text="Limpiar", bootstyle="info", command=self.limpiar_docente).pack(side="left", padx=4)
        ttk.Button(marco_botones_doc, text="Refrescar", command=self.refrescar_docentes).pack(side="left", padx=4)

        # Tabla
        marco_tabla_doc = ttk.Frame(self)
        marco_tabla_doc.pack(fill="both", expand=True)

        self.tabla_docentes = ttk.Treeview(
            marco_tabla_doc,
            columns=("codigo","nombre","usuario","contrasena","huella"),
            show="headings"
        )
        self.tabla_docentes.heading("codigo", text="Código")
        self.tabla_docentes.heading("nombre", text="Nombre")
        self.tabla_docentes.heading("usuario", text="Usuario")
        self.tabla_docentes.heading("contrasena", text="Contraseña")
        self.tabla_docentes.heading("huella", text="ID Huella")

        self.tabla_docentes.column("codigo", width=120, anchor="center")
        self.tabla_docentes.column("nombre", width=260, anchor="w")
        self.tabla_docentes.column("usuario", width=160, anchor="w")
        self.tabla_docentes.column("contrasena", width=160, anchor="w")
        self.tabla_docentes.column("huella", width=100, anchor="center")

        barra_doc = ttk.Scrollbar(marco_tabla_doc, orient="vertical", command=self.tabla_docentes.yview)
        self.tabla_docentes.configure(yscrollcommand=barra_doc.set)
        self.tabla_docentes.pack(side="left", fill="both", expand=True)
        barra_doc.pack(side="right", fill="y")

        self.tabla_docentes.bind("<<TreeviewSelect>>", self.seleccionar_docente)

        self.refrescar_docentes()

    # ------------------ CRUD (SQLite) ------------------
    def guardar_docente(self):
        codigo = self.entrada_codigo_doc.get().strip()
        nombre = self.entrada_nombre_doc.get().strip()
        id_huella = self.entrada_huella_doc.get().strip()
        usuario = self.entrada_usuario_doc.get().strip()
        contrasena = self.entrada_contrasena_doc.get().strip()

        if not codigo or not nombre or not id_huella or not usuario or not contrasena:
            messagebox.showwarning("Atención", "Completa todos los campos del docente.")
            return
        if not id_huella.isdigit():
            messagebox.showwarning("Atención", "ID Huella debe ser numérico.")
            return
        if obtener_docente_por_codigo(codigo):
            messagebox.showerror("Error", "El código de docente ya existe.")
            return

        try:
            insertar_docente(Docente(codigo, nombre, int(id_huella), usuario, contrasena))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar: {e}")
            return

        self.refrescar_docentes()
        messagebox.showinfo("Confirmación", f"Docente creado: {codigo} - {nombre}")
        self.limpiar_docente()

    def actualizar_docente(self):
        sel = self.tabla_docentes.selection()
        if not sel:
            messagebox.showwarning("Atención", "Selecciona un docente en la tabla para actualizar.")
            return

        vals = self.tabla_docentes.item(sel[0], "values")
        old_codigo = vals[0]

        codigo = self.entrada_codigo_doc.get().strip()
        nombre = self.entrada_nombre_doc.get().strip()
        id_huella = self.entrada_huella_doc.get().strip()
        usuario = self.entrada_usuario_doc.get().strip()
        contrasena = self.entrada_contrasena_doc.get().strip()

        if not codigo or not nombre or not id_huella or not usuario or not contrasena:
            messagebox.showwarning("Atención", "Completa los campos antes de actualizar.")
            return
        if not id_huella.isdigit():
            messagebox.showwarning("Atención", "ID Huella debe ser numérico.")
            return

        # Si cambia el código, valida que el nuevo no exista
        if old_codigo != codigo and obtener_docente_por_codigo(codigo):
            messagebox.showerror("Error", "El nuevo código ya existe.")
            return

        try:
            actualizar_docente(old_codigo, Docente(codigo, nombre, int(id_huella), usuario, contrasena))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar: {e}")
            return

        self.refrescar_docentes()
        messagebox.showinfo("Confirmación", f"Docente actualizado: {codigo}")

    def eliminar_docente(self):
        sel = self.tabla_docentes.selection()
        if not sel:
            messagebox.showwarning("Atención", "Selecciona un docente en la tabla para eliminar.")
            return
        codigo = self.tabla_docentes.item(sel[0], "values")[0]
        if not messagebox.askyesno("Confirmación", f"¿Eliminar el docente '{codigo}'?"):
            return

        try:
            eliminar_docente(codigo)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar: {e}")
            return

        self.refrescar_docentes()
        self.limpiar_docente()
        messagebox.showinfo("Confirmación", f"Docente eliminado: {codigo}")

    # ------------------ Helpers UI ------------------
    def limpiar_docente(self):
        self.entrada_codigo_doc.delete(0, tk.END)
        self.entrada_nombre_doc.delete(0, tk.END)
        self.entrada_huella_doc.delete(0, tk.END)
        self.entrada_usuario_doc.delete(0, tk.END)
        self.entrada_contrasena_doc.delete(0, tk.END)
        self.entrada_codigo_doc.focus_set()

    def refrescar_docentes(self):
        for iid in self.tabla_docentes.get_children():
            self.tabla_docentes.delete(iid)
        for d in listar_docentes():
            self.tabla_docentes.insert("", "end",
                values=(d.codigo, d.nombre, d.usuario, d.contrasena, d.id_huella)
            )

    def seleccionar_docente(self, _):
        sel = self.tabla_docentes.selection()
        if not sel:
            return
        vals = self.tabla_docentes.item(sel[0], "values")
        self.entrada_codigo_doc.delete(0, tk.END)
        self.entrada_nombre_doc.delete(0, tk.END)
        self.entrada_huella_doc.delete(0, tk.END)
        self.entrada_usuario_doc.delete(0, tk.END)
        self.entrada_contrasena_doc.delete(0, tk.END)

        self.entrada_codigo_doc.insert(0, vals[0])
        self.entrada_nombre_doc.insert(0, vals[1])
        self.entrada_usuario_doc.insert(0, vals[2])
        self.entrada_contrasena_doc.insert(0, vals[3])
        self.entrada_huella_doc.insert(0, vals[4])
