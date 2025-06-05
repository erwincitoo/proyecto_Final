import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import os
from cryptography.fernet import Fernet

#ENCRIPTAR

def cargar_clave():
    if not os.path.exists("clave.key"):
        ttk.Messagebox.show_error("No se encontró la clave de encriptación.", "Error")
        return None
    with open("clave.key", "rb") as archivo_clave:
        return archivo_clave.read()

def desencriptar_dato(dato_encriptado, fernet):
    try:
        return fernet.decrypt(dato_encriptado).decode()
    except Exception:
        return "[Error al desencriptar]"

# VER cuentas creadas de cuentas.txt

def ver_cuentas():
    clave = cargar_clave()
    if not clave:
        return

    fernet = Fernet(clave)

    if not os.path.exists("cuentas.txt"):
        ttk.Messagebox.show_info("No hay cuentas registradas todavía.", "Información")
        return

    with open("cuentas.txt", "rb") as archivo:
        for linea in archivo:
            partes = linea.strip().split(b"|")
            if len(partes) != 4:
                continue
            rol, nombre_enc, usuario_enc, _ = partes
            nombre = desencriptar_dato(nombre_enc, fernet)
            usuario = desencriptar_dato(usuario_enc, fernet)
            rol_decodificado = rol.decode()
            tree.insert("", "end", values=(rol_decodificado.upper(), nombre, usuario))

# La ventana de los registros

ventana = ttk.Window(title="CUENTAS REGISTRADAS", themename="flatly")
ventana.geometry("650x400")
ventana.resizable(0, 0)

ttk.Label(ventana, text="CUENTAS REGISTRADAS", font=("Courier", 16, "bold")).pack(pady=10)

columns = ("Rol", "Nombre", "Usuario")
tree = ttk.Treeview(ventana, columns=columns, show="headings", bootstyle="info")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=200)
tree.pack(padx=20, pady=10, fill="both", expand=True)

ttk.Button(ventana, text="VOLVER", bootstyle="danger", width=25, command=ventana.destroy).pack(pady=10)

ver_cuentas()
ventana.mainloop()
