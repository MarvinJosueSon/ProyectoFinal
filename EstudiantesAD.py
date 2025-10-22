# EstudiantesAD.py
import tkinter as tk
from ttkbootstrap import ttk
from tkinter import messagebox
from Clases import Estudiante
from DB_Manager import (
    listar_estudiantes, obtener_estudiante, insertar_estudiante,
    actualizar_estudiante, eliminar_estudiante,
    listar_carreras, buscar_estudiantes
)
from Huella import enrolar_huella_con_id
from DB_Manager import huella_en_uso, sugerir_id_huella_libre




class EstudiantesAD(ttk.Frame):
    def __init__(self, master, estudiantes=None, carreras=None, guardar_estudiantes_cb=None):
        super().__init__(master, padding=12)
        self._construir()

    # ------------------- UI -------------------
    def _construir(self):
        # --- Búsqueda ---
        marco_buscar_est = ttk.Frame(self)
        marco_buscar_est.pack(fill="x", pady=(0,8))

        ttk.Label(marco_buscar_est, text="Buscar:").pack(side="left", padx=(0,6))
        self.entrada_buscar_est = ttk.Entry(marco_buscar_est, width=40)
        self.entrada_buscar_est.pack(side="left")
        ttk.Button(marco_buscar_est, text="Limpiar búsqueda", bootstyle="secondary",
                   command=self.limpiar_busqueda_est).pack(side="left", padx=6)

        # Filtrar mientras escribe
        self.entrada_buscar_est.bind("<KeyRelease>", lambda e: self.refrescar_estudiantes())

        marco_est = ttk.Frame(self)
        marco_est.pack(fill="x", pady=(0,8))

        ttk.Label(marco_est, text="Código:").grid(row=0, column=0, sticky="e", padx=6, pady=6)
        ttk.Label(marco_est, text="Nombre:").grid(row=1, column=0, sticky="e", padx=6, pady=6)
        ttk.Label(marco_est, text="ID Huella:").grid(row=2, column=0, sticky="e", padx=6, pady=6)
        ttk.Label(marco_est, text="Carrera:").grid(row=0, column=2, sticky="e", padx=6, pady=6)

        self.entrada_codigo_est = ttk.Entry(marco_est, width=24)
        self.entrada_nombre_est = ttk.Entry(marco_est, width=24)
        self.entrada_huella_est = ttk.Entry(marco_est, width=24)

        self.combo_carrera_est = ttk.Combobox(marco_est, state="readonly", width=30)
        self._cargar_carreras_combo()

        self.entrada_codigo_est.grid(row=0, column=1, padx=6, pady=6)
        self.entrada_nombre_est.grid(row=1, column=1, padx=6, pady=6)
        self.entrada_huella_est.grid(row=2, column=1, padx=6, pady=6)
        btn_capturar = ttk.Button(marco_est, text="Capturar (auto)", bootstyle="info", command=self.capturar_huella_est_auto)
        btn_capturar.grid(row=2, column=2, padx=6, pady=6, sticky="w")

        self.combo_carrera_est.grid(row=0, column=3, padx=6, pady=6, sticky="w")

        marco_btn_est = ttk.Frame(self)
        marco_btn_est.pack(fill="x", pady=(8,8))
        ttk.Button(marco_btn_est, text="Guardar", bootstyle="success", command=self.guardar_estudiante).pack(side="left", padx=4)
        ttk.Button(marco_btn_est, text="Modficar", bootstyle="secondary", command=self.actualizar_estudiante).pack(side="left", padx=4)
        ttk.Button(marco_btn_est, text="Eliminar", bootstyle="danger", command=self.eliminar_estudiante).pack(side="left", padx=4)
        #ttk.Button(marco_btn_est, text="Limpiar", bootstyle="info", command=self.limpiar_estudiante).pack(side="left", padx=4)
        #ttk.Button(marco_btn_est, text="Refrescar", command=self.refrescar_estudiantes).pack(side="left", padx=4)

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

    def capturar_huella_est_auto(self):
        try:
            id_libre = sugerir_id_huella_libre(1, 127)
            if id_libre is None:
                messagebox.showerror("Huella", "No hay IDs libres (1-127).")
                return
            if huella_en_uso(id_libre):
                messagebox.showerror("Huella", f"El ID {id_libre} se ocupó. Intenta de nuevo.")
                return

            messagebox.showinfo("Huella", f"Coloca el dedo en el lector.\nSe usará el ID {id_libre}.")
            ok = enrolar_huella_con_id(id_libre)
            if not ok:
                messagebox.showerror("Huella", "No se pudo enrolar la huella. Intenta de nuevo.")
                return

            self.entrada_huella_est.delete(0, tk.END)
            self.entrada_huella_est.insert(0, str(id_libre))
            messagebox.showinfo("Huella", f"Huella enrolada con ID {id_libre}.")
        except Exception as e:
            messagebox.showerror("Huella", f"Error: {e}")

    # ----------------- Helpers -----------------
    def _cargar_carreras_combo(self):
        """Carga el combo con 'codigo - nombre' desde la BD."""
        self._carreras_cache = {c.codigo: c.nombre for c in listar_carreras()}
        values = [f"{cod} - {nom}" for cod, nom in self._carreras_cache.items()]
        self.combo_carrera_est.configure(values=values)

    def actualizar_combo_carreras(self):
        #Método expuesto para que Admin_UI pueda refrescar el combo si cambian las carreras
        self._cargar_carreras_combo()

    def _nombre_carrera(self, cod: str) -> str:
        nom = self._carreras_cache.get(cod, cod)
        return f"{cod} - {nom}"

    # ------------------- CRUD -------------------
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
        if obtener_estudiante(codigo):
            messagebox.showerror("Error", "El código del estudiante ya existe.")
            return

        try:
            insertar_estudiante(Estudiante(codigo, nombre, int(id_huella), id_carrera))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar: {e}")
            return

        self.refrescar_estudiantes()
        messagebox.showinfo("Confirmación", f"Estudiante creado: {codigo} - {nombre}")
        self.limpiar_estudiante()

    def actualizar_estudiante(self):
        sel = self.tabla_estudiantes.selection()
        if not sel:
            messagebox.showwarning("Atención", "Selecciona un estudiante en la tabla para actualizar.")
            return
        vals = self.tabla_estudiantes.item(sel[0], "values")
        old_codigo = vals[0]

        codigo = self.entrada_codigo_est.get().strip()
        nombre = self.entrada_nombre_est.get().strip()
        id_huella = self.entrada_huella_est.get().strip()
        sel_car = self.combo_carrera_est.get().strip()

        if not codigo or not nombre or not id_huella or not sel_car:
            messagebox.showwarning("Atención", "Completa los campos antes de actualizar.")
            return
        if not id_huella.isdigit():
            messagebox.showwarning("Atención", "ID Huella debe ser numérico.")
            return

        id_carrera = sel_car.split(" - ", 1)[0]

        # Si cambia el código, valida que el nuevo no exista
        if old_codigo != codigo and obtener_estudiante(codigo):
            messagebox.showerror("Error", "El nuevo código ya existe.")
            return

        try:
            actualizar_estudiante(old_codigo, Estudiante(codigo, nombre, int(id_huella), id_carrera))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar: {e}")
            return

        self.refrescar_estudiantes()
        messagebox.showinfo("Confirmación", f"Estudiante actualizado: {codigo}")

    def eliminar_estudiante(self):
        sel = self.tabla_estudiantes.selection()
        if not sel:
            messagebox.showwarning("Atención", "Selecciona un estudiante en la tabla para eliminar.")
            return
        codigo = self.tabla_estudiantes.item(sel[0], "values")[0]
        if not messagebox.askyesno("Confirmación", f"¿Eliminar el estudiante '{codigo}'?"):
            return

        try:
            eliminar_estudiante(codigo)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar: {e}")
            return

        self.refrescar_estudiantes()
        self.limpiar_estudiante()
        messagebox.showinfo("Confirmación", f"Estudiante eliminado: {codigo}")

    # ----------------- Tabla/selección -----------------
    def refrescar_estudiantes(self):
        self._cargar_carreras_combo()  # por si cambiaron carreras

        term = ""
        try:
            term = self.entrada_buscar_est.get().strip()
        except Exception:
            pass  # primer render

        for iid in self.tabla_estudiantes.get_children():
            self.tabla_estudiantes.delete(iid)

        estudiantes = buscar_estudiantes(term) if term else listar_estudiantes()
        for e in estudiantes:
            self.tabla_estudiantes.insert(
                "", "end",
                values=(e.codigo, e.nombre, e.id_huella, self._nombre_carrera(e.id_carrera))
            )

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
        self.entrada_huella_est.insert(0, str(vals[2]))
        # vals[3] ya viene como "COD - Nombre"
        self.combo_carrera_est.set(vals[3])

    def limpiar_estudiante(self):
        self.entrada_codigo_est.delete(0, tk.END)
        self.entrada_nombre_est.delete(0, tk.END)
        self.entrada_huella_est.delete(0, tk.END)
        self.combo_carrera_est.set("")
        self.entrada_codigo_est.focus_set()
    def limpiar_busqueda_est(self):
        if hasattr(self, "entrada_buscar_est"):
            self.entrada_buscar_est.delete(0, tk.END)
        self.refrescar_estudiantes()

