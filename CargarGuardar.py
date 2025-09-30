# CargarGuardar.py
from Clases import Curso, Docente

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

def guardar_docentes(diccionario):
    with open("docentes.txt", "w", encoding="utf-8") as archivo:
        for d in diccionario.values():
            ids_cursos = ",".join(d.cursos.keys())
            archivo.write(f"{d.codigo}|{d.nombre}|{d.id_huella}|{d.usuario}|{d.contrasena}|{ids_cursos}\n")

def cargar_docentes(cursos_existentes):
    diccionario = {}
    try:
        with open("docentes.txt", "r", encoding="utf-8") as archivo:
            for linea in archivo:
                linea = linea.strip()
                if not linea:
                    continue
                codigo, nombre, id_huella, usuario, contrasena, ids = linea.split("|")
                ids_lista = [x for x in ids.split(",") if x] if ids else []
                cursos_map = {cid: (cursos_existentes[cid].nombre if cid in cursos_existentes else cid) for cid in ids_lista}
                diccionario[codigo] = Docente(codigo, nombre, int(id_huella), usuario, contrasena, cursos_map)
    except FileNotFoundError:
        pass
    return diccionario
