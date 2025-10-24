#Admin_UI.Py
import ttkbootstrap as tb
from ttkbootstrap import ttk
from CursosAD import CursosAD
from DocentesAD import DocentesAD
from CarrerasAD import CarrerasAD
from EstudiantesAD import EstudiantesAD
from SensorHuellasAD import SensorHuellasAD

class VentanaAdministrador(tb.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Administrador")
        self.geometry("1100x760")
        self._construir()

    def _construir(self):
        contenedor = ttk.Frame(self, padding=12)
        contenedor.pack(fill="both", expand=True)

        pestañas = ttk.Notebook(contenedor)
        pestañas.pack(fill="both", expand=True)

        # Cursos
        self.tab_cursos = CursosAD(pestañas)
        pestañas.add(self.tab_cursos, text="Cursos")

        # Docentes
        self.tab_docentes = DocentesAD(pestañas)
        pestañas.add(self.tab_docentes, text="Docentes")

        # Carreras (cuando cambien, refrescamos combo en Estudiantes)
        def _carreras_cambiadas():
            if hasattr(self, "tab_estudiantes"):
                try:
                    self.tab_estudiantes.actualizar_combo_carreras()
                    self.tab_estudiantes.refrescar_estudiantes()
                except Exception:
                    pass

        self.tab_carreras = CarrerasAD(pestañas, on_carreras_cambiadas=_carreras_cambiadas)
        pestañas.add(self.tab_carreras, text="Carreras")

        # Estudiantes
        self.tab_estudiantes = EstudiantesAD(pestañas)
        pestañas.add(self.tab_estudiantes, text="Estudiantes")

        self.tab_sensor = SensorHuellasAD(pestañas)
        pestañas.add(self.tab_sensor, text="Sensor de Huellas")
