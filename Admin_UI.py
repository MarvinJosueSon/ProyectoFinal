# Admin_UI.py
import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap import ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from Clases import Curso, Docente, Eliminador

class VentanaAdministrador(tb.Toplevel):
    def __init__(self, master, cursos, docentes, guardar_cursos_cb, guardar_docentes_cb):
        super().__init__(master)
        self.title("Administrador")
        self.geometry("1000x700")
        self.cursos = cursos
        self.docentes = docentes
        self.guardar_cursos_cb = guardar_cursos_cb
        self.guardar_docentes_cb = guardar_docentes_cb
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

        marco_doc = ttk.Frame(pestaña_docentes)
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

        marco_lista = ttk.Frame(pestaña_docentes)
        marco_lista.pack(fill="x", pady=(0,8))
        ttk.Label(marco_lista, text="Cursos del docente:").pack(anchor="w")
        self.lista_cursos_doc = tk.Listbox(marco_lista, selectmode="extended", height=8)
        self.lista_cursos_doc.pack(fill="x")

        marco_botones_doc = ttk.Frame(pestaña_docentes)
        marco_botones_doc.pack(fill="x", pady=(8,8))
        ttk.Button(marco_botones_doc, text="Guardar Docente", bootstyle=SUCCESS, command=self.guardar_docente).pack(side="left", padx=4)
        ttk.Button(marco_botones_doc, text="Limpiar", bootstyle=INFO, command=self.limpiar_docente).pack(side="left", padx=4)
        ttk.Button(marco_botones_doc, text="Eliminar Docente", bootstyle=DANGER, command=self.eliminar_docente).pack(side="left", padx=4)

        marco_tabla_doc = ttk.Frame(pestaña_docentes)
        marco_tabla_doc.pack(fill="both", expand=True)
        self.tabla_docentes = ttk.Treeview(marco_tabla_doc, columns=("codigo","nombre","usuario","huella","cursos"), show="headings")
        self.tabla_docentes.heading("codigo", text="Código")
        self.tabla_docentes.heading("nombre", text="Nombre")
        self.tabla_docentes.heading("usuario", text="Usuario")
        self.tabla_docentes.heading("huella", text="ID Huella")
        self.tabla_docentes.heading("cursos", text="Cursos")
        self.tabla_docentes.column("codigo", width=120, anchor="center")
        self.tabla_docentes.column("nombre", width=220, anchor="w")
        self.tabla_docentes.column("usuario", width=160, anchor="w")
        self.tabla_docentes.column("huella", width=100, anchor="center")
        self.tabla_docentes.column("cursos", width=300, anchor="w")
        barra_doc = ttk.Scrollbar(marco_tabla_doc, orient="vertical", command=self.tabla_docentes.yview)
        self.tabla_docentes.configure(yscrollcommand=barra_doc.set)
        self.tabla_docentes.pack(side="left", fill="both", expand=True)
        barra_doc.pack(side="right", fill="y")
        self.tabla_docentes.bind("<<TreeviewSelect>>", self.seleccionar_docente)

        self.refrescar_cursos()
        self.refrescar_docentes()

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
        self.refrescar_lista_cursos_doc()

    def seleccionar_curso(self, _):
        seleccion = self.tabla_cursos.selection()
        if not seleccion:
            return
        valores = self.tabla_cursos.item(seleccion[0], "values")
        self.entrada_id_curso.delete(0, tk.END)
        self.entrada_nombre_curso.delete(0, tk.END)
        self.entrada_id_curso.insert(0, valores[0])
        self.entrada_nombre_curso.insert(0, valores[1])

    def refrescar_lista_cursos_doc(self):
        self.lista_cursos_doc.delete(0, tk.END)
        for cid, c in self.cursos.items():
            self.lista_cursos_doc.insert(tk.END, f"{cid} - {c.nombre}")

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
        if codigo in self.docentes:
            messagebox.showerror("Error", "El código de docente ya existe.")
            return
        seleccion = [self.lista_cursos_doc.get(i) for i in self.lista_cursos_doc.curselection()]
        cursos_sel = {}
        for item in seleccion:
            cid = item.split(" - ", 1)[0]
            if cid in self.cursos:
                cursos_sel[cid] = self.cursos[cid].nombre
        self.docentes[codigo] = Docente(codigo, nombre, int(id_huella), usuario, contrasena, cursos_sel)
        self.guardar_docentes_cb(self.docentes)
        self.refrescar_docentes()
        messagebox.showinfo("Confirmación", f"Docente creado: {codigo} - {nombre}")
        self.limpiar_docente()

    def limpiar_docente(self):
        self.entrada_codigo_doc.delete(0, tk.END)
        self.entrada_nombre_doc.delete(0, tk.END)
        self.entrada_huella_doc.delete(0, tk.END)
        self.entrada_usuario_doc.delete(0, tk.END)
        self.entrada_contrasena_doc.delete(0, tk.END)
        self.lista_cursos_doc.selection_clear(0, tk.END)
        self.entrada_codigo_doc.focus_set()

    def refrescar_docentes(self):
        for iid in self.tabla_docentes.get_children():
            self.tabla_docentes.delete(iid)
        for d in self.docentes.values():
            lista_cur = ", ".join([f"{cid}" for cid in d.cursos.keys()])
            self.tabla_docentes.insert("", "end", values=(d.codigo, d.nombre, d.usuario, d.id_huella, lista_cur))

    def seleccionar_docente(self, _):
        seleccion = self.tabla_docentes.selection()
        if not seleccion:
            return
        valores = self.tabla_docentes.item(seleccion[0], "values")
        self.entrada_codigo_doc.delete(0, tk.END)
        self.entrada_nombre_doc.delete(0, tk.END)
        self.entrada_huella_doc.delete(0, tk.END)
        self.entrada_usuario_doc.delete(0, tk.END)
        self.entrada_contrasena_doc.delete(0, tk.END)
        self.entrada_codigo_doc.insert(0, valores[0])
        self.entrada_nombre_doc.insert(0, valores[1])
        self.entrada_usuario_doc.insert(0, valores[2])
        self.entrada_huella_doc.insert(0, valores[3])
        self.lista_cursos_doc.selection_clear(0, tk.END)
        ids = [x.strip() for x in str(valores[4]).split(",") if x.strip()]
        for idx in range(self.lista_cursos_doc.size()):
            texto = self.lista_cursos_doc.get(idx)
            cid = texto.split(" - ", 1)[0]
            if cid in ids:
                self.lista_cursos_doc.selection_set(idx)

    def eliminar_docente(self):
        codigo = self.entrada_codigo_doc.get().strip()
        if not codigo:
            seleccion = self.tabla_docentes.selection()
            if seleccion:
                valores = self.tabla_docentes.item(seleccion[0], "values")
                if valores:
                    codigo = valores[0]
        if not codigo:
            messagebox.showwarning("Atención", "Selecciona o ingresa el código del docente a eliminar.")
            return
        confirmar = messagebox.askyesno("Confirmación", f"¿Eliminar el docente '{codigo}'?")
        if not confirmar:
            return
        eliminador = Eliminador(self.docentes)
        if eliminador.eliminar(codigo):
            self.guardar_docentes_cb(self.docentes)
            self.refrescar_docentes()
            self.limpiar_docente()
            messagebox.showinfo("Confirmación", f"Docente eliminado: {codigo}")
        else:
            messagebox.showerror("Error", "No existe un docente con ese código.")
