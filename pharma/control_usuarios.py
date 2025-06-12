import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from PIL import Image, ImageTk
import os
import sys
from cryptography.fernet import Fernet

# -------------------------------------
# FUNCIONES DE ENCRIPTACION (inicio y registro)
# -------------------------------------

def generar_clave():
    clave_path = os.path.join(base_path, "clave.key")
    if not os.path.exists(clave_path):
        clave = Fernet.generate_key()
        with open(clave_path, "wb") as archivo_clave:
            archivo_clave.write(clave)

def cargar_clave():
    clave_path = os.path.join(base_path, "clave.key")
    if not os.path.exists(clave_path):
        generar_clave()
    with open(clave_path, "rb") as archivo_clave:
        return archivo_clave.read()

def encriptar_datos(nombre, usuario, contrasena):
    clave = cargar_clave()
    fernet = Fernet(clave)
    nombre_encriptado = fernet.encrypt(nombre.encode())
    usuario_encriptado = fernet.encrypt(usuario.encode())
    contrasena_encriptada = fernet.encrypt(contrasena.encode())
    return nombre_encriptado, usuario_encriptado, contrasena_encriptada

def desencriptar(texto_encriptado):
    clave = cargar_clave()
    fernet = Fernet(clave)
    return fernet.decrypt(texto_encriptado).decode()

# -------------------------------------
# FUNCIONES DE CONTROL DE ROL (personal.py)
# -------------------------------------

def guardar_rol(rol):
    rol_path = os.path.join(base_path, "rol_actual.txt")
    with open(rol_path, "w") as f:
        f.write(rol)

def obtener_rol_actual():
    rol_path = os.path.join(base_path, "rol_actual.txt")
    if not os.path.exists(rol_path):
        Messagebox.show_error("No se encontró 'rol_actual.txt'.", "Error")
        sys.exit(1)
    with open(rol_path, "r") as archivo:
        rol_leido = archivo.read().strip().lower()
        if rol_leido not in ["usuario", "trabajador"]:
            Messagebox.show_error("Rol inválido en 'rol_actual.txt'.", "Error")
            sys.exit(1)
        return rol_leido

# -------------------------------------
# FUNCIONES DE IMAGENES (personal.py)
# -------------------------------------

def cargar_imagen(ruta, tamaño=(200, 200)):
    try:
        img_pil = Image.open(ruta)
        img_pil = img_pil.resize(tamaño, Image.LANCZOS)
        return ImageTk.PhotoImage(img_pil)
    except FileNotFoundError:
        print(f"Error: Imagen no encontrada en {ruta}")
        return None

# -------------------------------------
# FUNCIONES DE NAVEGACION Y LOGICA
# -------------------------------------

def mostrar_frame(frame_a_mostrar):
    # Oculta todos los frames, muestra solo el frame pedido
    for f in [frame_personal, frame_inicio, frame_registro]:
        f.pack_forget()
    frame_a_mostrar.pack(fill=BOTH, expand=YES)

# Desde pantalla de selección de rol (personal.py)
def seleccionar_rol_y_abrir_inicio(rol):
    guardar_rol(rol)
    mostrar_frame(frame_inicio)
    limpiar_campos_inicio()

# Desde pantalla inicio.py
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

    try:
        clave = cargar_clave()
        fernet = Fernet(clave)

        with open(cuentas_path, "rb") as archivo:
            for linea in archivo:
                partes = linea.strip().split(b"|")
                if len(partes) != 4:
                    continue

                rol_guardado, nombre_enc, usuario_guardado, contrasena_guardada = partes
                try:
                    usuario_descifrado = fernet.decrypt(usuario_guardado).decode()
                    contrasena_descifrada = fernet.decrypt(contrasena_guardada).decode()

                    if usuario == usuario_descifrado and contrasena == contrasena_descifrada:
                        Messagebox.show_info("Inicio de sesión exitoso.", "Acceso")
                        # Aquí decides qué abrir, en este caso mostramos mensaje y salimos
                        # o podrías ejecutar otro script, pero aquí solo demo
                        # Como no usar destroy, ocultamos todo y mostramos mensaje final
                        mostrar_frame(None)  # Oculta todo
                        Messagebox.show_info(f"Bienvenido {rol_guardado.decode()}. Aquí abrirías su interfaz.", "Acceso")
                        return
                except Exception as e:
                    print(f"Error al intentar descifrar una cuenta: {e}")
                    continue

        Messagebox.show_error("Credenciales incorrectas.", "Error")

    except Exception as e:
        Messagebox.show_error(f"Ocurrió un error durante el inicio de sesión: {e}", "Error")

