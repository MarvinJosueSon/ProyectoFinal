# CursosAD.py
import tkinter as tk
from ttkbootstrap import ttk
from tkinter import messagebox
from Clases import Curso, Eliminador

class CursosAD(ttk.Frame):
    def __init__(self, master, cursos: dict, guardar_cursos_cb):
        super().__init__(master, padding=12)
        self.cursos = cursos
        self.guardar_cursos_cb = guardar_cursos_cb
        self._construir()

    def _construir(self):
        marco_formulario = ttk.Frame(self)
        marco_formulario.pack(fill="x", pady=(0,8))
        ttk.Label(marco_formulario, text="ID del curso:").grid(row=0, column=0, sticky="e", padx=6, pady=6)
        ttk.Label(marco_formulario, text="Nombre del curso:").grid(row=1, column=0, sticky="e", padx=6, pady=6)
        self.entrada_id_curso = ttk.Entry(marco_formulario, width=30)
        self.entrada_nombre_curso = ttk.Entry(marco_formulario, width=40)
        self.entrada_id_curso.grid(row=0, column=1, padx=6, pady=6)
        self.entrada_nombre_curso.grid(row=1, column=1, padx=6, pady=6)

        marco_botones = ttk.Frame(self)
        marco_botones.pack(fill="x", pady=(0,8))
        ttk.Button(marco_botones, text="Guardar", bootstyle="success", command=self.guardar_curso).pack(side="left", padx=4)
        ttk.Button(marco_botones, text="Eliminar", bootstyle="danger", command=self.eliminar_curso).pack(side="left", padx=4)
        ttk.Button(marco_botones, text="Limpiar", bootstyle="info", command=self.limpiar_curso).pack(side="left", padx=4)
        ttk.Button(marco_botones, text="Refrescar", bootstyle="secondary", command=self.refrescar_cursos).pack(side="left", padx=4)

        marco_tabla = ttk.Frame(self)
        marco_tabla.pack(fill="both", expand=True)
        self.tabla_cursos = ttk.Treeview(marco_tabla, columns=("id","nombre"), show="headings")
        self.tabla_cursos.heading("id", text="ID")
        self.tabla_cursos.heading("nombre", text="Nombre")
        self.tabla_cursos.column("id", width=180, anchor="center")
        self.tabla_cursos.column("nombre", width=600, anchor="w")
        barra_scroll = ttk.Scrollbar(marco_tabla, orient="vertical", command=self.tabla_cursos.yview)
        self.tabla_cursos.configure(yscrollcommand=barra_scroll.set)
        self.tabla_cursos.pack(side="left", fill="both", expand=True)
        barra_scroll.pack(side="right", fill="y")
        self.tabla_cursos.bind("<<TreeviewSelect>>", self.seleccionar_curso)

        self.refrescar_cursos()


    def guardar_curso(self):
        id_curso = self.entrada_id_curso.get().strip()
        nombre = self.entrada_nombre_curso.get().strip()
        if not id_curso or not nombre:
            messagebox.showwarning("Atención", "Completa ID y Nombre del curso.")
            return
        if ":" in id_curso or ":" in nombre:
            messagebox.showwarning("Atención", "No usar ':' en los campos.")
            return
        if id_curso in self.cursos:
            messagebox.showerror("Error", "El ID del curso ya existe.")
            return
        self.cursos[id_curso] = Curso(id_curso, nombre)
        self.guardar_cursos_cb(self.cursos)
        self.refrescar_cursos()
        messagebox.showinfo("Confirmación", f"Curso creado: {id_curso} - {nombre}")
        self.limpiar_curso()

    def eliminar_curso(self):
        id_curso = self.entrada_id_curso.get().strip()
        if not id_curso:
            sel = self.tabla_cursos.selection()
            if sel:
                vals = self.tabla_cursos.item(sel[0], "values")
                if vals:
                    id_curso = vals[0]
        if not id_curso:
            messagebox.showwarning("Atención", "Selecciona o ingresa el ID del curso a eliminar.")
            return
        if not messagebox.askyesno("Confirmación", f"¿Eliminar el curso '{id_curso}'?"):
            return
        eliminador = Eliminador(self.cursos)
        if eliminador.eliminar(id_curso):
            self.guardar_cursos_cb(self.cursos)
            self.refrescar_cursos()
            self.limpiar_curso()
            messagebox.showinfo("Confirmación", f"Curso eliminado: {id_curso}")
        else:
            messagebox.showerror("Error", "No existe un curso con ese ID.")

    def limpiar_curso(self):
        self.entrada_id_curso.delete(0, tk.END)
        self.entrada_nombre_curso.delete(0, tk.END)
        self.entrada_id_curso.focus_set()

    def refrescar_cursos(self):
        for iid in self.tabla_cursos.get_children():
            self.tabla_cursos.delete(iid)
        for c in self.cursos.values():
            self.tabla_cursos.insert("", "end", values=(c.id_curso, c.nombre))

    def seleccionar_curso(self, _):
        sel = self.tabla_cursos.selection()
        if not sel:
            return
        vals = self.tabla_cursos.item(sel[0], "values")
        self.entrada_id_curso.delete(0, tk.END)
        self.entrada_nombre_curso.delete(0, tk.END)
        self.entrada_id_curso.insert(0, vals[0])
        self.entrada_nombre_curso.insert(0, vals[1])
