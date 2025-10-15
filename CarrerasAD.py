#CarrerasAD.py
import tkinter as tk
from ttkbootstrap import ttk
from tkinter import messagebox
from Clases import Carrera
from DB_Manager import listar_carreras, insertar_carrera, eliminar_carrera, actualizar_carrera, obtener_carrera

class CarrerasAD(ttk.Frame):
    def __init__(self, master, carreras=None, guardar_carreras_cb=None, on_carreras_cambiadas=None):
        super().__init__(master, padding=12)
        self.on_carreras_cambiadas = on_carreras_cambiadas
        self._construir()

    def _construir(self):
        marco_car = ttk.Frame(self)
        marco_car.pack(fill="x", pady=(0,8))
        ttk.Label(marco_car, text="ID Carrera:").grid(row=0, column=0, sticky="e", padx=6, pady=6)
        ttk.Label(marco_car, text="Nombre Carrera:").grid(row=1, column=0, sticky="e", padx=6, pady=6)
        self.entrada_id_carrera = ttk.Entry(marco_car, width=30)
        self.entrada_nombre_carrera = ttk.Entry(marco_car, width=40)
        self.entrada_id_carrera.grid(row=0, column=1, padx=6, pady=6)
        self.entrada_nombre_carrera.grid(row=1, column=1, padx=6, pady=6)

        marco_btn_car = ttk.Frame(self)
        marco_btn_car.pack(fill="x", pady=(0,8))
        ttk.Button(marco_btn_car, text="Guardar", bootstyle="success", command=self.guardar_carrera).pack(side="left", padx=4)
        ttk.Button(marco_btn_car, text="Actualizar", bootstyle="secondary", command=self.actualizar_carrera).pack(side="left", padx=4)
        ttk.Button(marco_btn_car, text="Eliminar", bootstyle="danger", command=self.eliminar_carrera).pack(side="left", padx=4)
        ttk.Button(marco_btn_car, text="Limpiar", bootstyle="info", command=self.limpiar_carrera).pack(side="left", padx=4)

        marco_tabla_car = ttk.Frame(self)
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

        self.refrescar_carreras()

    # ---- CRUD con SQLite ----
    def guardar_carrera(self):
        codigo = self.entrada_id_carrera.get().strip()
        nombre = self.entrada_nombre_carrera.get().strip()
        if not codigo or not nombre:
            messagebox.showwarning("Atención", "Completa ID y Nombre de la carrera.")
            return
        if obtener_carrera(codigo):
            messagebox.showerror("Error", "El ID de la carrera ya existe.")
            return
        insertar_carrera(Carrera(codigo, nombre))
        self.refrescar_carreras()
        if self.on_carreras_cambiadas:
            self.on_carreras_cambiadas()
        messagebox.showinfo("Confirmación", f"Carrera guardada: {codigo}")
        self.limpiar_carrera()

    def actualizar_carrera(self):
        sel = self.tabla_carreras.selection()
        if not sel:
            messagebox.showwarning("Atención", "Selecciona una carrera para actualizar.")
            return
        vals = self.tabla_carreras.item(sel[0], "values")
        old_codigo = vals[0]
        nuevo = Carrera(self.entrada_id_carrera.get().strip(), self.entrada_nombre_carrera.get().strip())
        if not nuevo.codigo or not nuevo.nombre:
            messagebox.showwarning("Atención", "Completa los campos antes de actualizar.")
            return
        actualizar_carrera(old_codigo, nuevo)
        self.refrescar_carreras()
        messagebox.showinfo("Confirmación", f"Carrera actualizada: {nuevo.codigo}")

    def eliminar_carrera(self):
        sel = self.tabla_carreras.selection()
        if not sel:
            messagebox.showwarning("Atención", "Selecciona una carrera para eliminar.")
            return
        vals = self.tabla_carreras.item(sel[0], "values")
        codigo = vals[0]
        if not messagebox.askyesno("Confirmación", f"¿Eliminar la carrera '{codigo}'?"):
            return
        eliminar_carrera(codigo)
        self.refrescar_carreras()
        if self.on_carreras_cambiadas:
            self.on_carreras_cambiadas()
        messagebox.showinfo("Confirmación", f"Carrera eliminada: {codigo}")

    def limpiar_carrera(self):
        self.entrada_id_carrera.delete(0, tk.END)
        self.entrada_nombre_carrera.delete(0, tk.END)
        self.entrada_id_carrera.focus_set()

    def refrescar_carreras(self):
        for iid in self.tabla_carreras.get_children():
            self.tabla_carreras.delete(iid)
        for c in listar_carreras():
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
