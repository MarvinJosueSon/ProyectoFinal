from typing import List, Dict, Optional
from datetime import datetime


class Persona:
    def __init__(self, codigo: str, nombre: str, id_huella: int):
        self.codigo = codigo
        self.nombre = nombre
        self.id_huella = id_huella


class Estudiante(Persona):
    def __init__(self, codigo: str, nombre: str, id_huella: int, id_carrera: str):
        super().__init__(codigo, nombre, id_huella)
        self.id_carrera = id_carrera


class Docente(Persona):
    def __init__(self, codigo: str, nombre: str, id_huella: int, cursos: Dict[str, str] | None = None):
        super().__init__(codigo, nombre, id_huella)
        self.cursos = cursos or {}


class Admin(Persona):
    def __init__(self, codigo: str, nombre: str, id_huella: int):
        super().__init__(codigo, nombre, id_huella)


class Curso:
    def __init__(self, id_curso: str, nombre: str):
        self.id_curso = id_curso
        self.nombre = nombre


class Carrera:
    def __init__(self, codigo: str, nombre: str):
        self.codigo = codigo
        self.nombre = nombre



class Huella:
    def __init__(self, id_huella: int, persona: Persona):
        self.id_huella = id_huella
        self.persona = persona


class LectorHuella:
    def __init__(self):
        self.huellas: List[Huella] = []

    def agregar_huella(self, huella: Huella):
        self.huellas.append(huella)

    def verificar_huella(self, id_huella: int) -> Optional[Persona]:
        for h in self.huellas:
            if h.id_huella == id_huella:
                return h.persona
        return None



class Asistencia:
    def __init__(self, fecha: str, id_curso: str, id_estudiantes: List[str], id_docente: str):
        self.fecha = fecha
        self.id_curso = id_curso
        self.id_estudiantes = id_estudiantes
        self.id_docente = id_docente


class ControlAsistencia:
    def __init__(self, hora_entrada: datetime | None = None, hora_salida: datetime | None = None):
        self.hora_entrada = hora_entrada
        self.hora_salida = hora_salida

    def verificacion(self) -> bool:
        return self.hora_entrada is not None and self.hora_salida is not None

    def registro(self):
        return {
            "hora_entrada": self.hora_entrada,
            "hora_salida": self.hora_salida
        }



class Buscar:
    def __init__(self, diccionario: Dict[str, str]):
        self.diccionario = diccionario

    def buscar(self, codigo: str) -> Optional[str]:
        return self.diccionario.get(codigo)


class Eliminar:
    def __init__(self, diccionario: Dict[str, str]):
        self.diccionario = diccionario

    def eliminar(self, codigo: str):
        if codigo in self.diccionario:
            del self.diccionario[codigo]


class QuickSort:
    def __init__(self, lista: List[int]):
        self.lista = lista

    def quicksort(self) -> List[int]:
        if len(self.lista) <= 1:
            return self.lista
        pivot = self.lista[len(self.lista) // 2]
        left = [x for x in self.lista if x < pivot]
        middle = [x for x in self.lista if x == pivot]
        right = [x for x in self.lista if x > pivot]
        return QuickSort(left).quicksort() + middle + QuickSort(right).quicksort()


class Mostrar:
    def __init__(self, elementos: List[str]):
        self.elementos = elementos

    def mostrar(self):
        for e in self.elementos:
            print(e)



class AdministrarAdmin:
    def __init__(self):
        self.admins: List[Admin] = []

    def agregar(self, admin: Admin):
        self.admins.append(admin)


class AdministrarEstudiante:
    def __init__(self):
        self.estudiantes: List[Estudiante] = []

    def agregar(self, estudiante: Estudiante):
        self.estudiantes.append(estudiante)


class AdministrarDocente:
    def __init__(self):
        self.docentes: List[Docente] = []

    def agregar(self, docente: Docente):
        self.docentes.append(docente)
