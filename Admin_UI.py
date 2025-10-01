# Admin_UI.py
import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap import ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from Clases import Curso, Docente, Eliminador, Carrera, Estudiante

class VentanaAdministrador(tb.Toplevel):
    def __init__(self, master, cursos, docentes, carreras, estudiantes,
                 guardar_cursos_cb, guardar_docentes_cb, guardar_carreras_cb, guardar_estudiantes_cb):
        super().__init__(master)
        self.title("Administrador")
        self.geometry("1100x760")
        self.cursos = cursos
        self.docentes = docentes
        self.carreras = carreras
        self.estudiantes = estudiantes
        self.guardar_cursos_cb = guardar_cursos_cb
        self.guardar_docentes_cb = guardar_docentes_cb
        self.guardar_carreras_cb = guardar_carreras_cb
        self.guardar_estudiantes_cb = guardar_estudiantes_cb
        self.construir()

    def construir(self):
        contenedor = ttk.Frame(self, padding=12)
        contenedor.pack(fill="both", expand=True)
        pestañas = ttk.Notebook(contenedor)
        pestañas.pack(fill="both", expand=True)

        pestaña_cursos = ttk.Frame(pestañas, padding=12)
        pestaña_docentes = ttk.Frame(pestañas, padding=12)
        pestaña_carreras = ttk.Frame(pestañas, padding=12)
        pestaña_estudiantes = ttk.Frame(pestañas, padding=12)
        pestañas.add(pestaña_cursos, text="Cursos")
        pestañas.add(pestaña_docentes, text="Docentes")
        pestañas.add(pestaña_carreras, text="Carreras")
        pestañas.add(pestaña_estudiantes, text="Estudiantes")

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
        self.tabla_cursos.column("id", width=180, anchor="center")
        self.tabla_cursos.column("nombre", width=600, anchor="w")
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
        marco_botones_doc = ttk.Frame(pestaña_docentes)
        marco_botones_doc.pack(fill="x", pady=(8,8))
        ttk.Button(marco_botones_doc, text="Guardar Docente", bootstyle=SUCCESS, command=self.guardar_docente).pack(side="left", padx=4)
        ttk.Button(marco_botones_doc, text="Limpiar", bootstyle=INFO, command=self.limpiar_docente).pack(side="left", padx=4)
        ttk.Button(marco_botones_doc, text="Eliminar Docente", bootstyle=DANGER, command=self.eliminar_docente).pack(side="left", padx=4)
        marco_tabla_doc = ttk.Frame(pestaña_docentes)
        marco_tabla_doc.pack(fill="both", expand=True)
        self.tabla_docentes = ttk.Treeview(marco_tabla_doc, columns=("codigo","nombre","usuario","huella"), show="headings")
        self.tabla_docentes.heading("codigo", text="Código")
        self.tabla_docentes.heading("nombre", text="Nombre")
        self.tabla_docentes.heading("usuario", text="Usuario")
        self.tabla_docentes.heading("huella", text="ID Huella")
        self.tabla_docentes.column("codigo", width=140, anchor="center")
        self.tabla_docentes.column("nombre", width=300, anchor="w")
        self.tabla_docentes.column("usuario", width=180, anchor="w")
        self.tabla_docentes.column("huella", width=120, anchor="center")
        barra_doc = ttk.Scrollbar(marco_tabla_doc, orient="vertical", command=self.tabla_docentes.yview)
        self.tabla_docentes.configure(yscrollcommand=barra_doc.set)
        self.tabla_docentes.pack(side="left", fill="both", expand=True)
        barra_doc.pack(side="right", fill="y")
        self.tabla_docentes.bind("<<TreeviewSelect>>", self.seleccionar_docente)

        marco_car = ttk.Frame(pestaña_carreras)
        marco_car.pack(fill="x", pady=(0,8))
        ttk.Label(marco_car, text="ID Carrera:").grid(row=0, column=0, sticky="e", padx=6, pady=6)
        ttk.Label(marco_car, text="Nombre Carrera:").grid(row=1, column=0, sticky="e", padx=6, pady=6)
        self.entrada_id_carrera = ttk.Entry(marco_car, width=30)
        self.entrada_nombre_carrera = ttk.Entry(marco_car, width=40)
        self.entrada_id_carrera.grid(row=0, column=1, padx=6, pady=6)
        self.entrada_nombre_carrera.grid(row=1, column=1, padx=6, pady=6)
        marco_btn_car = ttk.Frame(pestaña_carreras)
        marco_btn_car.pack(fill="x", pady=(0,8))
        ttk.Button(marco_btn_car, text="Guardar", bootstyle=SUCCESS, command=self.guardar_carrera).pack(side="left", padx=4)
        ttk.Button(marco_btn_car, text="Eliminar", bootstyle=DANGER, command=self.eliminar_carrera).pack(side="left", padx=4)
        ttk.Button(marco_btn_car, text="Limpiar", bootstyle=INFO, command=self.limpiar_carrera).pack(side="left", padx=4)
        ttk.Button(marco_btn_car, text="Refrescar", bootstyle=SECONDARY, command=self.refrescar_carreras).pack(side="left", padx=4)
        marco_tabla_car = ttk.Frame(pestaña_carreras)
        marco_tabla_car.pack(fill="both", expand=True)
        self.tabla_carreras = ttk.Treeview(marco_tabla_car, columns=("id","nombre"), show="headings")
        self.tabla_carreras.heading("id", text="ID")
        self.tabla_carreras.heading("nombre", text="Nombre")
        self.tabla_carreras.column("id", width=200, anchor="center")
        self.tabla_carreras.column("nombre", width=600, anchor="w")
        barra_car = ttk.Scrollbar(marco_tabla_car, orient="vertical", command=self.tabla_carreras.yview)
        self.tabla_carreras.configure(yscrollcommand=barra_car.set)
        self.tabla_carreras.pack(side="left", fill="both", expand=True)
        barra_car.pack(side="right", fill="y")
        self.tabla_carreras.bind("<<TreeviewSelect>>", self.seleccionar_carrera)

        marco_est = ttk.Frame(pestaña_estudiantes)
        marco_est.pack(fill="x", pady=(0,8))
        ttk.Label(marco_est, text="Código:").grid(row=0, column=0, sticky="e", padx=6, pady=6)
        ttk.Label(marco_est, text="Nombre:").grid(row=1, column=0, sticky="e", padx=6, pady=6)
        ttk.Label(marco_est, text="ID Huella:").grid(row=2, column=0, sticky="e", padx=6, pady=6)
        ttk.Label(marco_est, text="Carrera:").grid(row=0, column=2, sticky="e", padx=6, pady=6)
        self.entrada_codigo_est = ttk.Entry(marco_est, width=24)
        self.entrada_nombre_est = ttk.Entry(marco_est, width=24)
        self.entrada_huella_est = ttk.Entry(marco_est, width=24)
        self.combo_carrera_est = ttk.Combobox(marco_est, state="readonly", width=30, values=self.lista_carreras_combo())
        self.entrada_codigo_est.grid(row=0, column=1, padx=6, pady=6)
        self.entrada_nombre_est.grid(row=1, column=1, padx=6, pady=6)
        self.entrada_huella_est.grid(row=2, column=1, padx=6, pady=6)
        self.combo_carrera_est.grid(row=0, column=3, padx=6, pady=6, sticky="w")
        marco_btn_est = ttk.Frame(pestaña_estudiantes)
        marco_btn_est.pack(fill="x", pady=(8,8))
        ttk.Button(marco_btn_est, text="Guardar Estudiante", bootstyle=SUCCESS, command=self.guardar_estudiante).pack(side="left", padx=4)
        ttk.Button(marco_btn_est, text="Limpiar", bootstyle=INFO, command=self.limpiar_estudiante).pack(side="left", padx=4)
        ttk.Button(marco_btn_est, text="Eliminar Estudiante", bootstyle=DANGER, command=self.eliminar_estudiante).pack(side="left", padx=4)
        marco_tabla_est = ttk.Frame(pestaña_estudiantes)
        marco_tabla_est.pack(fill="both", expand=True)
        self.tabla_estudiantes = ttk.Treeview(marco_tabla_est, columns=("codigo","nombre","huella","carrera"), show="headings")
        self.tabla_estudiantes.heading("codigo", text="Código")
        self.tabla_estudiantes.heading("nombre", text="Nombre")
        self.tabla_estudiantes.heading("huella", text="ID Huella")
        self.tabla_estudiantes.heading("carrera", text="Carrera")
        self.tabla_estudiantes.column("codigo", width=150, anchor="center")
        self.tabla_estudiantes.column("nombre", width=300, anchor="w")
        self.tabla_estudiantes.column("huella", width=120, anchor="center")
        self.tabla_estudiantes.column("carrera", width=260, anchor="w")
        barra_est = ttk.Scrollbar(marco_tabla_est, orient="vertical", command=self.tabla_estudiantes.yview)
        self.tabla_estudiantes.configure(yscrollcommand=barra_est.set)
        self.tabla_estudiantes.pack(side="left", fill="both", expand=True)
        barra_est.pack(side="right", fill="y")
        self.tabla_estudiantes.bind("<<TreeviewSelect>>", self.seleccionar_estudiante)

        self.refrescar_cursos()
        self.refrescar_docentes()
        self.refrescar_carreras()
        self.refrescar_estudiantes()

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
        self.docentes[codigo] = Docente(codigo, nombre, int(id_huella), usuario, contrasena)
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
        self.entrada_codigo_doc.focus_set()

    def refrescar_docentes(self):
        for iid in self.tabla_docentes.get_children():
            self.tabla_docentes.delete(iid)
        for d in self.docentes.values():
            self.tabla_docentes.insert("", "end", values=(d.codigo, d.nombre, d.usuario, d.id_huella))

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
        self.entrada_huella_doc.insert(0, vals[3])

    def eliminar_docente(self):
        codigo = self.entrada_codigo_doc.get().strip()
        if not codigo:
            sel = self.tabla_docentes.selection()
            if sel:
                vals = self.tabla_docentes.item(sel[0], "values")
                if vals:
                    codigo = vals[0]
        if not codigo:
            messagebox.showwarning("Atención", "Selecciona o ingresa el código del docente a eliminar.")
            return
        if not messagebox.askyesno("Confirmación", f"¿Eliminar el docente '{codigo}'?"):
            return
        eliminador = Eliminador(self.docentes)
        if eliminador.eliminar(codigo):
            self.guardar_docentes_cb(self.docentes)
            self.refrescar_docentes()
            self.limpiar_docente()
            messagebox.showinfo("Confirmación", f"Docente eliminado: {codigo}")
        else:
            messagebox.showerror("Error", "No existe un docente con ese código.")

    def guardar_carrera(self):
        codigo = self.entrada_id_carrera.get().strip()
        nombre = self.entrada_nombre_carrera.get().strip()
        if not codigo or not nombre:
            messagebox.showwarning("Atención", "Completa ID y Nombre de la carrera.")
            return
        if ":" in codigo or ":" in nombre:
            messagebox.showwarning("Atención", "No usar ':' en los campos.")
            return
        if codigo in self.carreras:
            messagebox.showerror("Error", "El ID de la carrera ya existe.")
            return
        self.carreras[codigo] = Carrera(codigo, nombre)
        self.guardar_carreras_cb(self.carreras)
        self.refrescar_carreras()
        self.actualizar_combo_carreras_estudiantes()
        messagebox.showinfo("Confirmación", f"Carrera creada: {codigo} - {nombre}")
        self.limpiar_carrera()

    def eliminar_carrera(self):
        codigo = self.entrada_id_carrera.get().strip()
        if not codigo:
            sel = self.tabla_carreras.selection()
            if sel:
                vals = self.tabla_carreras.item(sel[0], "values")
                if vals:
                    codigo = vals[0]
        if not codigo:
            messagebox.showwarning("Atención", "Selecciona o ingresa el ID de la carrera a eliminar.")
            return
        if not messagebox.askyesno("Confirmación", f"¿Eliminar la carrera '{codigo}'?"):
            return
        eliminador = Eliminador(self.carreras)
        if eliminador.eliminar(codigo):
            self.guardar_carreras_cb(self.carreras)
            self.refrescar_carreras()
            self.actualizar_combo_carreras_estudiantes()
            messagebox.showinfo("Confirmación", f"Carrera eliminada: {codigo}")
        else:
            messagebox.showerror("Error", "No existe una carrera con ese ID.")

    def limpiar_carrera(self):
        self.entrada_id_carrera.delete(0, tk.END)
        self.entrada_nombre_carrera.delete(0, tk.END)
        self.entrada_id_carrera.focus_set()

    def refrescar_carreras(self):
        for iid in self.tabla_carreras.get_children():
            self.tabla_carreras.delete(iid)
        for c in self.carreras.values():
            self.tabla_carreras.insert("", "end", values=(c.codigo, c.nombre))

    def seleccionar_carrera(self, _):
        sel = self.tabla_carreras.selection()
        if not sel:
            return
        vals = self.tabla_carreras.item(sel[0], "values")
        self.entrada_id_carrera.delete(0, tk.END)
        self.entrada_nombre_carrera.delete(0, tk.END)
        self.entrada_id_carrera.insert(0, vals[0])
        self.entrada_nombre_carrera.insert(0, vals[1])

    def lista_carreras_combo(self):
        return [f"{c.codigo} - {c.nombre}" for c in self.carreras.values()]

    def actualizar_combo_carreras_estudiantes(self):
        self.combo_carrera_est.configure(values=self.lista_carreras_combo())

    def guardar_estudiante(self):
        codigo = self.entrada_codigo_est.get().strip()
        nombre = self.entrada_nombre_est.get().strip()
        id_huella = self.entrada_huella_est.get().strip()
        sel_car = self.combo_carrera_est.get().strip()
        if not codigo or not nombre or not id_huella or not sel_car:
            messagebox.showwarning("Atención", "Completa todos los campos del estudiante.")
            return
        if not id_huella.isdigit():
            messagebox.showwarning("Atención", "ID Huella debe ser numérico.")
            return
        id_carrera = sel_car.split(" - ", 1)[0]
        if codigo in self.estudiantes:
            messagebox.showerror("Error", "El código del estudiante ya existe.")
            return
        self.estudiantes[codigo] = Estudiante(codigo, nombre, int(id_huella), id_carrera)
        self.guardar_estudiantes_cb(self.estudiantes)
        self.refrescar_estudiantes()
        messagebox.showinfo("Confirmación", f"Estudiante creado: {codigo} - {nombre}")
        self.limpiar_estudiante()

    def limpiar_estudiante(self):
        self.entrada_codigo_est.delete(0, tk.END)
        self.entrada_nombre_est.delete(0, tk.END)
        self.entrada_huella_est.delete(0, tk.END)
        self.combo_carrera_est.set("")
        self.entrada_codigo_est.focus()

    def refrescar_estudiantes(self):
        for iid in self.tabla_estudiantes.get_children():
            self.tabla_estudiantes.delete(iid)
        for e in self.estudiantes.values():
            nom_carrera = self.carreras[e.id_carrera].nombre if e.id_carrera in self.carreras else e.id_carrera
            self.tabla_estudiantes.insert("", "end", values=(e.codigo, e.nombre, e.id_huella, f"{e.id_carrera} - {nom_carrera}"))

    def seleccionar_estudiante(self, _):
        sel = self.tabla_estudiantes.selection()
        if not sel:
            return
        vals = self.tabla_estudiantes.item(sel[0], "values")
        self.entrada_codigo_est.delete(0, tk.END)
        self.entrada_nombre_est.delete(0, tk.END)
        self.entrada_huella_est.delete(0, tk.END)
        self.combo_carrera_est.set("")
        self.entrada_codigo_est.insert(0, vals[0])
        self.entrada_nombre_est.insert(0, vals[1])
        self.entrada_huella_est.insert(0, vals[2])
        self.combo_carrera_est.set(vals[3])

    def eliminar_estudiante(self):
        codigo = self.entrada_codigo_est.get().strip()
        if not codigo:
            sel = self.tabla_estudiantes.selection()
            if sel:
                vals = self.tabla_estudiantes.item(sel[0], "values")
                if vals:
                    codigo = vals[0]
        if not codigo:
            messagebox.showwarning("Atención", "Selecciona o ingresa el código del estudiante a eliminar.")
            return
        if not messagebox.askyesno("Confirmación", f"¿Eliminar el estudiante '{codigo}'?"):
            return
        eliminador = Eliminador(self.estudiantes)
        if eliminador.eliminar(codigo):
            self.guardar_estudiantes_cb(self.estudiantes)
            self.refrescar_estudiantes()
            self.limpiar_estudiante()
            messagebox.showinfo("Confirmación", f"Estudiante eliminado: {codigo}")
        else:
            messagebox.showerror("Error", "No existe un estudiante con ese código.")
