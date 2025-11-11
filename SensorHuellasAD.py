# SensorHuellasAD.py
import tkinter as tk
from ttkbootstrap import ttk
from tkinter import messagebox

from DB_Manager import listar_docentes, listar_estudiantes
from Huella import ping, contar_huellas, listar_huellas_ids, borrar_huella_id, borrar_todas_huellas, existe_huella
from tkinter import simpledialog


class SensorHuellasAD(ttk.Frame):
    """
    Pestaña para auditar y administrar el sensor de huellas:
    - Verificar conexión
    - Contar huellas
    - Listar IDs en sensor
    - Cruce con BD (Docentes/Estudiantes)
    - Borrar por ID / Borrar
    """
    def __init__(self, master):
        super().__init__(master, padding=12)
        self._cache_ids_sensor = set()
        self._construir()

    def _construir(self):
        # Acciones superiores
        barra = ttk.Frame(self)
        barra.pack(fill="x", pady=(0, 8))

        ttk.Button(barra, text="Verificar conexión", bootstyle="info", command=self._verificar).pack(side="left", padx=4)
        ttk.Button(barra, text="Contar huellas", bootstyle="secondary", command=self._contar).pack(side="left", padx=4)
        ttk.Button(barra, text="Listar huellas (sensor)", bootstyle="primary", command=self._listar).pack(side="left", padx=4)

        ttk.Label(barra, text="ID a borrar:").pack(side="left", padx=(18, 6))
        self.ent_id_borrar = ttk.Entry(barra, width=8)
        self.ent_id_borrar.pack(side="left")
        ttk.Button(barra, text="Borrar ID", bootstyle="danger", command=self._borrar_id).pack(side="left", padx=4)

        ttk.Button(barra, text="Borrar TODO", bootstyle="danger-outline", command=self._borrar_todo).pack(side="right", padx=4)

        # Tabla
        marco = ttk.Labelframe(self, text="Estado del sensor y cruce con BD", padding=12)
        marco.pack(fill="both", expand=True)

        cols = ("sensor_id", "estado", "tipo", "codigo", "nombre")
        self.tabla = ttk.Treeview(marco, columns=cols, show="headings")
        self.tabla.heading("sensor_id", text="ID Sensor")
        self.tabla.heading("estado", text="Estado")
        self.tabla.heading("tipo", text="Tipo")
        self.tabla.heading("codigo", text="Código")
        self.tabla.heading("nombre", text="Nombre")

        self.tabla.column("sensor_id", width=110, anchor="center")
        self.tabla.column("estado", width=120, anchor="center")
        self.tabla.column("tipo", width=110, anchor="center")
        self.tabla.column("codigo", width=160, anchor="center")
        self.tabla.column("nombre", width=360, anchor="w")

        sc = ttk.Scrollbar(marco, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=sc.set)
        self.tabla.pack(side="left", fill="both", expand=True)
        sc.pack(side="right", fill="y")

        # Leyenda
        ttk.Label(self, text="Estado: Asignada = existe en sensor y está en BD | Libre = existe en sensor pero no está en BD | Falta en sensor = está en BD pero no en sensor",
                  bootstyle="secondary").pack(anchor="w", pady=(8,0))

    # ----- Acciones -----
    def _verificar(self):
        try:
            ok = ping()
            message = "Conectado (PONG recibido)" if ok else "Sin respuesta (PING falló)"
            messagebox.showinfo("Sensor", message)
        except Exception as e:
            messagebox.showerror("Sensor", f"Error al verificar: {e}")

    def _contar(self):
        try:
            n = contar_huellas()
            if n >= 0:
                messagebox.showinfo("Sensor", f"Total de huellas en sensor: {n}")
            else:
                messagebox.showwarning("Sensor", "No se pudo obtener el total (respuesta inválida).")
        except Exception as e:
            messagebox.showerror("Sensor", f"Error al contar: {e}")

    def _listar(self):
        try:
            ids = listar_huellas_ids()
            self._cache_ids_sensor = set(ids)
            self._poblar_tabla_cruce(ids)
        except Exception as e:
            messagebox.showerror("Sensor", f"Error al listar: {e}")

    def _borrar_id(self):
        val = self.ent_id_borrar.get().strip()
        if not val.isdigit():
            messagebox.showwarning("Borrar ID", "Ingresa un ID numérico.")
            return
        id_h = int(val)
        if not messagebox.askyesno("Confirmación", f"¿Borrar la huella ID {id_h} del sensor? Esta acción no se puede deshacer."):
            return
        try:
            # opcional: verificar existencia
            existe = existe_huella(id_h)
            if not existe:
                if not messagebox.askyesno("Borrar ID", f"El ID {id_h} no existe en el sensor.\n¿Deseas intentar borrarlo de todos modos?"):
                    return
            ok = borrar_huella_id(id_h)
            if ok:
                messagebox.showinfo("Borrar ID", f"Huella {id_h} borrada del sensor.")
                self._listar()
            else:
                messagebox.showerror("Borrar ID", f"No se pudo borrar la huella {id_h}.")
        except Exception as e:
            messagebox.showerror("Borrar ID", f"Error: {e}")

    def _borrar_todo(self):
        if not messagebox.askyesno("Borrar TODO", "¿Seguro que deseas borrar TODAS las huellas del sensor?"):
            return
        # segunda confirmación
        confirm = simpledialog.askstring("Confirmación adicional", "Escribe: BORRAR TODO")
        if (confirm or "").strip().upper() != "BORRAR TODO":
            messagebox.showinfo("Borrar TODO", "Operación cancelada.")
            return
        try:
            ok = borrar_todas_huellas()
            if ok:
                messagebox.showinfo("Borrar TODO", "Todas las huellas fueron borradas del sensor.")
                self._listar()
            else:
                messagebox.showerror("Borrar TODO", "No se pudo borrar todo. Revisa conexión/firmware.")
        except Exception as e:
            messagebox.showerror("Borrar TODO", f"Error: {e}")

    # ----- Cruce Sensor ↔ BD -----
    def _poblar_tabla_cruce(self, ids_sensor: list[int]):
        for iid in self.tabla.get_children():
            self.tabla.delete(iid)

        # BD → mapas por id_huella
        m_asignados = {}  # id -> (tipo, codigo, nombre)
        for d in listar_docentes():
            if d.id_huella is not None:
                m_asignados[int(d.id_huella)] = ("Docente", d.codigo, d.nombre)
        for e in listar_estudiantes():
            if e.id_huella is not None:
                # detectar conflicto mismo ID usado por dos tipos
                if int(e.id_huella) in m_asignados and m_asignados[int(e.id_huella)][0] != "Estudiante":
                    # marcar conflicto mostrando dos filas
                    tipo1, cod1, nom1 = m_asignados[int(e.id_huella)]
                    self.tabla.insert("", "end", values=(int(e.id_huella), "Conflicto", tipo1, cod1, nom1))
                    self.tabla.insert("", "end", values=(int(e.id_huella), "Conflicto", "Estudiante", e.codigo, e.nombre))
                else:
                    m_asignados[int(e.id_huella)] = ("Estudiante", e.codigo, e.nombre)

        set_sensor = set(int(x) for x in ids_sensor)
        set_bd = set(m_asignados.keys())

        # 1) IDs en sensor (Asignada/Libre/Conflicto)
        for sid in sorted(set_sensor):
            if sid in m_asignados:
                tipo, codigo, nombre = m_asignados[sid]
                self.tabla.insert("", "end", values=(sid, "Asignada", tipo, codigo, nombre))
            else:
                self.tabla.insert("", "end", values=(sid, "Libre", "-", "-", "-"))

        # 2) IDs en BD pero que faltan en sensor
        faltan = sorted(set_bd - set_sensor)
        for fid in faltan:
            tipo, codigo, nombre = m_asignados[fid]
            self.tabla.insert("", "end", values=(fid, "Falta en sensor", tipo, codigo, nombre))
