from tkinter import ttk, messagebox, filedialog
import tkinter
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

ventana = ttk.Window(themename="yeti")
ventana.title("BASE DE DATOS - FARMACIA")
ventana.geometry("1500x900+0+0")  
ventana.resizable(0,0)

frame = tkinter.Frame(ventana)
frame.pack()

frame.grid_rowconfigure(0, weight=1)  
frame.grid_rowconfigure(1, weight=0)  
frame.grid_columnconfigure(1, weight=1)


# Inicio Frame:

inicio_Frame = tkinter.LabelFrame(frame, font=("Verdana", 16, "bold"), text="BASE DE DATOS")
inicio_Frame.grid(row=0, column=0, padx=20, pady=10)

inicio_Frame.grid_rowconfigure(0, minsize=20)

codigo_label = tkinter.Label(inicio_Frame, font=("Roboto", 11, "bold"), text="CÓDIGO:", width=12)
codigo_label.grid(row=1, column=0, pady=7)

codigo_entry = tkinter.Entry(inicio_Frame, width=22)
codigo_entry.grid(row=1, column=1, padx=2)

nombre_label = tkinter.Label(inicio_Frame, font=("Roboto", 11, "bold"), text="NOMBRE:", width=12)
nombre_label.grid(row=2, column=0, pady=7)

nombre_entry = tkinter.Entry(inicio_Frame, width=22)
nombre_entry.grid(row=2, column=1, padx=2)

tipo_label = tkinter.Label(inicio_Frame, font=("Roboto", 11, "bold"), text="TIPO:", width=12)
tipo_label.grid(row=3, column=0, pady=7)

tipo_entry = tkinter.Entry(inicio_Frame, width=22)
tipo_entry.grid(row=3, column=1, padx=2)

categoria_label = tkinter.Label(inicio_Frame, font=("Roboto", 11, "bold"), text="CATEGORÍA:", width=12)
categoria_label.grid(row=4, column=0, pady=7)

categoria_combobox = ttk.Combobox(inicio_Frame, values=["ANTIBIÓTICO", "ANTIVIRAL"], state="readonly", width=21)
categoria_combobox.grid(row=4, column=1, padx=2)

lote_label = tkinter.Label(inicio_Frame, font=("Roboto", 11, "bold"), text="LOTE:", width=12)
lote_label.grid(row=5, column=0, pady=7)

lote_entry = tkinter.Entry(inicio_Frame, width=22)
lote_entry.grid(row=5, column=1, padx=2)

cantidad_label = tkinter.Label(inicio_Frame, font=("Roboto", 11, "bold"), text="CANTIDAD:", width=12)
cantidad_label.grid(row=6, column=0, pady=7)

cantidad_entry = tkinter.Entry(inicio_Frame, width=22)
cantidad_entry.grid(row=6, column=1, padx=2)

precio_label = ttk.Label(inicio_Frame, font=("Roboto", 11, "bold"), text="P/ UNITARIO:", width=12)
precio_label.grid(row=7, column=0, pady=7)

precio_entry = tkinter.Entry(inicio_Frame, width=22)
precio_entry.grid(row=7, column=1, padx=2)

# Frame Botones:

botones_Frame = tkinter.LabelFrame(frame, font=("Verdana", 16, "bold"), text="BOTONES")
botones_Frame.grid(row=1, column=0, padx=20, pady=10)

botones_Frame.grid_rowconfigure(0, minsize=20)

guardar_button = tkinter.Button(botones_Frame, font=("Roboto", 11, "bold"), text="GUARDAR", width=12)
guardar_button.grid(row=1, column=0, padx=7, pady=7)

editar_button = tkinter.Button(botones_Frame, font=("Roboto", 11, "bold"), text="EDITAR", width=12)
editar_button.grid(row=1, column=1, padx=7, pady=7)

eliminar_button = tkinter.Button(botones_Frame, font=("Roboto", 11, "bold"), text="ELIMINAR", width=12)
eliminar_button.grid(row=2, column=0, padx=7, pady=7)

imagen_button = tkinter.Button(botones_Frame, font=("Roboto", 11, "bold"), text="AGREGAR IMAGEN", width=16)
imagen_button.grid(row=2, column=1, padx=7, pady=7)

# Frame Imagen:

imagen_Frame = tkinter.LabelFrame(frame, font=("Verdana", 16, "bold"), text="IMÁGEN")
imagen_Frame.grid(row=2, column=0, padx=20, pady=10)

imagen_Frame.grid_rowconfigure(0, minsize=20)

# Crear un contenedor para la imagen con fondo gris claro
container_imagen = tkinter.Frame(imagen_Frame, width=200, height=200, bg="light gray")
container_imagen.grid(row=1, column=0, padx=10, pady=10)
container_imagen.pack_propagate(False)  # Mantener tamaño fijo

# Label para mostrar la imagen dentro del contenedor
label_imagen = tkinter.Label(container_imagen, bg="light gray", text="IMAGEN NO\nDISPONIBLE")
label_imagen.pack(expand=True, fill="both")


# Frame Tree:

tabla_Frame = tkinter.LabelFrame(frame, font=("Verdana", 16, "bold"), text="TABLA DE INVENTARIADO")
tabla_Frame.grid(row=0, column=1, padx=5, pady=20, rowspan=2, sticky="nsew")

tabla_Frame.grid_rowconfigure(0, weight=1)  
tabla_Frame.grid_columnconfigure(0, weight=1) 

scrollbar_y = ttk.Scrollbar(tabla_Frame, orient="vertical")
scrollbar_x = ttk.Scrollbar(tabla_Frame, orient="horizontal")

tabla_Frame.grid_rowconfigure(0, minsize=20)

tabla_tree = ttk.Treeview(tabla_Frame, columns=("CODIGO", "NOMBRE", "TIPO",
                                                "CATEGORIA", "LOTE", "CANTIDAD", "P/ UNITARIO"), 
                          show="headings", yscrollcommand=scrollbar_y.set,
                          xscrollcommand=scrollbar_x.set, bootstyle="primary")
tabla_tree.heading("CODIGO", text="CÓDIGO")
tabla_tree.heading("NOMBRE", text="NOMBRE")
tabla_tree.heading("TIPO", text="TIPO")
tabla_tree.heading("CATEGORIA", text="CATEGORÍA")
tabla_tree.heading("LOTE", text="LOTE")
tabla_tree.heading("CANTIDAD", text="CANTIDAD")
tabla_tree.heading("P/ UNITARIO", text="P/ UNITARIO")
tabla_tree.grid(row=0, column=0, sticky="nsew")

tabla_tree.column("CODIGO", width=180, anchor="center")
tabla_tree.column("NOMBRE", width=180, anchor="center")
tabla_tree.column("TIPO", width=180, anchor="center")
tabla_tree.column("CATEGORIA", width=180, anchor="center")
tabla_tree.column("LOTE", width=180, anchor="center")
tabla_tree.column("CANTIDAD", width=180, anchor="center")
tabla_tree.column("P/ UNITARIO", width=180, anchor="center")

scrollbar_y.config(command=tabla_tree.yview)
scrollbar_x.config(command=tabla_tree.xview)
scrollbar_y.grid(row=0, column=1, sticky="ns")
scrollbar_x.grid(row=1, column=0, sticky="ew")

ventana.mainloop()