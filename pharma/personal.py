import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
import os
import subprocess
import sys

# FUNCIONES 

def guardar_rol(rol):
    with open("rol_actual.txt", "w") as f:
        f.write(rol)

def abrir_inicio_como(rol):
    guardar_rol(rol)
    ventana.destroy()
    ruta = os.path.join(os.path.dirname(__file__), "inicio.py")
    subprocess.run([sys.executable, ruta])

# CARGAR IMAGEN 

def cargar_imagen(ruta, tamaño=(200, 200)):
    try:
        img_pil = Image.open(ruta)
        img_pil = img_pil.resize(tamaño, Image.LANCZOS)
        return ImageTk.PhotoImage(img_pil)
    except FileNotFoundError:
        print(f"Error: Imagen no encontrada en {ruta}")
        return None

# INTERFAZ 

ventana = ttk.Window(themename="flatly")  # colores dark,superhero,etc.....
ventana.title("SELECCIONA TU ROL")
ventana.geometry("900x600")
ventana.resizable(False, False)

frame = ttk.Frame(ventana, padding=20)
frame.pack(fill=BOTH, expand=YES)

label_titulo = ttk.Label(frame, text="¿CÓMO DESEAS INGRESAR?", font=("Courier", 22, "bold"))
label_titulo.pack(pady=(0, 40))

#Botones 
frame_roles = ttk.Frame(frame)
frame_roles.pack()

ruta_trabajador = os.path.join(os.path.dirname(__file__), "trabajador.png")
ruta_usuario = os.path.join(os.path.dirname(__file__), "usuario.png")

img_trabajador = cargar_imagen(ruta_trabajador)
img_usuario = cargar_imagen(ruta_usuario)

frame_trabajador = ttk.Frame(frame_roles)
frame_trabajador.pack(side=LEFT, padx=80)

if img_trabajador:
    label_img_trabajador = ttk.Label(frame_trabajador, image=img_trabajador)
    label_img_trabajador.pack()
else:
    print("Imagen trabajador.png no se cargó.")

btn_trabajador = ttk.Button(frame_trabajador, text="SOY TRABAJADOR",
                            bootstyle="success-outline",
                            width=20,
                            command=lambda: abrir_inicio_como("trabajador"))
btn_trabajador.pack(pady=10)

# Usuario
frame_usuario = ttk.Frame(frame_roles)
frame_usuario.pack(side=LEFT, padx=80)

if img_usuario:
    label_img_usuario = ttk.Label(frame_usuario, image=img_usuario)
    label_img_usuario.pack()
else:
    print("Imagen usuario.png no se cargó.")

btn_usuario = ttk.Button(frame_usuario, text="SOY USUARIO",
                        bootstyle="info-outline",
                        width=20,
                        command=lambda: abrir_inicio_como("usuario"))
btn_usuario.pack(pady=10)

ventana.img_trabajador = img_trabajador
ventana.img_usuario = img_usuario

ventana.mainloop()
