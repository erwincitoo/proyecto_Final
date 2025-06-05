import ttkbootstrap as ttk
import os
import subprocess
import sys
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from cryptography.fernet import Fernet

# ENCRIPTAR

def generar_clave():
    clave = Fernet.generate_key()
    with open("clave.key", "wb") as archivo_clave:
        archivo_clave.write(clave)

def cargar_clave():
    if not os.path.exists("clave.key"):
        generar_clave()
    with open("clave.key", "rb") as archivo_clave:
        return archivo_clave.read()

def encriptar_datos(nombre, usuario, contrasena):
    clave = cargar_clave()
    fernet = Fernet(clave)
    nombre_encriptado = fernet.encrypt(nombre.encode())
    usuario_encriptado = fernet.encrypt(usuario.encode())
    contrasena_encriptada = fernet.encrypt(contrasena.encode())
    return nombre_encriptado, usuario_encriptado, contrasena_encriptada

# LEER ROL 

def obtener_rol_actual():
    if not os.path.exists("rol_actual.txt"):
        Messagebox.show_error("No se encontró 'rol_actual.txt'.", "Error")
        sys.exit(1)

    with open("rol_actual.txt", "r") as archivo:
        rol_leido = archivo.read().strip().lower()
        if rol_leido not in ["usuario", "trabajador"]:
            Messagebox.show_error("Rol inválido en 'rol_actual.txt'.", "Error")
            sys.exit(1)
        return rol_leido

rol = obtener_rol_actual()

# REGISTRO

def registrar():
    nombre = nombre_entry.get().strip()
    usuario = usuario_entry.get().strip()
    contrasena = contrasena_entry.get().strip()

    if not nombre or not usuario or not contrasena:
        Messagebox.show_error("Por favor, completa todos los campos.", "Error")
        return

    if os.path.exists("cuentas.txt"):
        clave = cargar_clave()
        fernet = Fernet(clave)
        with open("cuentas.txt", "rb") as archivo:
            for linea in archivo:
                partes = linea.strip().split(b"|")
                if len(partes) != 4:
                    continue
                _, _, usuario_guardado, _ = partes
                try:
                    usuario_descifrado = fernet.decrypt(usuario_guardado).decode()
                    if usuario == usuario_descifrado:
                        Messagebox.show_error("Este usuario ya está registrado.", "Error")
                        return
                except Exception:
                    continue

    nombre_enc, usuario_enc, contrasena_enc = encriptar_datos(nombre, usuario, contrasena)

    with open("cuentas.txt", "ab") as archivo:
        linea = rol.encode() + b"|" + nombre_enc + b"|" + usuario_enc + b"|" + contrasena_enc + b"\n"
        archivo.write(linea)

    Messagebox.show_info("Cuenta creada exitosamente.", "Registro completado")
    ventana.destroy()

    if rol == "usuario":
        ruta = os.path.join(os.path.dirname(__file__), "mostrarcarro.py")
    else:
        ruta = os.path.join(os.path.dirname(__file__), "tree.py")

    subprocess.run([sys.executable, ruta], shell=True)

#VOLVER A INICIO 

def ir_a_inicio():
    ventana.destroy()
    ruta = os.path.join(os.path.dirname(__file__), "inicio.py")
    subprocess.run([sys.executable, ruta], shell=True)

# VENTANA PRINCIPAL

ventana = ttk.Window(themename="flatly")
ventana.title("PANTALLA - REGISTRO")
ventana.geometry("700x500")
ventana.resizable(0, 0)

frame = ttk.Frame(ventana)
frame.pack()

registro_frame = ttk.LabelFrame(frame, text="CREAR CUENTA NUEVA", bootstyle="primary", padding=20)
registro_frame.grid(row=0, column=0, padx=20, pady=20)

ttk.Label(registro_frame, text="NOMBRE:", font=("Courier", 12, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 5))
nombre_entry = ttk.Entry(registro_frame, width=40)
nombre_entry.grid(row=1, column=0, pady=(0, 10))

ttk.Label(registro_frame, text="USUARIO:", font=("Courier", 12, "bold")).grid(row=2, column=0, sticky="w", pady=(0, 5))
usuario_entry = ttk.Entry(registro_frame, width=40)
usuario_entry.grid(row=3, column=0, pady=(0, 10))

ttk.Label(registro_frame, text="CONTRASEÑA:", font=("Courier", 12, "bold")).grid(row=4, column=0, sticky="w", pady=(0, 5))
contrasena_entry = ttk.Entry(registro_frame, width=40, show="*")
contrasena_entry.grid(row=5, column=0, pady=(0, 20))

ttk.Button(registro_frame, text="REGISTRAR", width=31, bootstyle="success", command=registrar).grid(row=6, column=0, pady=10)
ttk.Button(registro_frame, text="VOLVER AL INICIO", width=31, bootstyle="secondary", command=ir_a_inicio).grid(row=7, column=0)

ventana.mainloop()
