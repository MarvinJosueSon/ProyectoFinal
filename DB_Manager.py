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
        codigo TEXT(50) PRIMARY KEY,
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
    # --- Sesiones de asistencia (cabecera) ---
    cur.execute("""
    CREATE TABLE IF NOT EXISTS sesiones_asistencia (
        id               INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha            TEXT NOT NULL,              -- YYYY-MM-DD
        hora_inicio      TEXT NOT NULL,              -- HH:MM:SS
        hora_fin         TEXT,                       -- HH:MM:SS (al cerrar)
        jornada          TEXT NOT NULL,              -- Matutina / Vespertina / FDS
        docente_usuario  TEXT NOT NULL,              -- usuario del docente (o código si prefieres)
        id_carrera       TEXT NOT NULL,              -- código carrera (p.ej. C20251)
        id_curso         TEXT NOT NULL               -- id_curso (p.ej. SIS101)
    );
    """)

    # --- Eventos (cada verificación exitosa, 1 por estudiante por sesión) ---
    cur.execute("""
    CREATE TABLE IF NOT EXISTS asistencias_eventos (
        id                 INTEGER PRIMARY KEY AUTOINCREMENT,
        sesion_id          INTEGER NOT NULL,
        codigo_estudiante  TEXT NOT NULL,
        id_huella          INTEGER NOT NULL,
        hora_evento        TEXT NOT NULL,            -- HH:MM:SS
        UNIQUE(sesion_id, codigo_estudiante),
        FOREIGN KEY(sesion_id) REFERENCES sesiones_asistencia(id) ON DELETE CASCADE
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
def buscar_cursos(term: str) -> List[Curso]:
    """Búsqueda case-insensitive por id_curso o nombre."""
    init_db()
    con = _conn(); cur = con.cursor()
    like = f"%{term.lower()}%"
    cur.execute("""
        SELECT id_curso, nombre
        FROM cursos
        WHERE LOWER(id_curso) LIKE ? OR LOWER(nombre) LIKE ?
        ORDER BY id_curso;
    """, (like, like))
    data = [Curso(idc, nom) for idc, nom in cur.fetchall()]
    con.close()
    return data

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

def buscar_docentes(term: str) -> List[Docente]:
    """Búsqueda case-insensitive por código, nombre, usuario.
    Si 'term' es numérico, también filtra por id_huella."""
    init_db()
    con = _conn(); cur = con.cursor()
    like = f"%{term.lower()}%"
    if term.isdigit():
        cur.execute("""
            SELECT codigo, nombre, id_huella, usuario, contrasena
            FROM docentes
            WHERE LOWER(codigo) LIKE ? OR LOWER(nombre) LIKE ?
               OR LOWER(usuario) LIKE ? OR id_huella = ?
            ORDER BY codigo;
        """, (like, like, like, int(term)))
    else:
        cur.execute("""
            SELECT codigo, nombre, id_huella, usuario, contrasena
            FROM docentes
            WHERE LOWER(codigo) LIKE ? OR LOWER(nombre) LIKE ?
               OR LOWER(usuario) LIKE ?
            ORDER BY codigo;
        """, (like, like, like))
    data = [Docente(c, n, int(h), u, p) for c, n, h, u, p in cur.fetchall()]
    con.close()
    return data

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

def buscar_carreras(term: str) -> List[Carrera]:
    """Búsqueda case-insensitive por código o nombre de carrera."""
    init_db()
    con = _conn(); cur = con.cursor()
    like = f"%{term.lower()}%"
    cur.execute("""
        SELECT codigo, nombre
        FROM carreras
        WHERE LOWER(codigo) LIKE ? OR LOWER(nombre) LIKE ?
        ORDER BY codigo;
    """, (like, like))
    data = [Carrera(c, n) for c, n in cur.fetchall()]
    con.close()
    return data

# ESTUDIANTES
def listar_estudiantes_por_carrera(id_carrera: str) -> List[Estudiante]:
    init_db()
    con = _conn(); cur = con.cursor()
    cur.execute("""
        SELECT codigo, nombre, id_huella, id_carrera
        FROM estudiantes
        WHERE id_carrera = ?
        ORDER BY codigo;
    """, (id_carrera,))
    data = [Estudiante(c, n, int(h), ic) for c, n, h, ic in cur.fetchall()]
    con.close()
    return data

def obtener_estudiante_por_huella(id_huella: int) -> Optional[Estudiante]:
    init_db()
    con = _conn(); cur = con.cursor()
    cur.execute("""
        SELECT codigo, nombre, id_huella, id_carrera
        FROM estudiantes
        WHERE id_huella = ?;
    """, (int(id_huella),))
    row = cur.fetchone()
    con.close()
    return Estudiante(*row) if row else None

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
def buscar_estudiantes(term: str) -> List[Estudiante]:
    """Búsqueda case-insensitive por código, nombre, carrera (código o nombre).
    Si 'term' es numérico, también filtra por id_huella (exacto)."""
    init_db()
    con = _conn(); cur = con.cursor()
    like = f"%{term.lower()}%"
    if term.isdigit():
        cur.execute("""
            SELECT e.codigo, e.nombre, e.id_huella, e.id_carrera
            FROM estudiantes e
            LEFT JOIN carreras c ON c.codigo = e.id_carrera
            WHERE LOWER(e.codigo)   LIKE ?
               OR LOWER(e.nombre)   LIKE ?
               OR LOWER(e.id_carrera) LIKE ?
               OR LOWER(c.nombre)   LIKE ?
               OR e.id_huella = ?
            ORDER BY e.codigo;
        """, (like, like, like, like, int(term)))
    else:
        cur.execute("""
            SELECT e.codigo, e.nombre, e.id_huella, e.id_carrera
            FROM estudiantes e
            LEFT JOIN carreras c ON c.codigo = e.id_carrera
            WHERE LOWER(e.codigo)   LIKE ?
               OR LOWER(e.nombre)   LIKE ?
               OR LOWER(e.id_carrera) LIKE ?
               OR LOWER(c.nombre)   LIKE ?
            ORDER BY e.codigo;
        """, (like, like, like, like))
    data = [Estudiante(cod, nom, int(h), car) for cod, nom, h, car in cur.fetchall()]
    con.close()
    return data

def huella_en_uso(id_huella: int) -> bool:
    init_db()
    con = _conn(); cur = con.cursor()
    cur.execute("SELECT 1 FROM docentes WHERE id_huella = ? LIMIT 1;", (int(id_huella),))
    if cur.fetchone():
        con.close(); return True
    cur.execute("SELECT 1 FROM estudiantes WHERE id_huella = ? LIMIT 1;", (int(id_huella),))
    usado = cur.fetchone() is not None
    con.close()
    return usado

def sugerir_id_huella_libre(min_id: int = 1, max_id: int = 127):
    init_db()
    con = _conn(); cur = con.cursor()
    cur.execute("SELECT id_huella FROM docentes WHERE id_huella BETWEEN ? AND ?;", (min_id, max_id))
    usados_doc = {int(x[0]) for x in cur.fetchall() if x[0] is not None}
    cur.execute("SELECT id_huella FROM estudiantes WHERE id_huella BETWEEN ? AND ?;", (min_id, max_id))
    usados_est = {int(x[0]) for x in cur.fetchall() if x[0] is not None}
    con.close()
    usados = usados_doc | usados_est
    for i in range(min_id, max_id + 1):
        if i not in usados:
            return i
    return None
def crear_sesion_asistencia(fecha: str, hora_inicio: str, jornada: str,
                            docente_usuario: str, id_carrera: str, id_curso: str) -> int:
    init_db()
    con = _conn(); cur = con.cursor()
    cur.execute("""
        INSERT INTO sesiones_asistencia(fecha, hora_inicio, jornada, docente_usuario, id_carrera, id_curso)
        VALUES(?,?,?,?,?,?);
    """, (fecha, hora_inicio, jornada, docente_usuario, id_carrera, id_curso))
    sesion_id = cur.lastrowid
    con.commit(); con.close()
    return sesion_id

def cerrar_sesion_asistencia(sesion_id: int, hora_fin: str) -> None:
    init_db()
    con = _conn(); cur = con.cursor()
    cur.execute("""
        UPDATE sesiones_asistencia
        SET hora_fin = ?
        WHERE id = ?;
    """, (hora_fin, int(sesion_id)))
    con.commit(); con.close()

def registrar_evento_asistencia(sesion_id: int, codigo_estudiante: str, id_huella: int, hora_evento: str) -> None:
    init_db()
    con = _conn(); cur = con.cursor()
    try:
        cur.execute("""
            INSERT OR IGNORE INTO asistencias_eventos(sesion_id, codigo_estudiante, id_huella, hora_evento)
            VALUES(?,?,?,?);
        """, (int(sesion_id), codigo_estudiante, int(id_huella), hora_evento))
        con.commit()
    finally:
        con.close()

def listar_sesiones() -> list[tuple]:
    init_db()
    con = _conn(); cur = con.cursor()
    cur.execute("""
        SELECT id, fecha, hora_inicio, hora_fin, jornada, docente_usuario, id_carrera, id_curso
        FROM sesiones_asistencia
        ORDER BY id DESC;
    """)
    rows = cur.fetchall()
    con.close()
    return rows

def listar_eventos_por_sesion(sesion_id: int) -> list[tuple]:
    init_db()
    con = _conn(); cur = con.cursor()
    cur.execute("""
        SELECT codigo_estudiante, id_huella, hora_evento
        FROM asistencias_eventos
        WHERE sesion_id = ?
        ORDER BY hora_evento ASC;
    """, (int(sesion_id),))
    rows = cur.fetchall()
    con.close()
    return rows
