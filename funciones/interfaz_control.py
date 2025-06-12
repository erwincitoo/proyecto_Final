# interfaz.py
import os
import subprocess
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox

from .funciones_control import (
    base_path, cargar_imagen, encriptar_datos, cargar_clave,
    guardar_rol, obtener_rol_actual
)

from cryptography.fernet import Fernet

# Variables globales
ventana = None
frame_personal = None
frame_inicio = None
frame_registro = None
usuario_entry = None
contrasena_entry = None
nombre_entry = None
usuario_reg_entry = None
contrasena_reg_entry = None

def mostrar_frame(frame_a_mostrar):
    for f in [frame_personal, frame_inicio, frame_registro]:
        if f is not None:
            f.pack_forget()
    if frame_a_mostrar:
        frame_a_mostrar.pack(fill=BOTH, expand=YES)

def limpiar_campos_inicio():
    usuario_entry.delete(0, 'end')
    contrasena_entry.delete(0, 'end')

def limpiar_campos_registro():
    nombre_entry.delete(0, 'end')
    usuario_reg_entry.delete(0, 'end')
    contrasena_reg_entry.delete(0, 'end')

def seleccionar_rol_y_abrir_inicio(rol):
    guardar_rol(rol)
    mostrar_frame(frame_inicio)
    limpiar_campos_inicio()

def iniciar_sesion():
    usuario = usuario_entry.get().strip()
    contrasena = contrasena_entry.get().strip()

    if not usuario or not contrasena:
        Messagebox.show_error("Por favor, completa todos los campos.", "Error")
        return

    cuentas_path = os.path.join(base_path, "cuentas.txt")
    if not os.path.exists(cuentas_path):
        Messagebox.show_error("No hay cuentas registradas aún.", "Error")
        return

    clave = cargar_clave()
    fernet = Fernet(clave)

    with open(cuentas_path, "rb") as archivo:
        for linea in archivo:
            partes = linea.strip().split(b"|")
            if len(partes) != 4:
                continue
            rol_guardado, nombre_enc, usuario_guardado, contrasena_guardada = partes
            try:
                usuario_desc = fernet.decrypt(usuario_guardado).decode()
                contrasena_desc = fernet.decrypt(contrasena_guardada).decode()
                if usuario == usuario_desc and contrasena == contrasena_desc:
                    mostrar_frame(None)
                    Messagebox.show_info(f"Bienvenido {rol_guardado.decode()}.", "Acceso")
                    if rol_guardado.decode() == "usuario":
                        subprocess.run(["python", "main.py"])
                    elif rol_guardado.decode() == "trabajador":
                        subprocess.run(["python", "main2.py"])
                    return
            except Exception as e:
                print(f"Error al descifrar: {e}")
    Messagebox.show_error("Credenciales incorrectas.", "Error")

def ir_a_registro():
    mostrar_frame(frame_registro)
    limpiar_campos_registro()

def volver_a_inicio():
    mostrar_frame(frame_inicio)
    limpiar_campos_inicio()

def registrar():
    nombre = nombre_entry.get().strip()
    usuario = usuario_reg_entry.get().strip()
    contrasena = contrasena_reg_entry.get().strip()

    if not nombre or not usuario or not contrasena:
        Messagebox.show_error("Por favor, completa todos los campos.", "Error")
        return

    cuentas_path = os.path.join(base_path, "cuentas.txt")

    clave = cargar_clave()
    fernet = Fernet(clave)

    if os.path.exists(cuentas_path):
        with open(cuentas_path, "rb") as archivo:
            for linea in archivo:
                partes = linea.strip().split(b"|")
                if len(partes) != 4:
                    continue
                _, _, usuario_guardado, _ = partes
                try:
                    if usuario == fernet.decrypt(usuario_guardado).decode():
                        Messagebox.show_error("Este usuario ya está registrado.", "Error")
                        return
                except:
                    continue

    rol = obtener_rol_actual()
    nombre_enc, usuario_enc, contrasena_enc = encriptar_datos(nombre, usuario, contrasena)

    with open(cuentas_path, "ab") as archivo:
        archivo.write(rol.encode() + b"|" + nombre_enc + b"|" + usuario_enc + b"|" + contrasena_enc + b"\n")

    Messagebox.show_info("Cuenta creada exitosamente.", "Registro")
    mostrar_frame(frame_inicio)
    limpiar_campos_inicio()

