import tkinter as tk
from tkinter import ttk, messagebox
import os 
import pandas as pd

# Lista para guardar todos los productos de la farmacia
lista_productos = []

# Lista para guardar los productos que el cliente quiere comprar
lista_carrito = []

# Función para cargar datos desde Excel
def cargar_productos_desde_excel():
    # Verificar si el archivo existe
    if os.path.exists("datos_farmacia.xlsx") == False:
        messagebox.showerror("ERROR", "El archivo datos_farmacia.xlsx no se encontró.")
        return False
    
    datos_excel = pd.read_excel("datos_farmacia.xlsx")
    
    contador = 0
    while contador < len(datos_excel):
        fila_actual = datos_excel.iloc[contador]
        
        producto_nuevo = {}
        producto_nuevo["codigo"] = fila_actual["CÓDIGO"]
        producto_nuevo["nombre"] = fila_actual["NOMBRE"]
        producto_nuevo["precio"] = fila_actual["PRECIO"]
        producto_nuevo["cantidad"] = int(fila_actual["CANTIDAD"])
        
        lista_productos.append(producto_nuevo)
        
        contador = contador + 1
    
    numero_productos = len(lista_productos)
    mensaje = "Se cargaron " + str(numero_productos) + " productos correctamente"
    print(mensaje)
    return True


# Función mostrar los productos
def mostrar_todos_los_productos():
    
    tabla_productos.delete(*tabla_productos.get_children())
    
    contador = 0
    while contador < len(lista_productos):
        producto = lista_productos[contador]
        
        # Determina si el producto está disponible
        if producto["cantidad"] == 0:
            etiqueta_estado = "agotado"
        else:
            etiqueta_estado = ""
        
        valores = (producto["codigo"], producto["nombre"], producto["precio"], producto["cantidad"])
        tabla_productos.insert("", "end", values=valores, tags=(etiqueta_estado,))
        
        contador = contador + 1

# Funcion buscar productos
def buscar_productos():
    texto_busqueda = entrada_buscador.get()
    texto_busqueda = texto_busqueda.lower()
    
    tabla_productos.delete(*tabla_productos.get_children())
    
    contador = 0
    while contador < len(lista_productos):
        producto = lista_productos[contador]
        nombre_producto = producto["nombre"]
        nombre_producto = nombre_producto.lower()
        
        if texto_busqueda in nombre_producto:
            if producto["cantidad"] == 0:
                etiqueta_estado = "agotado"
            else:
                etiqueta_estado = ""
            
            valores = (producto["codigo"], producto["nombre"], producto["precio"], producto["cantidad"])
            tabla_productos.insert("", "end", values=valores, tags=(etiqueta_estado,))
        
        contador = contador + 1

# Función agregar productos al carrito
def agregar_producto_al_carrito():
    # Verificar que haya un producto seleccionado
    seleccion = tabla_productos.selection()
    if len(seleccion) == 0:
        messagebox.showwarning("ADVERTENCIA", "POR FAVOR SELECCIONA UN PRODUCTO")
        return
    
    # Obtener la cantidad ingresada
    texto_cantidad = entrada_cantidad.get()
    
    # Verificar que la cantidad sea válida
    if texto_cantidad.isdigit() == False:
        messagebox.showwarning("ADVERTENCIA", "INGRESA UNA CANTIDAD VALIDA (SOLO NÚMEROS)")
        return
    
    cantidad_deseada = int(texto_cantidad)
    if cantidad_deseada <= 0:
        messagebox.showwarning("ADVERTENCIA", "LA CANTIDAD DEBE SER MAYOR A 0")
        return
    
    # Obtener los datos del producto seleccionado
    datos_producto = tabla_productos.item(seleccion)["values"]
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
    while contador < len(lista_carrito):
        item_carrito = lista_carrito[contador]
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
        lista_carrito.append(nuevo_item)
    
    # Reducir el stock del producto
    contador = 0
    while contador < len(lista_productos):
        producto = lista_productos[contador]
        if producto["codigo"] == codigo_producto:
            producto["cantidad"] = producto["cantidad"] - cantidad_deseada
            break
        contador = contador + 1
    
    mostrar_productos_en_carrito()
    mostrar_todos_los_productos()
    calcular_total_carrito()
    
    entrada_cantidad.delete(0, tk.END)

