# EstudiantesAD.py
import tkinter as tk
from ttkbootstrap import ttk
from tkinter import messagebox
from Clases import Estudiante, Eliminador

class EstudiantesAD(ttk.Frame):
    def __init__(self, master, estudiantes: dict, carreras: dict, guardar_estudiantes_cb):
        super().__init__(master, padding=12)
        self.estudiantes = estudiantes
        self.carreras = carreras
        self.guardar_estudiantes_cb = guardar_estudiantes_cb
        self._construir()

    def _construir(self):
        marco_est = ttk.Frame(self)
        marco_est.pack(fill="x", pady=(0,8))
        ttk.Label(marco_est, text="Código:").grid(row=0, column=0, sticky="e", padx=6, pady=6)
        ttk.Label(marco_est, text="Nombre:").grid(row=1, column=0, sticky="e", padx=6, pady=6)
        ttk.Label(marco_est, text="ID Huella:").grid(row=2, column=0, sticky="e", padx=6, pady=6)
        ttk.Label(marco_est, text="Carrera:").grid(row=0, column=2, sticky="e", padx=6, pady=6)
        self.entrada_codigo_est = ttk.Entry(marco_est, width=24)
        self.entrada_nombre_est = ttk.Entry(marco_est, width=24)
        self.entrada_huella_est = ttk.Entry(marco_est, width=24)
        self.combo_carrera_est = ttk.Combobox(marco_est, state="readonly", width=30, values=self._lista_carreras_combo())
        self.entrada_codigo_est.grid(row=0, column=1, padx=6, pady=6)
        self.entrada_nombre_est.grid(row=1, column=1, padx=6, pady=6)
        self.entrada_huella_est.grid(row=2, column=1, padx=6, pady=6)
        self.combo_carrera_est.grid(row=0, column=3, padx=6, pady=6, sticky="w")

        marco_btn_est = ttk.Frame(self)
        marco_btn_est.pack(fill="x", pady=(8,8))
        ttk.Button(marco_btn_est, text="Guardar Estudiante", bootstyle="success", command=self.guardar_estudiante).pack(side="left", padx=4)
        ttk.Button(marco_btn_est, text="Limpiar", bootstyle="info", command=self.limpiar_estudiante).pack(side="left", padx=4)
        ttk.Button(marco_btn_est, text="Eliminar Estudiante", bootstyle="danger", command=self.eliminar_estudiante).pack(side="left", padx=4)

        marco_tabla_est = ttk.Frame(self)
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

        self.refrescar_estudiantes()

    # ---- utilidades idénticas ----
    def _lista_carreras_combo(self):
        return [f"{c.codigo} - {c.nombre}" for c in self.carreras.values()]

    def actualizar_combo_carreras(self):
        self.combo_carrera_est.configure(values=self._lista_carreras_combo())

    # ---- Lógica (idéntica) ----
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
