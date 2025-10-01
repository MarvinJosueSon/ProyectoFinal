# CargarGuardar.py
from Clases import Curso, Docente, Carrera, Estudiante

def guardar_cursos(diccionario):
    with open("cursos.txt", "w", encoding="utf-8") as archivo:
        for c in diccionario.values():
            archivo.write(f"{c.id_curso}:{c.nombre}\n")

def cargar_cursos():
    dic = {}
    try:
        with open("cursos.txt", "r", encoding="utf-8") as f:
            for ln in f:
                ln = ln.strip()
                if not ln:
                    continue
                id_curso, nombre = ln.split(":", 1)
                dic[id_curso] = Curso(id_curso, nombre)
    except FileNotFoundError:
        pass
    return dic

def guardar_docentes(diccionario):
    with open("docentes.txt", "w", encoding="utf-8") as archivo:
        for d in diccionario.values():
            archivo.write(f"{d.codigo}|{d.nombre}|{d.id_huella}|{d.usuario}|{d.contrasena}\n")

def cargar_docentes():
    dic = {}
    try:
        # utf-8-sig elimina BOM si el archivo lo tiene
        with open("docentes.txt", "r", encoding="utf-8-sig") as f:
            linea_n = 0
            for ln in f:
                linea_n += 1
                ln = ln.strip()
                if not ln:
                    continue
                partes = ln.split("|")
                if len(partes) < 5:

                    continue

                codigo = partes[0].strip()
                nombre = partes[1].strip()
                id_huella_str = partes[2].strip()
                usuario = partes[3].strip()
                contrasena = partes[4].strip()
                if not id_huella_str.isdigit():

                    continue
                dic[codigo] = Docente(codigo, nombre, int(id_huella_str), usuario, contrasena)
    except FileNotFoundError:
        pass
    return dic

def guardar_carreras(diccionario):
    with open("carreras.txt", "w", encoding="utf-8") as archivo:
        for c in diccionario.values():
            archivo.write(f"{c.codigo}:{c.nombre}\n")

def cargar_carreras():
    dic = {}
    try:
        with open("carreras.txt", "r", encoding="utf-8") as f:
            for ln in f:
                ln = ln.strip()
                if not ln:
                    continue
                codigo, nombre = ln.split(":", 1)
                dic[codigo] = Carrera(codigo, nombre)
    except FileNotFoundError:
        pass
    return dic

def guardar_estudiantes(diccionario):
    with open("estudiantes.txt", "w", encoding="utf-8") as archivo:
        for e in diccionario.values():
            archivo.write(f"{e.codigo}|{e.nombre}|{e.id_huella}|{e.id_carrera}\n")

def cargar_estudiantes():
    dic = {}
    try:
        with open("estudiantes.txt", "r", encoding="utf-8") as f:
            for ln in f:
                ln = ln.strip()
                if not ln:
                    continue
                partes = ln.split("|")
                if len(partes) < 4:
                    continue
                codigo, nombre, id_huella, id_carrera = partes[:4]
                dic[codigo] = Estudiante(codigo, nombre, int(id_huella), id_carrera)
    except FileNotFoundError:
        pass
    return dic