# Función para mostrar los productos en la tabla del carrito
def mostrar_productos_en_carrito():
    tabla_carrito.delete(*tabla_carrito.get_children())
    

    contador = 0
    while contador < len(lista_carrito):
        item = lista_carrito[contador]
        valores = (item["codigo"], item["nombre"], item["precio"], item["cantidad"], item["subtotal"])
        tabla_carrito.insert("", "end", values=valores)
        contador = contador + 1

# Funcion para quitar el producto del carrito
def quitar_producto_del_carrito():
    seleccion = tabla_carrito.selection()
    if len(seleccion) == 0:
        messagebox.showwarning("ADVERTENCIA", "SELECCIONE UN PRODUCTO DEL CARRITO PARA QUITAR")
        return
    
    # Obtener datos del producto a quitar
    datos_item = tabla_carrito.item(seleccion)["values"]
    codigo_producto = datos_item[0]
    nombre_producto = datos_item[1]
    cantidad_en_carrito = datos_item[3]
    
    pregunta = "¿DESEA QUITAR " + nombre_producto + " DEL CARRITO?"
    respuesta = messagebox.askyesno("CONFIRMAR", pregunta)
    if respuesta == False:
        return
    
    # Buscar y quitar el producto del carrito
    contador = 0
    while contador < len(lista_carrito):
        item = lista_carrito[contador]
        if item["codigo"] == codigo_producto:
            contador_productos = 0
            while contador_productos < len(lista_productos):
                producto = lista_productos[contador_productos]
                if producto["codigo"] == codigo_producto:
                    producto["cantidad"] = producto["cantidad"] + cantidad_en_carrito
                    break
                contador_productos = contador_productos + 1
            
            # Eliminar del carrito
            lista_carrito.pop(contador)
            break
        contador = contador + 1
    
    mostrar_productos_en_carrito()
    mostrar_todos_los_productos()
    calcular_total_carrito()
    

def calcular_total_carrito():
    total = 0
    contador = 0
    while contador < len(lista_carrito):
        item = lista_carrito[contador]
        total = total + item["subtotal"]
        contador = contador + 1
    
    total_redondeado = round(total, 2)
    texto_total = "TOTAL A PAGAR: Bs. " + str(total_redondeado)
    etiqueta_total.config(text=texto_total)

# Función de la compra final
def finalizar_compra():
    if len(lista_carrito) == 0:
        messagebox.showinfo("CARRITO VACÍO", "NO AGREGASTE PRODUCTOS AL CARRITO")
        return
    
    # Creación de la compra
    texto_factura = "-------FACTURA------\n\n"
    total_final = 0
    
    contador = 0
    while contador < len(lista_carrito):
        item = lista_carrito[contador]
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
    ventana_principal.destroy()

def cancelar_compra():
    respuesta = messagebox.askyesno("CANCELAR COMPRA", "¿DESEA CANCELAR LA COMPRA?")
    if respuesta == False:
        return
    

    contador_carrito = 0
    while contador_carrito < len(lista_carrito):
        item = lista_carrito[contador_carrito]
        
        contador_productos = 0
        while contador_productos < len(lista_productos):
            producto = lista_productos[contador_productos]
            if producto["codigo"] == item["codigo"]:
                producto["cantidad"] = producto["cantidad"] + item["cantidad"]
                break
            contador_productos = contador_productos + 1
        
        contador_carrito = contador_carrito + 1
    
    lista_carrito.clear()
    
    mostrar_productos_en_carrito()
    mostrar_todos_los_productos()
    calcular_total_carrito()
    
    
    messagebox.showinfo("CANCELADO", "COMPRA CANCELADA")

