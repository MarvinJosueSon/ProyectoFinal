# Docente_UI.py
import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as tb
from ttkbootstrap import ttk
from datetime import datetime

from DB_Manager import (
    obtener_docente_por_usuario, listar_carreras, listar_cursos,
    listar_estudiantes_por_carrera, obtener_estudiante_por_huella,
    crear_sesion_asistencia, cerrar_sesion_asistencia, registrar_evento_asistencia,
    listar_sesiones, listar_eventos_por_sesion,eliminar_sesion, listar_sesiones_por_docente,listar_eventos_por_sesion_con_nombre
)
from Huella import verificar_huella


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
        self.var_carrera = tk.StringVar()
        self.var_curso = tk.StringVar()
        self.var_fecha = tk.StringVar()
        self.var_hora = tk.StringVar()

        # Estado de sesión de asistencia
        self.sesion_id = None
        self._escuchando = False
        self._loop_id = None
        self.presentes = set()  # códigos de estudiante ya registrados en la sesión

        # --- Construcción UI ---
        self._construir_ui()

        # Carga inicial de combos y datos
        self._cargar_carreras()
        self._cargar_cursos()
        self.combo_carrera.bind("<<ComboboxSelected>>", lambda e: self._precargar_estudiantes())
        self._precargar_estudiantes()
        self._cargar_historial()

        # Reloj
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

        # --- Pestaña: Tomar asistencia ---
        tab_asistencia = ttk.Frame(Cuaderno, padding=12)
        Cuaderno.add(tab_asistencia, text="Tomar asistencia")
        self._construir_tab_asistencia(tab_asistencia)

        # --- Pestaña: Historial ---
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

        # Fila 2: Fecha y Hora (auto) + Carrera + Curso
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

        # Tabla de estudiantes
        marco_lista = ttk.Labelframe(parent, text="Listado de estudiantes", padding=12)
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

        # Barra de acciones
        barra_botones = ttk.Frame(parent)
        barra_botones.pack(fill="x", pady=(8, 0))
        ttk.Button(barra_botones, text="Iniciar asistencia", bootstyle="success",
                   command=self.iniciar_asistencia).pack(side="left", padx=4)
        ttk.Button(barra_botones, text="Terminar asistencia", bootstyle="danger",
                   command=self.terminar_asistencia).pack(side="left", padx=4)

    def _construir_tab_historial(self, parent: ttk.Frame):
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

        # Barra de historial
        barra = ttk.Frame(parent)
        barra.pack(fill="x", pady=(8, 0))
        ttk.Button(barra, text="Actualizar historial", command=self._cargar_historial).pack(side="left", padx=4)
        ttk.Button(barra, text="Ver detalle de sesión seleccionada", command=self._ver_detalle_sesion).pack(side="left", padx=4)

        ttk.Button(barra, text="Eliminar sesión seleccionada", bootstyle="danger",
                   command=self._eliminar_sesion).pack(side="left", padx=12)

    # -------------------- Datos / Helpers --------------------
    def _cargar_carreras(self):
        """Carga carreras al combobox."""
        try:
            carreras = listar_carreras()
            values = [f"{c.codigo} - {c.nombre}" for c in carreras]
            self.combo_carrera.configure(values=values)
            if values:
                self.combo_carrera.current(0)
        except Exception:
            self.combo_carrera.configure(values=[])

    def _cargar_cursos(self):
        """Carga cursos al combobox con formato 'ID - Nombre'."""
        try:
            cursos = listar_cursos()
            values = [f"{c.id_curso} - {c.nombre}" for c in cursos]
            self.combo_curso.configure(values=values)
            if values:
                self.combo_curso.current(0)
        except Exception:
            self.combo_curso.configure(values=[])

    def _precargar_estudiantes(self):
        """Llena la tabla con estudiantes de la carrera seleccionada."""
        try:
            sel_car = self.var_carrera.get().strip()
            if not sel_car:
                return
            id_carrera = sel_car.split(" - ", 1)[0]
            estudiantes = listar_estudiantes_por_carrera(id_carrera)

            # limpiar tabla
            for iid in self.tabla_prev.get_children():
                self.tabla_prev.delete(iid)

            carrera_txt = self.var_carrera.get().strip()
            for e in estudiantes:
                self.tabla_prev.insert(
                    "", "end", iid=e.codigo,
                    values=(e.codigo, e.nombre, carrera_txt)
                )
        except Exception:
            pass

    def _tick_reloj(self):
        """Actualiza Fecha y Hora cada segundo (desde el sistema)."""
        ahora = datetime.now()
        self.var_fecha.set(ahora.strftime("%Y-%m-%d"))
        self.var_hora.set(ahora.strftime("%H:%M:%S"))
        self.after(1000, self._tick_reloj)

    # -------------------- Asistencia (sesión) --------------------
    def iniciar_asistencia(self):
        if self._escuchando:
            return

        jornada = self.var_jornada.get().strip()
        fecha = self.var_fecha.get().strip()
        hora = datetime.now().strftime("%H:%M:%S")

        sel_car = self.var_carrera.get().strip()
        sel_cur = self.var_curso.get().strip()
        if not sel_car or not sel_cur:
            messagebox.showwarning("Asistencia", "Selecciona Carrera y Curso.")
            return

        id_carrera = sel_car.split(" - ", 1)[0]
        id_curso = sel_cur.split(" - ", 1)[0]
        usuario_docente = self.usuario_docente or (self.docente.usuario if self.docente else "")

        try:
            self.sesion_id = crear_sesion_asistencia(fecha, hora, jornada, usuario_docente, id_carrera, id_curso)
        except Exception as e:
            messagebox.showerror("Asistencia", f"No se pudo crear la sesión: {e}")
            return

        # Bloquear combos mientras esté activa la sesión
        self.combo_jornada.configure(state="disabled")
        self.combo_carrera.configure(state="disabled")
        self.combo_curso.configure(state="disabled")

        self.presentes = set()
        self._escuchando = True
        messagebox.showinfo("Asistencia", "Sesión iniciada. Pida a los estudiantes pasar su huella.")
        self._loop_verificacion()

    def terminar_asistencia(self):
        if not self._escuchando:
            messagebox.showinfo("Asistencia", "No hay sesión en curso.")
            return

        self._escuchando = False
        if self._loop_id:
            try:
                self.after_cancel(self._loop_id)
            except Exception:
                pass
            self._loop_id = None

        try:
            hora_fin = datetime.now().strftime("%H:%M:%S")
            if self.sesion_id:
                cerrar_sesion_asistencia(self.sesion_id, hora_fin)
        except Exception as e:
            messagebox.showerror("Asistencia", f"No se pudo cerrar la sesión: {e}")

        # Desbloquear combos
        self.combo_jornada.configure(state="readonly")
        self.combo_carrera.configure(state="readonly")
        self.combo_curso.configure(state="readonly")

        messagebox.showinfo("Asistencia", "Sesión terminada y guardada.")
        self.sesion_id = None

        # refrescar historial
        self._cargar_historial()

    def _loop_verificacion(self):
        """Llama a verificar_huella() periódicamente mientras la sesión está activa."""
        if not self._escuchando:
            return

        try:
            found, match_id = verificar_huella()
            if found and match_id is not None:
                est = obtener_estudiante_por_huella(int(match_id))
                if est is not None:
                    if est.codigo in self.presentes:
                        messagebox.showinfo(
                            "Asistencia",
                            f"El estudiante {est.nombre} ({est.codigo}) ya fue registrado en esta sesión."
                        )
                    else:
                        self.presentes.add(est.codigo)
                        if self.sesion_id:
                            registrar_evento_asistencia(
                                self.sesion_id,
                                est.codigo,
                                int(match_id),
                                datetime.now().strftime("%H:%M:%S")
                            )
                        messagebox.showinfo(
                            "Asistencia",
                            f"Asistencia registrada: {est.nombre} ({est.codigo})"
                        )
                else:
                    messagebox.showwarning(
                        "Asistencia",
                        f"Huella detectada (ID {match_id}) no asignada a ningún estudiante."
                    )
        except Exception:
            # evitar spam de errores si no hay huella/puerto ocupado
            pass

        # Repetir ~cada segundo
        self._loop_id = self.after(1000, self._loop_verificacion)

    # -------------------- Historial --------------------
    def _cargar_historial(self):
        # usuario del docente logueado
        usuario_doc = self.usuario_docente or (self.docente.usuario if self.docente else "")

        # limpiar tabla
        for iid in self.tabla_hist.get_children():
            self.tabla_hist.delete(iid)

        try:
            filas = listar_sesiones_por_docente(usuario_doc)
            # filas: (sid, fecha, hi, hf, jornada, usuario, id_carrera, carrera_nom, id_curso, curso_nom)
            for (sid, fecha, hi, hf, jornada, _u, _idcar, carrera_nom, _idcur, curso_nom) in filas:
                presentes = len(listar_eventos_por_sesion(sid))
                self.tabla_hist.insert(
                    "", "end", iid=f"s{sid}",
                    values=(fecha, hi, jornada, carrera_nom, curso_nom, presentes, "-")
                )
        except Exception as e:
            messagebox.showerror("Historial", f"Error al cargar: {e}")

    def _ver_detalle_sesion(self):
        sel = self.tabla_hist.selection()
        if not sel:
            messagebox.showinfo("Historial", "Selecciona una sesión.")
            return

        sid = int(sel[0][1:])  # quita prefijo 's'

        # Trae también el nombre del estudiante
        eventos = listar_eventos_por_sesion_con_nombre(sid)
        if not eventos:
            messagebox.showinfo("Detalle", "Sin eventos en esta sesión.")
            return

        top = tk.Toplevel(self)
        top.title(f"Detalle sesión {sid}")
        top.geometry("640x460")

        # Tabla bonita en lugar de Text
        cols = ("codigo", "nombre", "huella", "hora")
        tv = ttk.Treeview(top, columns=cols, show="headings")
        tv.heading("codigo", text="Código")
        tv.heading("nombre", text="Nombre")
        tv.heading("huella", text="ID Huella")
        tv.heading("hora", text="Hora")

        tv.column("codigo", width=120, anchor="center")
        tv.column("nombre", width=300, anchor="w")
        tv.column("huella", width=100, anchor="center")
        tv.column("hora", width=100, anchor="center")

        scroll = ttk.Scrollbar(top, orient="vertical", command=tv.yview)
        tv.configure(yscrollcommand=scroll.set)
        tv.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        for cod, nom, idh, hora in eventos:
            tv.insert("", "end", values=(cod, nom, idh, hora))

    def _eliminar_sesion(self):
        sel = self.tabla_hist.selection()
        if not sel:
            messagebox.showinfo("Historial", "Selecciona una sesión para eliminar.")
            return

        # id viene con prefijo 's'
        sid = int(sel[0][1:])
        # Datos opcionales para mostrar en el diálogo
        vals = self.tabla_hist.item(sel[0], "values")
        fecha, hora, jornada, carrera, curso = vals[0], vals[1], vals[2], vals[3], vals[4]

        if not messagebox.askyesno(
                "Confirmación",
                f"¿Eliminar la sesión #{sid}?\n\n"
                f"Fecha: {fecha} {hora}\nJornada: {jornada}\nCarrera: {carrera}\nCurso: {curso}\n\n"
                "Esta acción eliminará también sus registros de asistencia."
        ):
            return

        try:
            eliminar_sesion(sid)
            self._cargar_historial()
            messagebox.showinfo("Historial", f"Sesión #{sid} eliminada.")
        except Exception as e:
            messagebox.showerror("Historial", f"No se pudo eliminar la sesión: {e}")

        def _cargar_historial(self):
            # Determinar el usuario del docente logueado
            usuario_docente = self.usuario_docente or (self.docente.usuario if self.docente else "")
            for iid in self.tabla_hist.get_children():
                self.tabla_hist.delete(iid)
            try:
                # Trae SOLO sesiones de este docente + nombres de carrera/curso
                filas = listar_sesiones_por_docente(usuario_docente)
                for (sid, fecha, hi, hf, jornada, _usuario, id_carrera, carrera_nom, id_curso, curso_nom) in filas:
                    presentes = len(listar_eventos_por_sesion(sid))
                    # Muestra NOMBRES en las columnas "Carrera" y "Curso"
                    self.tabla_hist.insert(
                        "", "end", iid=f"s{sid}",
                        values=(fecha, hi, jornada, carrera_nom, curso_nom, presentes, "-")
                    )
            except Exception as e:
                messagebox.showerror("Historial", f"Error al cargar: {e}")
