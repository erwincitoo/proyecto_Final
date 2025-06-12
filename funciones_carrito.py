import tkinter as tk
from tkinter import messagebox
import variables_globales as vg

# Función agregar productos al carrito
def agregar_producto_al_carrito():
    # Verificar que haya un producto seleccionado
    seleccion = vg.tabla_productos.selection()
    if len(seleccion) == 0:
        messagebox.showwarning("ADVERTENCIA", "POR FAVOR SELECCIONA UN PRODUCTO")
        return
    
    # Obtener la cantidad ingresada
    texto_cantidad = vg.entrada_cantidad.get()
    
    # Verificar que la cantidad sea válida
    if texto_cantidad.isdigit() == False:
        messagebox.showwarning("ADVERTENCIA", "INGRESA UNA CANTIDAD VALIDA (SOLO NÚMEROS POSITIVOS)")
        return
    
    cantidad_deseada = int(texto_cantidad)
    if cantidad_deseada <= 0:
        messagebox.showwarning("ADVERTENCIA", "LA CANTIDAD DEBE SER MAYOR A 0")
        return
    
    # Obtener los datos del producto seleccionado
    datos_producto = vg.tabla_productos.item(seleccion)["values"]
    codigo_producto = datos_producto[0]
    nombre_producto = datos_producto[1]
    precio_producto = datos_producto[2]
    stock_disponible = datos_producto[3]
    
    # Verificar que hay suficiente stock
    if cantidad_deseada > stock_disponible:
        mensaje = "Solo hay " + str(stock_disponible) + " unidades disponibles"
        messagebox.showerror("STOCK INSUFICIENTE", mensaje)
        return
    
    producto_encontrado = False
    contador = 0
    while contador < len(vg.lista_carrito):
        item_carrito = vg.lista_carrito[contador]
        if item_carrito["codigo"] == codigo_producto:
            item_carrito["cantidad"] = item_carrito["cantidad"] + cantidad_deseada
            item_carrito["subtotal"] = item_carrito["cantidad"] * float(precio_producto)
            producto_encontrado = True
            break
        contador = contador + 1
    
    if producto_encontrado == False:
        nuevo_item = {}
        nuevo_item["codigo"] = codigo_producto
        nuevo_item["nombre"] = nombre_producto
        nuevo_item["precio"] = precio_producto
        nuevo_item["cantidad"] = cantidad_deseada
        nuevo_item["subtotal"] = float(precio_producto) * cantidad_deseada
        vg.lista_carrito.append(nuevo_item)
    
    # Reducir el stock del producto
    contador = 0
    while contador < len(vg.lista_productos):
        producto = vg.lista_productos[contador]
        if producto["codigo"] == codigo_producto:
            producto["cantidad"] = producto["cantidad"] - cantidad_deseada
            break
        contador = contador + 1
    
    mostrar_productos_en_carrito()
    mostrar_todos_los_productos()
    calcular_total_carrito()
    
    vg.entrada_cantidad.delete(0, tk.END)

# Funcion para quitar el producto del carrito
def quitar_producto_del_carrito():
    seleccion = vg.tabla_carrito.selection()
    if len(seleccion) == 0:
        messagebox.showwarning("ADVERTENCIA", "SELECCIONE UN PRODUCTO DEL CARRITO PARA QUITAR")
        return
    
    # Obtener datos del producto a quitar
    datos_item = vg.tabla_carrito.item(seleccion)["values"]
    codigo_producto = datos_item[0]
    nombre_producto = datos_item[1]
    cantidad_en_carrito = datos_item[3]
    
    pregunta = "¿DESEA QUITAR " + nombre_producto + " DEL CARRITO?"
    respuesta = messagebox.askyesno("CONFIRMAR", pregunta)
    if respuesta == False:
        return
    
    # Buscar y quitar el producto del carrito
    contador = 0
    while contador < len(vg.lista_carrito):
        item = vg.lista_carrito[contador]
        if item["codigo"] == codigo_producto:
            contador_productos = 0
            while contador_productos < len(vg.lista_productos):
                producto = vg.lista_productos[contador_productos]
                if producto["codigo"] == codigo_producto:
                    producto["cantidad"] = producto["cantidad"] + cantidad_en_carrito
                    break
                contador_productos = contador_productos + 1
            
            # Eliminar del carrito
            vg.lista_carrito.pop(contador)
            break
        contador = contador + 1
    
    mostrar_productos_en_carrito()
    mostrar_todos_los_productos()
    calcular_total_carrito()