def crear_interfaz():
    global ventana_principal, tabla_productos, tabla_carrito, entrada_buscador, entrada_cantidad, etiqueta_total
    
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

    # Buscador
    tk.Label(frame_productos, text="Buscar producto:", font=("Arial", 10)).pack(pady=5)
    entrada_buscador = tk.Entry(frame_productos, font=("Arial", 12), width=40)
    entrada_buscador.pack(pady=5)
    entrada_buscador.bind("<KeyRelease>", lambda event: buscar_productos())
    
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


    frame_agregar = tk.Frame(frame_principal)
    frame_agregar.grid(row=1, column=0, pady=10, sticky="ew")
    
    tk.Label(frame_agregar, text="CANTIDAD:", font=("Arial", 12, "bold")).pack(side="left", padx=5)
    entrada_cantidad = tk.Entry(frame_agregar, font=("Arial", 12), width=10)
    entrada_cantidad.pack(side="left", padx=5)
    
    boton_agregar = tk.Button(frame_agregar, text="AGREGAR AL CARRITO", font=("Arial", 12, "bold"), command=agregar_producto_al_carrito)
    boton_agregar.pack(side="left", padx=20)
    

    # Frame del carrito
    
    frame_carrito = tk.LabelFrame(frame_principal, text="CARRITO DE COMPRAS", font=("Arial", 12, "bold"))
    frame_carrito.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
    
    # Tabla del carrito
    columnas_carrito = ("CÓDIGO", "NOMBRE", "PRECIO", "CANTIDAD", "SUBTOTAL")
    tabla_carrito = ttk.Treeview(frame_carrito, columns=columnas_carrito, show="headings", height=8)
    
    # Configurar columnas del carrito
    tabla_carrito.heading("CÓDIGO", text="CÓDIGO")
    tabla_carrito.heading("NOMBRE", text="NOMBRE")
    tabla_carrito.heading("PRECIO", text="PRECIO (Bs.)")
    tabla_carrito.heading("CANTIDAD", text="CANTIDAD")
    tabla_carrito.heading("SUBTOTAL", text="SUBTOTAL (Bs.)")
    
    tabla_carrito.column("CÓDIGO", width=80, anchor="center")
    tabla_carrito.column("NOMBRE", width=180, anchor="center")
    tabla_carrito.column("PRECIO", width=100, anchor="center")
    tabla_carrito.column("CANTIDAD", width=80, anchor="center")
    tabla_carrito.column("SUBTOTAL", width=120, anchor="center")
    
    tabla_carrito.pack(padx=5, pady=5, fill="both", expand=True)

    # Botones
    
    frame_botones = tk.Frame(frame_principal)
    frame_botones.grid(row=3, column=0, pady=10, sticky="ew")
    
    # Botón quitar del carrito
    boton_quitar = tk.Button(frame_botones, text="QUITAR DEL CARRITO", font=("Arial", 12, "bold"), command=quitar_producto_del_carrito)
    boton_quitar.pack(side="left", padx=5)
    
    # Etiqueto de precio a pagar
    etiqueta_total = tk.Label(frame_botones, text="TOTAL A PAGAR: Bs. 0.00", font=("Arial", 14, "bold"), fg="blue")
    etiqueta_total.pack(side="left", padx=50)
    
    # Botón finalizar compra
    boton_finalizar = tk.Button(frame_botones, text="FINALIZAR COMPRA", font=("Arial", 12, "bold"), command=finalizar_compra)
    boton_finalizar.pack(side="right", padx=5)
    
    # Botón cancelar compra
    boton_cancelar = tk.Button(frame_botones, text="CANCELAR COMPRA", font=("Arial", 12, "bold"), command=cancelar_compra)
    boton_cancelar.pack(side="right", padx=5)

# Función Principal:
def main():
    # Cargar los productos desde Excel
    resultado = cargar_productos_desde_excel()
    if resultado == False:
        print("ERROR: NO SE PUDIERON CARGAR LOS PRODUCTOS")
        return

    crear_interfaz()
    mostrar_todos_los_productos()
    ventana_principal.mainloop()

if __name__ == "__main__":
    main()