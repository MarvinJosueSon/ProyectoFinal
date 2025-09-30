# CargarGuardar.py
from Clases import Curso

def guardar_cursos(diccionario):
    with open("cursos.txt", "w", encoding="utf-8") as archivo:
        for curso in diccionario.values():
            archivo.write(f"{curso.id_curso}:{curso.nombre}\n")

def cargar_cursos():
    diccionario = {}
    try:
        with open("cursos.txt", "r", encoding="utf-8") as archivo:
            for linea in archivo:
                linea = linea.strip()
                if not linea:
                    continue
                id_curso, nombre = linea.split(":", 1)
                diccionario[id_curso] = Curso(id_curso, nombre)
    except FileNotFoundError:
        pass
    return diccionario
