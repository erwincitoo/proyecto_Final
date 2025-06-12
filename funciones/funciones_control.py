# control_usuarios.py
import os
import sys
from cryptography.fernet import Fernet
from PIL import Image, ImageTk
from ttkbootstrap.dialogs import Messagebox


base_path = os.path.dirname(__file__)
clave_path = os.path.join(base_path, "clave.key")
rol_path = os.path.join(base_path, "rol_actual.txt")
cuentas_path = os.path.join(base_path, "cuentas.txt")


# ----------------- ENCRIPTACIÓN -----------------
def generar_clave():
    if not os.path.exists(clave_path):
        clave = Fernet.generate_key()
        with open(clave_path, "wb") as archivo_clave:
            archivo_clave.write(clave)


def cargar_clave():
    if not os.path.exists(clave_path):
        generar_clave()
    with open(clave_path, "rb") as archivo_clave:
        return archivo_clave.read()


def encriptar_datos(nombre, usuario, contrasena):
    clave = cargar_clave()
    fernet = Fernet(clave)
    return (
        fernet.encrypt(nombre.encode()),
        fernet.encrypt(usuario.encode()),
        fernet.encrypt(contrasena.encode())
    )


def desencriptar(texto_encriptado):
    clave = cargar_clave()
    fernet = Fernet(clave)
    return fernet.decrypt(texto_encriptado).decode()


# ----------------- CONTROL DE ROL -----------------
def guardar_rol(rol):
    with open(rol_path, "w") as f:
        f.write(rol)


def obtener_rol_actual():
    if not os.path.exists(rol_path):
        Messagebox.show_error("No se encontró 'rol_actual.txt'.", "Error")
        sys.exit(1)
    with open(rol_path, "r") as archivo:
        rol_leido = archivo.read().strip().lower()
        if rol_leido not in ["usuario", "trabajador"]:
            Messagebox.show_error("Rol inválido en 'rol_actual.txt'.", "Error")
            sys.exit(1)
        return rol_leido


# ----------------- UTILIDAD DE IMÁGENES -----------------
def cargar_imagen(ruta, tamaño=(200, 200)):
    try:
        img_pil = Image.open(ruta)
        img_pil = img_pil.resize(tamaño, Image.LANCZOS)
        return ImageTk.PhotoImage(img_pil)
    except FileNotFoundError:
        print(f"Error: Imagen no encontrada en {ruta}")
        return None
