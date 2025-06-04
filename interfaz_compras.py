import tkinter as tk
from tkinter import ttk

def crear_interfaz():
    global ventana_principal, tabla_productos
    
    # Creación de la ventana principal
    ventana_principal = tk.Tk()
    ventana_principal.title("PHARMA - INTERFAZ DE COMPRAS PARA USUARIOS")
    ventana_principal.geometry("1280x720+0+0")
    ventana_principal.resizable(0, 0)
    
    # Frame principal
    frame_principal = tk.Frame(ventana_principal)
    frame_principal.pack(padx=10, pady=10, fill="both", expand=True)
    
    frame_principal.grid_rowconfigure(0, weight=1)
    frame_principal.grid_rowconfigure(2, weight=1)
    frame_principal.grid_columnconfigure(0, weight=1)
    
    frame_productos = tk.LabelFrame(frame_principal, text="PRODUCTOS DISPONIBLES", font=("Verdana", 12, "bold"))
    frame_productos.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
    
    
    # Creación de la tabla de productos
    columnas = ("CÓDIGO", "NOMBRE", "PRECIO", "CANTIDAD")
    tabla_productos = ttk.Treeview(frame_productos, columns=columnas, show="headings", height=10)
    
    # Configuración de las columnas de la tabla
    tabla_productos.heading("CÓDIGO", text="CÓDIGO")
    tabla_productos.heading("NOMBRE", text="NOMBRE")
    tabla_productos.heading("PRECIO", text="PRECIO (Bs.)")
    tabla_productos.heading("CANTIDAD", text="CANTIDAD")
    
    tabla_productos.column("CÓDIGO", width=100, anchor="center")
    tabla_productos.column("NOMBRE", width=200, anchor="center")
    tabla_productos.column("PRECIO", width=100, anchor="center")
    tabla_productos.column("CANTIDAD", width=100, anchor="center")
    
    # Configurar colores para los productos agotados
    tabla_productos.tag_configure("AGOTADO", background="#ffdddd", foreground="red")
    
    tabla_productos.pack(padx=5, pady=5, fill="both", expand=True)

# Función Principal:
def main():
    
    crear_interfaz()
    ventana_principal.mainloop()

if __name__ == "__main__":
    main()