def ir_a_registro():
    mostrar_frame(frame_registro)
    limpiar_campos_registro()

# Desde pantalla registro.py

def registrar():
    nombre = nombre_entry.get().strip()
    usuario = usuario_reg_entry.get().strip()
    contrasena = contrasena_reg_entry.get().strip()

    if not nombre or not usuario or not contrasena:
        Messagebox.show_error("Por favor, completa todos los campos.", "Error")
        return

    cuentas_path = os.path.join(base_path, "cuentas.txt")

    if os.path.exists(cuentas_path):
        clave = cargar_clave()
        fernet = Fernet(clave)
        with open(cuentas_path, "rb") as archivo:
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

    rol_actual = obtener_rol_actual()
    nombre_enc, usuario_enc, contrasena_enc = encriptar_datos(nombre, usuario, contrasena)

    with open(cuentas_path, "ab") as archivo:
        linea = rol_actual.encode() + b"|" + nombre_enc + b"|" + usuario_enc + b"|" + contrasena_enc + b"\n"
        archivo.write(linea)

    Messagebox.show_info("Cuenta creada exitosamente.", "Registro completado")
    mostrar_frame(frame_inicio)
    limpiar_campos_inicio()

def volver_a_inicio():
    mostrar_frame(frame_inicio)
    limpiar_campos_inicio()

# Limpieza de campos

def limpiar_campos_inicio():
    usuario_entry.delete(0, 'end')
    contrasena_entry.delete(0, 'end')

def limpiar_campos_registro():
    nombre_entry.delete(0, 'end')
    usuario_reg_entry.delete(0, 'end')
    contrasena_reg_entry.delete(0, 'end')

# -------------------------------------
# VENTANA PRINCIPAL
# -------------------------------------

base_path = os.path.dirname(__file__)

ventana = ttk.Window(themename="flatly")
ventana.title("CONTROL DE USUARIOS")
ventana.geometry("700x500")
ventana.resizable(False, False)

# --- FRAME PERSONAL (selección de rol) ---
##correccion del la interfaz desde aqui-----

frame_personal = ttk.Frame(ventana, padding=20)
frame_personal.pack(expand=True)

label_titulo = ttk.Label(frame_personal, text="¿CÓMO DESEAS INGRESAR?", font=("Courier", 22, "bold"))
label_titulo.pack(pady=(0, 40))

frame_roles = ttk.Frame(frame_personal)
frame_roles.pack()

# Cargar imágenes
ruta_trabajador = os.path.join(base_path, "trabajador.png")
ruta_usuario = os.path.join(base_path, "usuario.png")

img_trabajador = cargar_imagen(ruta_trabajador)
img_usuario = cargar_imagen(ruta_usuario)

# Trabajador
frame_trabajador = ttk.Frame(frame_roles)
frame_trabajador.pack(side=LEFT, padx=40)

if img_trabajador:
    label_img_trabajador = ttk.Label(frame_trabajador, image=img_trabajador)
    label_img_trabajador.pack(side=TOP, anchor="center")
else:
    print("Imagen trabajador.png no se cargó.")

btn_trabajador = ttk.Button(frame_trabajador, text="SOY TRABAJADOR",
                            bootstyle="success-outline", width=20,
                            command=lambda: seleccionar_rol_y_abrir_inicio("trabajador"))
