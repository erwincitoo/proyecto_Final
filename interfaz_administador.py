from tkinter import ttk, messagebox, filedialog
import tkinter
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import os
import shutil
from PIL import ImageTk, Image
import pandas as pd
import traceback

ventana = ttk.Window(themename="yeti")
ventana.title("BASE DE DATOS - FARMACIA")
ventana.geometry("1500x900+0+0")  
ventana.resizable(0,0)

frame = tkinter.Frame(ventana)
frame.pack()

frame.grid_rowconfigure(0, weight=1)  
frame.grid_rowconfigure(1, weight=0)  
frame.grid_columnconfigure(1, weight=1)

# Variable global para almacenar todos los datos originales
datos_originales = []

# Funciones

# Función para mostrar imagen al seleccionar un producto
def mostrar_imagen_producto(event):
    selected_item = tabla_tree.selection()
    
    if not selected_item:
        return
    
    valores = tabla_tree.item(selected_item)["values"]
    codigo_producto = valores[0]  
    
    # Buscar la imagen en el directorio
    directorio_imagenes = "imagenes"
    if not os.path.exists(directorio_imagenes):
        os.makedirs(directorio_imagenes)
    
    # Buscar cualquier archivo con el nombre del código del producto
    imagen_encontrada = False
    for extension in ['.png', '.jpg', '.jpeg', '.gif']:
        ruta_imagen = os.path.join(directorio_imagenes, f"{codigo_producto}{extension}")
        if os.path.exists(ruta_imagen):
            try:
                # Cargar y mostrar la imagen
                imagen = Image.open(ruta_imagen)
                imagen = imagen.resize((200, 200))
                imagen_tk = ImageTk.PhotoImage(imagen)
                
                # Mostrar la imagen en el label
                label_imagen.config(image=imagen_tk)
                label_imagen.image = imagen_tk 
                imagen_encontrada = True
                break
            except Exception as e:
                print(f"ERROR AL CARGAR LA IMAGEN {ruta_imagen}: {e}")
    
    if not imagen_encontrada:
        label_imagen.config(image="", text="IMAGEN\nNO DISPONIBLE")

# Función para buscar productos por código o nombre
def buscar_producto(event=None):
    termino_busqueda = busqueda_entry.get().lower().strip()
    
    for item in tabla_tree.get_children():
        tabla_tree.delete(item)
    
    # Si no hay término de búsqueda, mostrar todos los datos
    if not termino_busqueda:
        for datos in datos_originales:
            tabla_tree.insert("", "end", values=datos)
        return
    
    # Filtrar datos que coincidan con el valor de búsqueda
    resultados_encontrados = False
    for datos in datos_originales:
        codigo = str(datos[0]).lower()
        nombre = str(datos[1]).lower()
        
        # Buscar a través de un código o nombre
        if termino_busqueda in codigo or termino_busqueda in nombre:
            tabla_tree.insert("", "end", values=datos)
            resultados_encontrados = True
    
    # Si no se encontraron resultados, mostrar el mensaje
    if not resultados_encontrados and termino_busqueda:
        tabla_tree.insert("", "end", values=("", "NO RESULTADOS", "", "", "", "", ""))

# Función Actualizar el documento Excel
def actualizar_excel():
    try:
        # Usar datos_originales en lugar de los datos de la tabla (que pueden estar filtrados)
        columnas = ["CÓDIGO", "NOMBRE", "TIPO", "CATEGORÍA", "LOTE", "CANTIDAD", "PRECIO"]
        df = pd.DataFrame(datos_originales, columns=columnas)
        
        print(f"ACTUALIZANDO EXCEL CON {len(datos_originales)} REGISTROS")
        
        # Guardar Excel
        df.to_excel("datos_farmacia.xlsx", index=False)
        print("EXCEL ACTUALIZADO CORRECTAMENTE")
        
    except Exception as e:
      
        print(traceback.format_exc()) 
        messagebox.showerror("ERROR", f"NO SE PUDO ACTUALIZAR EL ARCHIVO EXCEL: {str(e)}")

# Función para cargar los datos de Excel
def cargar_datos_excel():
    global datos_originales
    if os.path.exists("datos_farmacia.xlsx"):
        df = pd.read_excel("datos_farmacia.xlsx")
        datos_originales = []
        for _, fila in df.iterrows():
            valores = tuple(fila)
            tabla_tree.insert("", "end", values=valores)
            datos_originales.append(valores)
    else:
        messagebox.showwarning("ADVERTENCIA", "ARCHIVO 'datos_farmacia.xlsx' NO ENCONTRADO.")


