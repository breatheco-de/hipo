import os

def generate_pretty_structure(ignore_list, output_file="structure.txt"):
    """
    Genera un archivo con la estructura jerárquica del proyecto, ignorando archivos y directorios según una lista.

    :param ignore_list: Lista de patrones o nombres de archivos/directorios a ignorar.
    :param output_file: Nombre del archivo de salida (por defecto 'structure.txt').
    """
    def is_ignored(path):
        """Comprueba si un archivo o directorio debe ser ignorado."""
        for pattern in ignore_list:
            if pattern in path:
                return True
        return False

    def walk_directory(root_dir, prefix=""):
        """Recorre el directorio y genera la estructura jerárquica."""
        entries = sorted(os.listdir(root_dir))  # Ordenar para consistencia
        entries = [e for e in entries if not is_ignored(os.path.join(root_dir, e))]

        for index, entry in enumerate(entries):
            path = os.path.join(root_dir, entry)
            connector = "└── " if index == len(entries) - 1 else "├── "

            # Escribe la línea actual
            f.write(f"{prefix}{connector}{entry}\n")

            # Si es un directorio, recorrer recursivamente
            if os.path.isdir(path):
                extension = "    " if index == len(entries) - 1 else "│   "
                walk_directory(path, prefix + extension)

    # Cambiar a encoding "utf-8" para soportar caracteres especiales
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(".\n")  # Raíz del proyecto
        walk_directory(".", "")

    print(f"Estructura del proyecto guardada en '{output_file}'")


if __name__ == "__main__":
    # Define aquí tu lista de patrones a ignorar
    ignore_list = [
        ".git",  # Ignorar el directorio .git
        "__pycache__",  # Ignorar carpetas de caché de Python
        ".DS_Store",  # Ignorar archivos de macOS
        "node_modules",  # Ignorar directorio de dependencias de Node.js
        "*.pyc",  # Ignorar archivos compilados de Python
        "tests",  # Ignorar directorio de pruebas
        "venv",  # Ignorar entorno virtual
    ]
    generate_pretty_structure(ignore_list)
