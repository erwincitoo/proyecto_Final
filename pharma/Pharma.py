import os
import sys
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
import subprocess

# Ventana Principal
ventana = ttk.Window(themename="cyborg")
ventana.title("PHARMA")
ventana.geometry("800x600")
ventana.resizable(False, False)

ruta_imagen = os.path.join(os.path.dirname(__file__), "pharmaa.jpg")

if not os.path.isfile(ruta_imagen):
    print(f"ERROR: No existe el archivo '{ruta_imagen}'")
    sys.exit(1)

# Cargar Imagen
imagen_original = Image.open(ruta_imagen)
imagen_redimensionada = imagen_original.resize((800, 600))
imagen = ImageTk.PhotoImage(imagen_redimensionada)

label_imagen = ttk.Label(ventana, image=imagen)
label_imagen.place(x=0, y=0, relwidth=1, relheight=1)


def abrir_personal():
    ventana.destroy()
    ruta_personal = os.path.join(os.path.dirname(__file__), "personal.py")
    subprocess.run([sys.executable, ruta_personal], shell=True)

ventana.after(10000, abrir_personal)
ventana.mainloop()