# Función para actualizar los datos en la base de datos:
def actualizar_datos(selected_item, valores_originales):
    codigo = codigo_entry.get()
    nombre = nombre_entry.get()
    tipo = tipo_entry.get()
    categoria = categoria_combobox.get()
    lote = lote_entry.get()
    cantidad = cantidad_entry.get()
    precio = precio_entry.get()

    if codigo and nombre and tipo and categoria and lote and cantidad and precio:
        nuevos_valores = (codigo, nombre, tipo, categoria, lote, cantidad, precio)
        tabla_tree.item(selected_item, values=nuevos_valores)
        
        for i, datos in enumerate(datos_originales):
            if datos == valores_originales:
                datos_originales[i] = nuevos_valores
                break
        
        limpiar_campos()
        guardar_button.config(text="GUARDAR")
        
        actualizar_excel()
        
    else:
        messagebox.showwarning("ADVERTENCIA", "POR FAVOR, COMPLETE TODOS LOS CAMPOS.")

# Función que vacía los datos de los campos de ingreso de datos:
def limpiar_campos():
    codigo_entry.delete(0, tkinter.END)
    nombre_entry.delete(0, tkinter.END)
    tipo_entry.delete(0, tkinter.END)
    categoria_combobox.set("")
    lote_entry.delete(0, tkinter.END)
    cantidad_entry.delete(0, tkinter.END)
    precio_entry.delete(0, tkinter.END)

# Función para mostrar las imagenes de los productos
def cargar_imagen():
    selected_item = tabla_tree.selection()
    
    if not selected_item:
        messagebox.showwarning("ADVERTENCIA", "SELECCIONE UN PRODUCTO PRIMERO.")
        return
    
    valores = tabla_tree.item(selected_item)["values"]
    
    if valores[1] == "NO SE ENCONTRARON RESULTADOS":
        messagebox.showwarning("ADVERTENCIA", "SELECCIONE UN PRODUCTO VÁLIDO.")
        return
    
    codigo_producto = valores[0]  
    
    # Pedir al usuario seleccionar una imagen
    ruta_imagen = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.gif")])
    
    if ruta_imagen:
        directorio_imagenes = "imagenes"
        if not os.path.exists(directorio_imagenes):
            os.makedirs(directorio_imagenes)
        _, extension = os.path.splitext(ruta_imagen)
        
        # Crear nombre de archivo basado en el código del producto
        nombre_archivo = os.path.join(directorio_imagenes, f"{codigo_producto}{extension}")
        
        # Copiar la imagen al directorio de imágenes con el nombre del código
        shutil.copy2(ruta_imagen, nombre_archivo)
        
        # Cargar y mostrar la imagen
        imagen = Image.open(nombre_archivo)
        imagen = imagen.resize((200, 200))
        imagen_tk = ImageTk.PhotoImage(imagen)
        
        # Mostrar la imagen en el label
        label_imagen.config(image=imagen_tk, text="")
        label_imagen.image = imagen_tk  
        
        messagebox.showinfo("ÉXITO", f"IMAGEN ASOCIADA AL PRODUCTO {codigo_producto}")

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
label_imagen = tkinter.Label(container_imagen, bg="light gray", text="IMÁGEN NO\nDISPONIBLE")
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

# Frame de Búsqueda:

busqueda_Frame = tkinter.LabelFrame(frame, font=("Verdana", 12, "bold"), text="BÚSQUEDA DE PRODUCTOS")
busqueda_Frame.grid(row=2, column=1, padx=5, pady=(0, 20), sticky="ew")

busqueda_Frame.grid_columnconfigure(1, weight=1)

busqueda_label = tkinter.Label(busqueda_Frame, font=("Roboto", 10, "bold"), text="CÓDIGO O NOMBRE DEL PRODUCTO:")
busqueda_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

busqueda_entry = tkinter.Entry(busqueda_Frame, font=("Roboto", 10), width=40)
busqueda_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
busqueda_entry.bind('<KeyRelease>', buscar_producto)  # Búsqueda en tiempo real

ventana.mainloop()