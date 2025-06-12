from tkinter import messagebox
import tkinter
import variables_globales2 as vg2
from funciones import actualizar_excel, buscar_producto

# Función para guardar los datos ingresados por teclado
def guardar_datos():
    codigo = vg2.codigo_entry.get()
    nombre = vg2.nombre_entry.get()
    tipo = vg2.tipo_entry.get()
    categoria = vg2.categoria_combobox.get()
    lote = vg2.lote_entry.get()
    cantidad = vg2.cantidad_entry.get()
    precio = vg2.precio_entry.get()
    
    if codigo and nombre and tipo and categoria and lote and cantidad and precio:
        nuevos_valores = (str(codigo), str(nombre), str(tipo), str(categoria), str(lote), str(cantidad), str(precio))
        vg2.tabla_tree.insert("", "end", values=nuevos_valores)
        
        actualizar_datos_originales()
        actualizar_excel()

        
        vg2.codigo_entry.delete(0, tkinter.END)
        vg2.nombre_entry.delete(0, tkinter.END)
        vg2.tipo_entry.delete(0, tkinter.END)
        vg2.categoria_combobox.set("")
        vg2.lote_entry.delete(0, tkinter.END)
        vg2.cantidad_entry.delete(0, tkinter.END)
        vg2.precio_entry.delete(0, tkinter.END)
        
        actualizar_excel()
        
        if vg2.busqueda_entry.get().strip():
            buscar_producto()
    else:
        messagebox.showwarning("ADVERTENCIA", "TODOS LOS CAMPOS DEBEN SER LLENADOS.")

# Función que vacía los datos de los campos de ingreso de datos:
def limpiar_campos():
    vg2.codigo_entry.delete(0, tkinter.END)
    vg2.nombre_entry.delete(0, tkinter.END)
    vg2.tipo_entry.delete(0, tkinter.END)
    vg2.categoria_combobox.set("")
    vg2.lote_entry.delete(0, tkinter.END)
    vg2.cantidad_entry.delete(0, tkinter.END)
    vg2.precio_entry.delete(0, tkinter.END)

# Función para eliminar los datos de alguna fila:
def eliminar_datos():
    selected_item = vg2.tabla_tree.selection()
    if not selected_item:
        messagebox.showwarning("ADVERTENCIA", "SELECCIONA UNA FILA PARA ELIMINAR.")
        return
    
    valores_seleccionados = vg2.tabla_tree.item(selected_item)["values"]
    
    if valores_seleccionados[1] == "NO SE ENCONTRARON RESULTADOS":
        messagebox.showwarning("ADVERTENCIA", "NO SE PUEDE ELIMINAR ESTA FILA")
        return
    
    vg2.datos_originales[:] = [datos for datos in vg2.datos_originales if datos != valores_seleccionados]
    
    vg2.tabla_tree.delete(selected_item)
    
    actualizar_datos_originales()
    actualizar_excel()
    
    if vg2.busqueda_entry.get().strip():
        buscar_producto()

# Función para modificar los datos de algún producto desde la interfaz
def editar_datos():
    item_seleccionado = vg2.tabla_tree.selection()
    
    if not item_seleccionado:
        messagebox.showwarning("ADVERTENCIA", "SELECCIONE UNA FILA PARA EDITAR.")
        return
    
    valores_seleccionados = vg2.tabla_tree.item(item_seleccionado)["values"]
    
    if valores_seleccionados[1] == "NO SE ENCONTRARON RESULTADOS":
        messagebox.showwarning("ADVERTENCIA", "NO SE PUEDE EDITAR ESTA FILA.")
        return
    
    vg2.codigo_entry.delete(0, tkinter.END)
    vg2.codigo_entry.insert(0, valores_seleccionados[0])
    
    vg2.nombre_entry.delete(0, tkinter.END)
    vg2.nombre_entry.insert(0, valores_seleccionados[1])
    
    vg2.tipo_entry.delete(0, tkinter.END)
    vg2.tipo_entry.insert(0, valores_seleccionados[2])
    
    vg2.categoria_combobox.set(valores_seleccionados[3])
    
    vg2.lote_entry.delete(0, tkinter.END)
    vg2.lote_entry.insert(0, valores_seleccionados[4])
    
    vg2.cantidad_entry.delete(0, tkinter.END)
    vg2.cantidad_entry.insert(0, valores_seleccionados[5])
    
    vg2.precio_entry.delete(0, tkinter.END)
    vg2.precio_entry.insert(0, valores_seleccionados[6])

    vg2.guardar_button.config(text="ACTUALIZAR", command=lambda: actualizar_datos(item_seleccionado, valores_seleccionados))

# Función para limpiar la búsqueda y mostrar los productos
def limpiar_busqueda():
    vg2.busqueda_entry.delete(0, tkinter.END)
    buscar_producto()

# Función para actualizar los datos en la base de datos:
def actualizar_datos(selected_item, valores_originales):
    codigo = vg2.codigo_entry.get()
    nombre = vg2.nombre_entry.get()
    tipo = vg2.tipo_entry.get()
    categoria = vg2.categoria_combobox.get()
    lote = vg2.lote_entry.get()
    cantidad = vg2.cantidad_entry.get()
    precio = vg2.precio_entry.get()

    if codigo and nombre and tipo and categoria and lote and cantidad and precio:
        nuevos_valores = (codigo, nombre, tipo, categoria, lote, cantidad, precio)
        vg2.tabla_tree.item(selected_item, values=nuevos_valores)
        actualizar_datos_originales()
        
        limpiar_campos()
        vg2.guardar_button.config(text="GUARDAR", command=guardar_datos)
        
        actualizar_excel()

        if vg2.busqueda_entry.get().strip():
            buscar_producto()
        
    else:
        messagebox.showwarning("ADVERTENCIA", "POR FAVOR, COMPLETE TODOS LOS CAMPOS.")

# Función para actualizar los datos originales
def actualizar_datos_originales():
    vg2.datos_originales = []
    for item in vg2.tabla_tree.get_children():
        valores = vg2.tabla_tree.item(item)["values"]
        if valores[1] != "NO SE ENCONTRARON RESULTADOS":
            vg2.datos_originales.append(valores)