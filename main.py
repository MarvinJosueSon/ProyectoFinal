import os
import sys
import subprocess
from pathlib import Path

def main():

    project_dir = Path(__file__).resolve().parent
    base_path = project_dir / "Base.py"

    # Validar existencia de Base.py
    if not base_path.exists():
        print("No se encontró 'Base.py' en la carpeta del proyecto.")
        print(f"Ruta esperada: {base_path}")
        sys.exit(1)

    # Cambiar directorio de trabajo al del proyecto
    os.chdir(project_dir)

    print("🚀 Iniciando sistema de asistencia...")
    print(f"📂 Directorio actual: {project_dir}")
    print(f"▶ Ejecutando: {base_path.name}")

    # Ejecutar Base.py con el mismo intérprete
    try:
        subprocess.run([sys.executable, str(base_path)], check=True)
    except subprocess.CalledProcessError as e:
        print("Error al ejecutar Base.py")
        print("Código de salida:", e.returncode)
        sys.exit(e.returncode)
    except Exception as e:
        print("⚠️ Error inesperado:", e)
        sys.exit(1)

if __name__ == "__main__":
    main()
