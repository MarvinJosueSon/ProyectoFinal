# Clases.py
from typing import List, Dict, Optional, Callable
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
    def __init__(self, codigo: str, nombre: str, id_huella: int, usuario: str, contrasena: str):
        super().__init__(codigo, nombre, id_huella)
        self.usuario = usuario
        self.contrasena = contrasena

class Administrador(Persona):
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
    def __init__(self, fecha: str, id_curso: str, ids_estudiantes: List[str], id_docente: str):
        self.fecha = fecha
        self.id_curso = id_curso
        self.ids_estudiantes = ids_estudiantes
        self.id_docente = id_docente

class ControlAsistencia:
    def __init__(self, hora_entrada: Optional[datetime] = None, hora_salida: Optional[datetime] = None):
        self.hora_entrada = hora_entrada
        self.hora_salida = hora_salida
    def verificado(self) -> bool:
        return self.hora_entrada is not None and self.hora_salida is not None
    def registro(self):
        return {"hora_entrada": self.hora_entrada, "hora_salida": self.hora_salida}

def ordenar_quicksort(lista: List, clave: Callable) -> List:
    if len(lista) <= 1:
        return lista
    pivote = lista[len(lista) // 2]
    valor_pivote = clave(pivote)
    izquierda = [x for x in lista if clave(x) < valor_pivote]
    medio = [x for x in lista if clave(x) == valor_pivote]
    derecha = [x for x in lista if clave(x) > valor_pivote]
    return ordenar_quicksort(izquierda, clave) + medio + ordenar_quicksort(derecha, clave)

class Buscador:
    def __init__(self, diccionario: Dict[str, object]):
        self.diccionario = diccionario
    def buscar(self, codigo: str):
        return self.diccionario.get(codigo)

class Eliminador:
    def __init__(self, diccionario: Dict[str, object]):
        self.diccionario = diccionario
    def eliminar(self, codigo: str) -> bool:
        return self.diccionario.pop(codigo, None) is not None

class AdministrarAdministradores:
    def __init__(self):
        self.administradores: Dict[str, Administrador] = {}
    def agregar(self, administrador: Administrador):
        self.administradores[administrador.codigo] = administrador
    def obtener(self, codigo: str) -> Optional[Administrador]:
        return self.administradores.get(codigo)
    def eliminar(self, codigo: str) -> bool:
        return self.administradores.pop(codigo, None) is not None
    def listar(self) -> List[Administrador]:
        return list(self.administradores.values())

class AdministrarEstudiantes:
    def __init__(self):
        self.estudiantes: Dict[str, Estudiante] = {}
    def agregar(self, estudiante: Estudiante):
        self.estudiantes[estudiante.codigo] = estudiante
    def obtener(self, codigo: str) -> Optional[Estudiante]:
        return self.estudiantes.get(codigo)
    def eliminar(self, codigo: str) -> bool:
        return self.estudiantes.pop(codigo, None) is not None
    def listar(self) -> List[Estudiante]:
        return list(self.estudiantes.values())

class AdministrarDocentes:
    def __init__(self):
        self.docentes: Dict[str, Docente] = {}
    def agregar(self, docente: Docente):
        self.docentes[docente.codigo] = docente
    def obtener(self, codigo: str) -> Optional[Docente]:
        return self.docentes.get(codigo)
    def eliminar(self, codigo: str) -> bool:
        return self.docentes.pop(codigo, None) is not None
    def buscar_por_usuario(self, usuario: str) -> Optional[Docente]:
        for d in self.docentes.values():
            if d.usuario == usuario:
                return d
        return None
    def listar(self) -> List[Docente]:
        return list(self.docentes.values())
