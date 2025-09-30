# Admin_UI.py
import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap import ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from Clases import Curso, Eliminador

class VentanaAdministrador(tb.Toplevel):
    def __init__(self, master, cursos, guardar_cursos_cb):
        super().__init__(master)
        self.title("Administrador")
        self.geometry("980x640")
        self.cursos = cursos
        self.guardar_cursos_cb = guardar_cursos_cb
        self.construir()

    def construir(self):
        contenedor = ttk.Frame(self, padding=12)
        contenedor.pack(fill="both", expand=True)

        pestañas = ttk.Notebook(contenedor)
        pestañas.pack(fill="both", expand=True)

        pestaña_cursos = ttk.Frame(pestañas, padding=12)
        pestaña_docentes = ttk.Frame(pestañas, padding=12)
        pestaña_alumnos = ttk.Frame(pestañas, padding=12)
        pestañas.add(pestaña_cursos, text="Cursos")
        pestañas.add(pestaña_docentes, text="Docentes")
        pestañas.add(pestaña_alumnos, text="Alumnos")

        marco_formulario = ttk.Frame(pestaña_cursos)
        marco_formulario.pack(fill="x", pady=(0,8))
        ttk.Label(marco_formulario, text="ID del curso:").grid(row=0, column=0, sticky="e", padx=6, pady=6)
        ttk.Label(marco_formulario, text="Nombre del curso:").grid(row=1, column=0, sticky="e", padx=6, pady=6)
        self.entrada_id_curso = ttk.Entry(marco_formulario, width=30)
        self.entrada_nombre_curso = ttk.Entry(marco_formulario, width=40)
        self.entrada_id_curso.grid(row=0, column=1, padx=6, pady=6)
        self.entrada_nombre_curso.grid(row=1, column=1, padx=6, pady=6)

        marco_botones = ttk.Frame(pestaña_cursos)
        marco_botones.pack(fill="x", pady=(0,8))
        ttk.Button(marco_botones, text="Guardar", bootstyle=SUCCESS, command=self.guardar_curso).pack(side="left", padx=4)
        ttk.Button(marco_botones, text="Eliminar", bootstyle=DANGER, command=self.eliminar_curso).pack(side="left", padx=4)
        ttk.Button(marco_botones, text="Limpiar", bootstyle=INFO, command=self.limpiar_curso).pack(side="left", padx=4)
        ttk.Button(marco_botones, text="Refrescar", bootstyle=SECONDARY, command=self.refrescar_cursos).pack(side="left", padx=4)

        marco_tabla = ttk.Frame(pestaña_cursos)
        marco_tabla.pack(fill="both", expand=True)
        self.tabla_cursos = ttk.Treeview(marco_tabla, columns=("id","nombre"), show="headings")
        self.tabla_cursos.heading("id", text="ID")
        self.tabla_cursos.heading("nombre", text="Nombre")
        self.tabla_cursos.column("id", width=160, anchor="center")
        self.tabla_cursos.column("nombre", width=520, anchor="w")
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
            seleccion = self.tabla_cursos.selection()
            if seleccion:
                valores = self.tabla_cursos.item(seleccion[0], "values")
                if valores:
                    id_curso = valores[0]
        if not id_curso:
            messagebox.showwarning("Atención", "Selecciona o ingresa el ID del curso a eliminar.")
            return
        confirmar = messagebox.askyesno("Confirmación", f"¿Eliminar el curso '{id_curso}'?")
        if not confirmar:
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
        for curso in self.cursos.values():
            self.tabla_cursos.insert("", "end", values=(curso.id_curso, curso.nombre))

    def seleccionar_curso(self, _):
        seleccion = self.tabla_cursos.selection()
        if not seleccion:
            return
        valores = self.tabla_cursos.item(seleccion[0], "values")
        self.entrada_id_curso.delete(0, tk.END)
        self.entrada_nombre_curso.delete(0, tk.END)
        self.entrada_id_curso.insert(0, valores[0])
        self.entrada_nombre_curso.insert(0, valores[1])
