# Docente_UI.py
import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap import ttk
from datetime import datetime

from DB_Manager import obtener_docente_por_usuario, listar_carreras,listar_cursos

class VentanaDocente(tb.Toplevel):

    def __init__(self, master, usuario_docente: str = None):
        super().__init__(master)

        # --- Docente desde login / BD ---
        self.usuario_docente = usuario_docente or ""
        self.docente = None
        try:
            if self.usuario_docente:
                self.docente = obtener_docente_por_usuario(self.usuario_docente)
        except Exception:
            self.docente = None

        # Texto para título y encabezado
        nombre_para_titulo = f"'{self.usuario_docente}'"
        if self.docente and getattr(self.docente, "nombre", None):
            nombre_para_titulo = f"'{self.docente.nombre}'"

        self.title(f"Docente - {nombre_para_titulo}")
        self.geometry("1100x760")
        self.resizable(True, True)

        # --- Estado UI ---
        self.var_docente = tk.StringVar(value=nombre_para_titulo.strip("'"))
        self.var_jornada = tk.StringVar()
        self.var_curso = tk.StringVar()
        self.var_fecha = tk.StringVar()
        self.var_hora = tk.StringVar()
        self.var_carrera = tk.StringVar()

        # --- Construcción UI ---
        self._construir_ui()
        self._cargar_carreras()
        self._cargar_cursos()
        self._tick_reloj()  # inicia actualización de fecha/hora

    # -------------------- UI --------------------
    def _construir_ui(self):
        cont = ttk.Frame(self, padding=12)
        cont.pack(fill="both", expand=True)

        # Título grande
        hdr = ttk.Frame(cont)
        hdr.pack(fill="x", pady=(0, 8))
        ttk.Label(
            hdr,
            text="Panel del Docente",
            font=("Segoe UI", 16, "bold")
        ).pack(side="left")

        # Notebook principal
        Cuaderno = ttk.Notebook(cont)
        Cuaderno.pack(fill="both", expand=True)

        # --- Pestaña: Tomar asistencia (solo visual) ---
        tab_asistencia = ttk.Frame(Cuaderno, padding=12)
        Cuaderno.add(tab_asistencia, text="Tomar asistencia")

        self._construir_tab_asistencia(tab_asistencia)

        # --- Pestaña: Historial (solo visual) ---
        tab_historial = ttk.Frame(Cuaderno, padding=12)
        Cuaderno.add(tab_historial, text="Historial")

        self._construir_tab_historial(tab_historial)

    def _construir_tab_asistencia(self, parent: ttk.Frame):
        # Encabezado de datos
        marco = ttk.Labelframe(parent, text="Datos de la toma", padding=12)
        marco.pack(fill="x")

        # Fila 1: Docente (solo lectura) + Jornada
        fila1 = ttk.Frame(marco)
        fila1.pack(fill="x", pady=6)

        ttk.Label(fila1, text="Docente:").grid(row=0, column=0, sticky="e", padx=(0, 6))
        entrada_doc = ttk.Entry(fila1, textvariable=self.var_docente, width=40, state="readonly")
        entrada_doc.grid(row=0, column=1, sticky="w")

        ttk.Label(fila1, text="Jornada:").grid(row=0, column=2, sticky="e", padx=(18, 6))
        self.combo_jornada = ttk.Combobox(
            fila1,
            textvariable=self.var_jornada,
            state="readonly",
            width=24,
            values=["Matutina", "Vespertina", "Fin de semana"]
        )
        self.combo_jornada.grid(row=0, column=3, sticky="w")
        self.combo_jornada.current(0)  # default Matutina

        # Fila 2: Fecha y Hora (auto) + Carrera
        fila2 = ttk.Frame(marco)
        fila2.pack(fill="x", pady=6)

        ttk.Label(fila2, text="Fecha:").grid(row=0, column=0, sticky="e", padx=(0, 6))
        ttk.Entry(fila2, textvariable=self.var_fecha, state="readonly", width=18).grid(row=0, column=1, sticky="w")

        ttk.Label(fila2, text="Hora:").grid(row=0, column=2, sticky="e", padx=(18, 6))
        ttk.Entry(fila2, textvariable=self.var_hora, state="readonly", width=14).grid(row=0, column=3, sticky="w")

        ttk.Label(fila2, text="Carrera:").grid(row=0, column=4, sticky="e", padx=(18, 6))
        self.combo_carrera = ttk.Combobox(fila2, textvariable=self.var_carrera, state="readonly", width=36)
        self.combo_carrera.grid(row=0, column=5, sticky="w")

        ttk.Label(fila2, text="Curso:").grid(row=0, column=6, sticky="e", padx=(18, 6))
        self.combo_curso = ttk.Combobox(fila2, textvariable=self.var_curso, state="readonly", width=36)
        self.combo_curso.grid(row=0, column=7, sticky="w")

        # Separador
        ttk.Separator(parent).pack(fill="x", pady=12)

        # Placeholder de tabla/listado de estudiantes (visual)
        marco_lista = ttk.Labelframe(parent, text="Listado de estudiantes (vista previa)", padding=12)
        marco_lista.pack(fill="both", expand=True)

        cols = ("codigo", "nombre", "carrera")
        self.tabla_prev = ttk.Treeview(marco_lista, columns=cols, show="headings", height=18)
        self.tabla_prev.heading("codigo", text="Código")
        self.tabla_prev.heading("nombre", text="Nombre")
        self.tabla_prev.heading("carrera", text="Carrera")

        self.tabla_prev.column("codigo", width=140, anchor="center")
        self.tabla_prev.column("nombre", width=420, anchor="w")
        self.tabla_prev.column("carrera", width=280, anchor="w")

        scroll_prev = ttk.Scrollbar(marco_lista, orient="vertical", command=self.tabla_prev.yview)
        self.tabla_prev.configure(yscrollcommand=scroll_prev.set)
        self.tabla_prev.pack(side="left", fill="both", expand=True)
        scroll_prev.pack(side="right", fill="y")

        # Nota de que es solo visual por ahora
        ttk.Label(
            parent,
            text="* Esta es solo la interfaz visual. La funcionalidad se activará en el siguiente paso.",
            bootstyle="secondary"
        ).pack(anchor="w", pady=(8, 0))

        # Botones (deshabilitados por ahora para dejar claro que es visual)
        barra_botones = ttk.Frame(parent)
        barra_botones.pack(fill="x", pady=(8, 0))
        ttk.Button(barra_botones, text="Cargar estudiantes", state="disabled").pack(side="left", padx=4)
        ttk.Button(barra_botones, text="Guardar asistencia", state="disabled").pack(side="right", padx=4)

    def _construir_tab_historial(self, parent: ttk.Frame):
        # Solo UI: tabla vacía por ahora
        marco = ttk.Labelframe(parent, text="Historial de tomas de asistencia", padding=12)
        marco.pack(fill="both", expand=True)

        cols = ("fecha", "hora", "jornada", "carrera", "curso", "presentes", "ausentes")
        self.tabla_hist = ttk.Treeview(marco, columns=cols, show="headings", height=22)

        self.tabla_hist.heading("fecha", text="Fecha")
        self.tabla_hist.heading("hora", text="Hora")
        self.tabla_hist.heading("jornada", text="Jornada")
        self.tabla_hist.heading("carrera", text="Carrera")
        self.tabla_hist.heading("curso", text="Curso")
        self.tabla_hist.heading("presentes", text="Presentes")
        self.tabla_hist.heading("ausentes", text="Ausentes")

        self.tabla_hist.column("fecha", width=100, anchor="center")
        self.tabla_hist.column("hora", width=100, anchor="center")
        self.tabla_hist.column("jornada", width=120, anchor="center")
        self.tabla_hist.column("carrera", width=240, anchor="w")
        self.tabla_hist.column("curso", width=240, anchor="w")
        self.tabla_hist.column("presentes", width=110, anchor="center")
        self.tabla_hist.column("ausentes", width=110, anchor="center")

        scroll = ttk.Scrollbar(marco, orient="vertical", command=self.tabla_hist.yview)
        self.tabla_hist.configure(yscrollcommand=scroll.set)
        self.tabla_hist.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        # Mensaje de placeholder
        ttk.Label(
            parent,
            text="* Historial en modo vista — conectaremos la base de datos en el siguiente paso.",
            bootstyle="secondary"
        ).pack(anchor="w", pady=(8, 0))

    # -------------------- Datos UI --------------------
    def _cargar_carreras(self):
        """Carga carreras al combobox (solo UI — sin lógica aún)."""
        try:
            carreras = listar_carreras()
            values = [f"{c.codigo} - {c.nombre}" for c in carreras]
            self.combo_carrera.configure(values=values)
            if values:
                self.combo_carrera.current(0)
        except Exception:
            # Si no cargan, dejamos el combobox vacío
            self.combo_carrera.configure(values=[])

    def _cargar_cursos(self):
        """Carga cursos al combobox con formato 'ID - Nombre' (sin filtrar)."""
        try:
            cursos = listar_cursos()
            values = [f"{c.id_curso} - {c.nombre}" for c in cursos]
            self.combo_curso.configure(values=values)
            if values:
                self.combo_curso.current(0)
        except Exception:
            self.combo_curso.configure(values=[])

    def _tick_reloj(self):
        """Actualiza Fecha y Hora cada segundo (desde el sistema)."""
        ahora = datetime.now()
        self.var_fecha.set(ahora.strftime("%Y-%m-%d"))
        self.var_hora.set(ahora.strftime("%H:%M:%S"))
        self.after(1000, self._tick_reloj)
