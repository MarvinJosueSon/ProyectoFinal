# DB_Manager.py
import sqlite3
from pathlib import Path
from typing import List, Optional
from Clases import Curso, Docente, Carrera, Estudiante

_DB_PATH = Path("data.db")

def _conn() -> sqlite3.Connection:
    con = sqlite3.connect(_DB_PATH)
    con.execute("PRAGMA foreign_keys = ON;")
    return con

def init_db() -> None:
    """Crea (si no existen) las tablas de la BD."""
    con = _conn()
    cur = con.cursor()

    # --- Cursos ---
    cur.execute("""
    CREATE TABLE IF NOT EXISTS cursos (
        id_curso TEXT PRIMARY KEY,
        nombre   TEXT NOT NULL
    );
    """)

    # --- Carreras ---
    cur.execute("""
    CREATE TABLE IF NOT EXISTS carreras (
        codigo TEXT PRIMARY KEY,
        nombre TEXT NOT NULL
    );
    """)

    # --- Docentes ---
    cur.execute("""
    CREATE TABLE IF NOT EXISTS docentes (
        codigo     TEXT PRIMARY KEY,
        nombre     TEXT NOT NULL,
        id_huella  INTEGER NOT NULL,
        usuario    TEXT NOT NULL UNIQUE,
        contrasena TEXT NOT NULL
    );
    """)

    # --- Estudiantes ---
    cur.execute("""
    CREATE TABLE IF NOT EXISTS estudiantes (
        codigo     TEXT PRIMARY KEY,
        nombre     TEXT NOT NULL,
        id_huella  INTEGER NOT NULL,
        id_carrera TEXT NOT NULL,
        FOREIGN KEY(id_carrera) REFERENCES carreras(codigo)
            ON UPDATE CASCADE
            ON DELETE RESTRICT
    );
    """)

    con.commit()
    con.close()


# CURSOS

def listar_cursos() -> List[Curso]:
    init_db()
    con = _conn(); cur = con.cursor()
    cur.execute("SELECT id_curso, nombre FROM cursos ORDER BY id_curso;")
    data = [Curso(idc, nom) for idc, nom in cur.fetchall()]
    con.close()
    return data

def obtener_curso(id_curso: str) -> Optional[Curso]:
    init_db()
    con = _conn(); cur = con.cursor()
    cur.execute("SELECT id_curso, nombre FROM cursos WHERE id_curso=?;", (id_curso,))
    row = cur.fetchone()
    con.close()
    return Curso(*row) if row else None

def insertar_curso(curso: Curso) -> None:
    init_db()
    con = _conn(); cur = con.cursor()
    cur.execute("INSERT INTO cursos(id_curso, nombre) VALUES(?,?);", (curso.id_curso, curso.nombre))
    con.commit(); con.close()

def actualizar_curso(old_id: str, nuevo: Curso) -> None:
    init_db()
    con = _conn(); cur = con.cursor()
    if old_id != nuevo.id_curso:
        cur.execute("UPDATE cursos SET id_curso=?, nombre=? WHERE id_curso=?;",
                    (nuevo.id_curso, nuevo.nombre, old_id))
    else:
        cur.execute("UPDATE cursos SET nombre=? WHERE id_curso=?;",
                    (nuevo.nombre, old_id))
    con.commit(); con.close()

def eliminar_curso(id_curso: str) -> None:
    init_db()
    con = _conn(); cur = con.cursor()
    cur.execute("DELETE FROM cursos WHERE id_curso=?;", (id_curso,))
    con.commit(); con.close()


# DOCENTES

def listar_docentes() -> List[Docente]:
    init_db()
    con = _conn(); cur = con.cursor()
    cur.execute("SELECT codigo, nombre, id_huella, usuario, contrasena FROM docentes ORDER BY codigo;")
    data = [Docente(c, n, int(h), u, p) for c, n, h, u, p in cur.fetchall()]
    con.close()
    return data

def obtener_docente_por_codigo(codigo: str) -> Optional[Docente]:
    init_db()
    con = _conn(); cur = con.cursor()
    cur.execute("SELECT codigo, nombre, id_huella, usuario, contrasena FROM docentes WHERE codigo=?;", (codigo,))
    row = cur.fetchone()
    con.close()
    return Docente(*row) if row else None

def obtener_docente_por_usuario(usuario: str) -> Optional[Docente]:
    init_db()
    con = _conn(); cur = con.cursor()
    cur.execute("SELECT codigo, nombre, id_huella, usuario, contrasena FROM docentes WHERE usuario=?;", (usuario,))
    row = cur.fetchone()
    con.close()
    return Docente(*row) if row else None

def obtener_docente_por_usuario_y_contrasena(usuario: str, contrasena: str) -> Optional[Docente]:
  
    init_db()
    con = _conn(); cur = con.cursor()
    cur.execute("""SELECT codigo, nombre, id_huella, usuario, contrasena
                   FROM docentes WHERE usuario=? AND contrasena=?;""", (usuario, contrasena))
    row = cur.fetchone()
    con.close()
    return Docente(*row) if row else None

