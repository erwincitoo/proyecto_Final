import os
import sys
import subprocess
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from cryptography.fernet import Fernet

# ENCRIPTAR DATOS

def generar_clave():
    clave = Fernet.generate_key()
    with open("clave.key", "wb") as archivo_clave:
        archivo_clave.write(clave)

def cargar_clave():
    if not os.path.exists("clave.key"):
        generar_clave()
    with open("clave.key", "rb") as archivo_clave:
        return archivo_clave.read()

def encriptar_datos(usuario, contrasena):
    clave = cargar_clave()
    fernet = Fernet(clave)
    usuario_encriptado = fernet.encrypt(usuario.encode())
    contrasena_encriptada = fernet.encrypt(contrasena.encode())
    return usuario_encriptado, contrasena_encriptada

def desencriptar(texto_encriptado):
    clave = cargar_clave()
    fernet = Fernet(clave)
    return fernet.decrypt(texto_encriptado).decode()

#LOGIN 

def iniciar_sesion():
    usuario = usuario_entry.get().strip()
    contrasena = contrasena_entry.get().strip()

    if not usuario or not contrasena:
        Messagebox.show_error("Por favor, completa todos los campos.", "Error")
        return

    if not os.path.exists("cuentas.txt"):
        Messagebox.show_error("No hay cuentas registradas aún.", "Error")
        return

    try:
        clave = cargar_clave()
        fernet = Fernet(clave)

        with open("cuentas.txt", "rb") as archivo:
            for linea in archivo:
                partes = linea.strip().split(b"|")
                if len(partes) != 4:
                    continue

                rol, nombre_enc, usuario_guardado, contrasena_guardada = partes
                try:
                    usuario_descifrado = fernet.decrypt(usuario_guardado).decode()
                    contrasena_descifrada = fernet.decrypt(contrasena_guardada).decode()

                    if usuario == usuario_descifrado and contrasena == contrasena_descifrada:
                        Messagebox.show_info("Inicio de sesión exitoso.", "Acceso")
                        ventana.destroy()

                        if rol.decode() == "usuario":
                            ruta = os.path.join(os.path.dirname(__file__), "mostrarcarro.py")
                        else:
                            ruta = os.path.join(os.path.dirname(__file__), "tree.py") 

                        subprocess.run([sys.executable, ruta], shell=True)
                        return
                except Exception as e:
                   
                    print(f"Error al intentar descifrar una cuenta: {e}")
                    continue

        Messagebox.show_error("Credenciales incorrectas.", "Error")

    except Exception as e:
        Messagebox.show_error(f"Ocurrió un error durante el inicio de sesión: {e}", "Error")

# IR A REGISTRO 

def ir_a_registro():
    ventana.destroy()
    ruta = os.path.join(os.path.dirname(__file__), "registro.py")
    subprocess.run([sys.executable, ruta], shell=True)

# VENTANA

ventana = ttk.Window(themename="flatly")
ventana.title("PANTALLA - INICIO")
ventana.geometry("700x500")
ventana.resizable(0, 0)

frame = ttk.Frame(ventana)
frame.pack()

login_frame = ttk.LabelFrame(frame, text="INICIO DE SESIÓN", bootstyle="primary", padding=20)
login_frame.grid(row=0, column=0, padx=20, pady=20)

ttk.Label(login_frame, text="USUARIO:", font=("Courier", 12, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 5))
usuario_entry = ttk.Entry(login_frame, width=40)
usuario_entry.grid(row=1, column=0, pady=(0, 10))

ttk.Label(login_frame, text="CONTRASEÑA:", font=("Courier", 12, "bold")).grid(row=2, column=0, sticky="w", pady=(10, 5))
contrasena_entry = ttk.Entry(login_frame, width=40, show="*")
contrasena_entry.grid(row=3, column=0, pady=(0, 20))

ttk.Button(login_frame, text="INICIAR SESIÓN", width=31, bootstyle="success", command=iniciar_sesion).grid(row=4, column=0, pady=10)
ttk.Button(login_frame, text="CREAR CUENTA", width=31, bootstyle="secondary", command=ir_a_registro).grid(row=5, column=0)

ventana.mainloop()