btn_trabajador.pack(pady=10)

# Usuario
frame_usuario = ttk.Frame(frame_roles)
frame_usuario.pack(side=LEFT, padx=40)

if img_usuario:
    label_img_usuario = ttk.Label(frame_usuario, image=img_usuario)
    label_img_usuario.pack(side=TOP, anchor="center")
else:
    print("Imagen usuario.png no se cargó.")

btn_usuario = ttk.Button(frame_usuario, text="SOY USUARIO",
                        bootstyle="info-outline", width=20,
                        command=lambda: seleccionar_rol_y_abrir_inicio("usuario"))
btn_usuario.pack(pady=10)

ventana.img_trabajador = img_trabajador
ventana.img_usuario = img_usuario

#correccion denuevo desde aqui
# --- FRAME INICIO (LOGIN) ---
frame_inicio = ttk.Frame(ventana, padding=20)
frame_inicio.pack(expand=True)

login_frame = ttk.LabelFrame(
    frame_inicio,
    text="INICIO DE SESIÓN",
    bootstyle="primary",
    padding=(30, 20),
    width=500,
    height=320
)
login_frame.pack(expand=True)
login_frame.pack_propagate(False)  # Evita que el frame se reduzca a sus hijos

ttk.Label(login_frame, text="USUARIO:", font=("Courier", 13, "bold")).pack(anchor="w", pady=(0, 5))
usuario_entry = ttk.Entry(login_frame, width=50)
usuario_entry.pack(pady=(0, 15))

ttk.Label(login_frame, text="CONTRASEÑA:", font=("Courier", 13, "bold")).pack(anchor="w", pady=(0, 5))
contrasena_entry = ttk.Entry(login_frame, width=50, show="*")
contrasena_entry.pack(pady=(0, 20))

btn_login = ttk.Button(login_frame, text="INICIAR SESIÓN", width=40, bootstyle="success", command=iniciar_sesion)
btn_login.pack(pady=(0, 10))

btn_ir_registro = ttk.Button(login_frame, text="CREAR CUENTA", width=40, bootstyle="secondary", command=ir_a_registro)
btn_ir_registro.pack()

# --- FRAME REGISTRO ---
frame_registro = ttk.Frame(ventana, padding=20)
frame_registro.pack(expand=True)

registro_frame = ttk.LabelFrame(
    frame_registro,
    text="CREAR CUENTA NUEVA",
    bootstyle="primary",
    padding=(30, 20),
    width=500,
    height=400
)
registro_frame.pack(expand=True)
registro_frame.pack_propagate(False)

ttk.Label(registro_frame, text="NOMBRE:", font=("Courier", 13, "bold")).pack(anchor="w", pady=(0, 5))
nombre_entry = ttk.Entry(registro_frame, width=50)
nombre_entry.pack(pady=(0, 15))

ttk.Label(registro_frame, text="USUARIO:", font=("Courier", 13, "bold")).pack(anchor="w", pady=(0, 5))
usuario_reg_entry = ttk.Entry(registro_frame, width=50)
usuario_reg_entry.pack(pady=(0, 15))

ttk.Label(registro_frame, text="CONTRASEÑA:", font=("Courier", 13, "bold")).pack(anchor="w", pady=(0, 5))
contrasena_reg_entry = ttk.Entry(registro_frame, width=50, show="*")
contrasena_reg_entry.pack(pady=(0, 20))

btn_registrar = ttk.Button(registro_frame, text="REGISTRAR", width=40, bootstyle="success", command=registrar)
btn_registrar.pack(pady=(0, 10))

btn_volver = ttk.Button(registro_frame, text="VOLVER AL INICIO", width=40, bootstyle="secondary", command=volver_a_inicio)
btn_volver.pack()

#hasta aqui
# --- INICIO ---
mostrar_frame(frame_personal)

ventana.mainloop()
