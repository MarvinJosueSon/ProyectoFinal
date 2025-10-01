# Admin_UI.py
import ttkbootstrap as tb
from ttkbootstrap import ttk

from CursosAD import CursosAD
from DocentesAD import DocentesAD
from CarrerasAD import CarrerasAD
from EstudiantesAD import EstudiantesAD

class VentanaAdministrador(tb.Toplevel):
    def __init__(self, master, cursos, docentes, carreras, estudiantes,
                 guardar_cursos_cb, guardar_docentes_cb, guardar_carreras_cb, guardar_estudiantes_cb,
                 on_docentes_actualizados=None):
        super().__init__(master)
        self.title("Administrador")
        self.geometry("1100x760")

        # Datos y callbacks
        self.cursos = cursos
        self.docentes = docentes
        self.carreras = carreras
        self.estudiantes = estudiantes
        self.guardar_cursos_cb = guardar_cursos_cb
        self.guardar_docentes_cb = guardar_docentes_cb
        self.guardar_carreras_cb = guardar_carreras_cb
        self.guardar_estudiantes_cb = guardar_estudiantes_cb
        self.on_docentes_actualizados = on_docentes_actualizados

        self._construir()

    def _construir(self):
        contenedor = ttk.Frame(self, padding=12)
        contenedor.pack(fill="both", expand=True)
        pestañas = ttk.Notebook(contenedor)
        pestañas.pack(fill="both", expand=True)

        # Cursos
        self.tab_cursos = CursosAD(
            pestañas,
            cursos=self.cursos,
            guardar_cursos_cb=self.guardar_cursos_cb
        )
        pestañas.add(self.tab_cursos, text="Cursos")


        self.tab_docentes = DocentesAD(
            pestañas,
            docentes=self.docentes,
            guardar_docentes_cb=self.guardar_docentes_cb,
            on_docentes_actualizados=self.on_docentes_actualizados
        )
        pestañas.add(self.tab_docentes, text="Docentes")


        def _carreras_cambiadas():
            if hasattr(self, "tab_estudiantes"):
                self.tab_estudiantes.actualizar_combo_carreras()

        self.tab_carreras = CarrerasAD(
            pestañas,
            carreras=self.carreras,
            guardar_carreras_cb=self.guardar_carreras_cb,
            on_carreras_cambiadas=_carreras_cambiadas
        )
        pestañas.add(self.tab_carreras, text="Carreras")


        self.tab_estudiantes = EstudiantesAD(
            pestañas,
            estudiantes=self.estudiantes,
            carreras=self.carreras,
            guardar_estudiantes_cb=self.guardar_estudiantes_cb
        )
        pestañas.add(self.tab_estudiantes, text="Estudiantes")