def insertar_docente(docente: Docente) -> None:
    init_db()
    con = _conn(); cur = con.cursor()
    cur.execute("""INSERT INTO docentes(codigo, nombre, id_huella, usuario, contrasena)
                   VALUES(?,?,?,?,?);""",
                (docente.codigo, docente.nombre, int(docente.id_huella), docente.usuario, docente.contrasena))
    con.commit(); con.close()

def actualizar_docente(old_codigo: str, nuevo: Docente) -> None:
    init_db()
    con = _conn(); cur = con.cursor()
    if old_codigo != nuevo.codigo:
        cur.execute("""UPDATE docentes
                       SET codigo=?, nombre=?, id_huella=?, usuario=?, contrasena=?
                       WHERE codigo=?;""",
                    (nuevo.codigo, nuevo.nombre, int(nuevo.id_huella), nuevo.usuario, nuevo.contrasena, old_codigo))
    else:
        cur.execute("""UPDATE docentes
                       SET nombre=?, id_huella=?, usuario=?, contrasena=?
                       WHERE codigo=?;""",
                    (nuevo.nombre, int(nuevo.id_huella), nuevo.usuario, nuevo.contrasena, old_codigo))
    con.commit(); con.close()

def eliminar_docente(codigo: str) -> None:
    init_db()
    con = _conn(); cur = con.cursor()
    cur.execute("DELETE FROM docentes WHERE codigo=?;", (codigo,))
    con.commit(); con.close()


# CARRERAS

def listar_carreras() -> List[Carrera]:
    init_db()
    con = _conn(); cur = con.cursor()
    cur.execute("SELECT codigo, nombre FROM carreras ORDER BY codigo;")
    data = [Carrera(c, n) for c, n in cur.fetchall()]
    con.close()
    return data

def obtener_carrera(codigo: str) -> Optional[Carrera]:
    init_db()
    con = _conn(); cur = con.cursor()
    cur.execute("SELECT codigo, nombre FROM carreras WHERE codigo=?;", (codigo,))
    row = cur.fetchone()
    con.close()
    return Carrera(*row) if row else None

def insertar_carrera(carrera: Carrera) -> None:
    init_db()
    con = _conn(); cur = con.cursor()
    cur.execute("INSERT INTO carreras(codigo, nombre) VALUES(?,?);", (carrera.codigo, carrera.nombre))
    con.commit(); con.close()

def actualizar_carrera(old_codigo: str, nuevo: Carrera) -> None:
    """Si cambia el código, estudiantes.id_carrera se actualiza por ON UPDATE CASCADE."""
    init_db()
    con = _conn(); cur = con.cursor()
    if old_codigo != nuevo.codigo:
        cur.execute("UPDATE carreras SET codigo=?, nombre=? WHERE codigo=?;",
                    (nuevo.codigo, nuevo.nombre, old_codigo))
    else:
        cur.execute("UPDATE carreras SET nombre=? WHERE codigo=?;",
                    (nuevo.nombre, old_codigo))
    con.commit(); con.close()

def eliminar_carrera(codigo: str) -> None:
    init_db()
    con = _conn(); cur = con.cursor()
    cur.execute("DELETE FROM carreras WHERE codigo=?;", (codigo,))
    con.commit(); con.close()


# ESTUDIANTES
def listar_estudiantes() -> List[Estudiante]:
    init_db()
    con = _conn(); cur = con.cursor()
    cur.execute("SELECT codigo, nombre, id_huella, id_carrera FROM estudiantes ORDER BY codigo;")
    data = [Estudiante(c, n, int(h), ic) for c, n, h, ic in cur.fetchall()]
    con.close()
    return data

def obtener_estudiante(codigo: str) -> Optional[Estudiante]:
    init_db()
    con = _conn(); cur = con.cursor()
    cur.execute("SELECT codigo, nombre, id_huella, id_carrera FROM estudiantes WHERE codigo=?;", (codigo,))
    row = cur.fetchone()
    con.close()
    return Estudiante(*row) if row else None

def insertar_estudiante(est: Estudiante) -> None:
    init_db()
    con = _conn(); cur = con.cursor()
    cur.execute("""INSERT INTO estudiantes(codigo, nombre, id_huella, id_carrera)
                   VALUES(?,?,?,?);""",
                (est.codigo, est.nombre, int(est.id_huella), est.id_carrera))
    con.commit(); con.close()

def actualizar_estudiante(old_codigo: str, nuevo: Estudiante) -> None:
    init_db()
    con = _conn(); cur = con.cursor()
    if old_codigo != nuevo.codigo:
        cur.execute("""UPDATE estudiantes
                       SET codigo=?, nombre=?, id_huella=?, id_carrera=?
                       WHERE codigo=?;""",
                    (nuevo.codigo, nuevo.nombre, int(nuevo.id_huella), nuevo.id_carrera, old_codigo))
    else:
        cur.execute("""UPDATE estudiantes
                       SET nombre=?, id_huella=?, id_carrera=?
                       WHERE codigo=?;""",
                    (nuevo.nombre, int(nuevo.id_huella), nuevo.id_carrera, old_codigo))
    con.commit(); con.close()

def eliminar_estudiante(codigo: str) -> None:
    init_db()
    con = _conn(); cur = con.cursor()
    cur.execute("DELETE FROM estudiantes WHERE codigo=?;", (codigo,))
    con.commit(); con.close()