def ventana_main():
    global ventana, frame_personal, frame_inicio, frame_registro
    global usuario_entry, contrasena_entry, nombre_entry, usuario_reg_entry, contrasena_reg_entry

    ventana = ttk.Window(themename="flatly")
    ventana.title("CONTROL DE USUARIOS")
    ventana.geometry("700x500")
    ventana.resizable(False, False)

    # --- FRAME SELECCIÓN DE ROL ---
    frame_personal = ttk.Frame(ventana, padding=20)
    frame_personal.pack(expand=True)

    ttk.Label(frame_personal, text="¿CÓMO DESEAS INGRESAR?", font=("Courier", 22, "bold")).pack(pady=(0, 40))

    frame_roles = ttk.Frame(frame_personal)
    frame_roles.pack()

    img_trabajador = cargar_imagen(os.path.join(base_path, "trabajador.png"))
    img_usuario = cargar_imagen(os.path.join(base_path, "usuario.png"))

    # Trabajador
    frame_trabajador = ttk.Frame(frame_roles)
    frame_trabajador.pack(side=LEFT, padx=40)
    if img_trabajador:
        ttk.Label(frame_trabajador, image=img_trabajador).pack()
    ttk.Button(frame_trabajador, text="SOY TRABAJADOR", bootstyle="success-outline", width=20,
               command=lambda: seleccionar_rol_y_abrir_inicio("trabajador")).pack(pady=10)

    # Usuario
    frame_usuario = ttk.Frame(frame_roles)
    frame_usuario.pack(side=LEFT, padx=40)
    if img_usuario:
        ttk.Label(frame_usuario, image=img_usuario).pack()
    ttk.Button(frame_usuario, text="SOY USUARIO", bootstyle="info-outline", width=20,
               command=lambda: seleccionar_rol_y_abrir_inicio("usuario")).pack(pady=10)

    ventana.img_trabajador = img_trabajador
    ventana.img_usuario = img_usuario

    # --- LOGIN ---
    frame_inicio = ttk.Frame(ventana, padding=20)
    login_frame = ttk.LabelFrame(frame_inicio, text="INICIO DE SESIÓN", bootstyle="primary", padding=20, width=500, height=300)
    login_frame.pack(expand=True)
    login_frame.pack_propagate(False)

    ttk.Label(login_frame, text="USUARIO:").pack(anchor="w")
    usuario_entry = ttk.Entry(login_frame, width=50)
    usuario_entry.pack()

    ttk.Label(login_frame, text="CONTRASEÑA:").pack(anchor="w")
    contrasena_entry = ttk.Entry(login_frame, width=50, show="*")
    contrasena_entry.pack()

    ttk.Button(login_frame, text="INICIAR SESIÓN", bootstyle="success", command=iniciar_sesion).pack(pady=5)
    ttk.Button(login_frame, text="REGISTRARSE", bootstyle="secondary", command=ir_a_registro).pack()

    # --- REGISTRO ---
    frame_registro = ttk.Frame(ventana, padding=20)
    registro_frame = ttk.LabelFrame(frame_registro, text="REGISTRO", bootstyle="info", padding=20, width=500, height=400)
    registro_frame.pack(expand=True)
    registro_frame.pack_propagate(False)

    ttk.Label(registro_frame, text="NOMBRE:").pack(anchor="w")
    nombre_entry = ttk.Entry(registro_frame, width=50)
    nombre_entry.pack()

    ttk.Label(registro_frame, text="USUARIO:").pack(anchor="w")
    usuario_reg_entry = ttk.Entry(registro_frame, width=50)
    usuario_reg_entry.pack()

    ttk.Label(registro_frame, text="CONTRASEÑA:").pack(anchor="w")
    contrasena_reg_entry = ttk.Entry(registro_frame, width=50, show="*")
    contrasena_reg_entry.pack()

    ttk.Button(registro_frame, text="REGISTRAR", bootstyle="success", command=registrar).pack(pady=5)
    ttk.Button(registro_frame, text="VOLVER", bootstyle="secondary", command=volver_a_inicio).pack()

    mostrar_frame(frame_personal)
    ventana.mainloop()