def cancelar_compra():
    respuesta = messagebox.askyesno("CANCELAR COMPRA", "¿DESEA CANCELAR LA COMPRA?")
    if respuesta == False:
        return
    

    contador_carrito = 0
    while contador_carrito < len(vg.lista_carrito):
        item = vg.lista_carrito[contador_carrito]
        
        contador_productos = 0
        while contador_productos < len(vg.lista_productos):
            producto = vg.lista_productos[contador_productos]
            if producto["codigo"] == item["codigo"]:
                producto["cantidad"] = producto["cantidad"] + item["cantidad"]
                break
            contador_productos = contador_productos + 1
        
        contador_carrito = contador_carrito + 1
    
    vg.lista_carrito.clear()
    
    mostrar_productos_en_carrito()
    mostrar_todos_los_productos()
    calcular_total_carrito()
    
    
    messagebox.showinfo("CANCELADO", "COMPRA CANCELADA")

  
# Función de la compra final
def finalizar_compra():
    if len(vg.lista_carrito) == 0:
        messagebox.showinfo("CARRITO VACÍO", "NO AGREGASTE PRODUCTOS AL CARRITO")
        return
    
    # Creación de la compra
    texto_factura = "========== FACTURA ==========\n\n"
    total_final = 0
    
    contador = 0
    while contador < len(vg.lista_carrito):
        item = vg.lista_carrito[contador]
        nombre = item['nombre']
        cantidad = str(item['cantidad'])
        subtotal = str(round(item['subtotal'], 2))
        
        linea = nombre + " x " + cantidad + " = Bs. " + subtotal + "\n"
        texto_factura = texto_factura + linea
        total_final = total_final + item["subtotal"]
        contador = contador + 1
    
    texto_factura = texto_factura + "\n" + "=" * 30
    total_texto = "\nTOTAL A PAGAR: Bs. " + str(round(total_final, 2))
    texto_factura = texto_factura + total_texto
    texto_factura = texto_factura + "\n" + "=" * 30
    
    messagebox.showinfo("COMPRA FINALIZADA", texto_factura)
    
    # Cerrar el programa
    vg.ventana_principal.destroy()

# Función de calcular el precio total del carrito
def calcular_total_carrito():
    total = 0
    contador = 0
    while contador < len(vg.lista_carrito):
        item = vg.lista_carrito[contador]
        total = total + item["subtotal"]
        contador = contador + 1
    
    total_redondeado = round(total, 2)
    texto_total = "TOTAL A PAGAR: Bs. " + str(total_redondeado)
    vg.etiqueta_total.config(text=texto_total)

# Función para mostrar los productos en la tabla del carrito
def mostrar_productos_en_carrito():
    vg.tabla_carrito.delete(*vg.tabla_carrito.get_children())
    

    contador = 0
    while contador < len(vg.lista_carrito):
        item = vg.lista_carrito[contador]
        valores = (item["codigo"], item["nombre"], item["precio"], item["cantidad"], item["subtotal"])
        vg.tabla_carrito.insert("", "end", values=valores)
        contador = contador + 1

# Función mostrar los productos
def mostrar_todos_los_productos():
    
    vg.tabla_productos.delete(*vg.tabla_productos.get_children())
    
    contador = 0
    while contador < len(vg.lista_productos):
        producto = vg.lista_productos[contador]
        
        # Determina si el producto está disponible
        if producto["cantidad"] == 0:
            etiqueta_estado = "agotado"
        else:
            etiqueta_estado = ""
        
        valores = (producto["codigo"], producto["nombre"], producto["precio"], producto["cantidad"])
        vg.tabla_productos.insert("", "end", values=valores, tags=(etiqueta_estado,))
        
        contador = contador + 1

# Funcion buscar productos
def buscar_productos():
    texto_busqueda = vg.entrada_buscador.get()
    texto_busqueda = texto_busqueda.lower()
    
    vg.tabla_productos.delete(*vg.tabla_productos.get_children())
    
    contador = 0
    while contador < len(vg.lista_productos):
        producto = vg.lista_productos[contador]
        nombre_producto = producto["nombre"]
        nombre_producto = nombre_producto.lower()
        
        if texto_busqueda in nombre_producto:
            if producto["cantidad"] == 0:
                etiqueta_estado = "agotado"
            else:
                etiqueta_estado = ""
            
            valores = (producto["codigo"], producto["nombre"], producto["precio"], producto["cantidad"])
            vg.tabla_productos.insert("", "end", values=valores, tags=(etiqueta_estado,))
        
        contador = contador + 1