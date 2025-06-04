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

def crear_interfaz():
    global ventana_principal, tabla_productos, tabla_carrito
    
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


    frame_agregar = tk.Frame(frame_principal)
    frame_agregar.grid(row=1, column=0, pady=10, sticky="ew")
    
    tk.Label(frame_agregar, text="CANTIDAD:", font=("Arial", 12, "bold")).pack(side="left", padx=5)
    entrada_cantidad = tk.Entry(frame_agregar, font=("Arial", 12), width=10)
    entrada_cantidad.pack(side="left", padx=5)
    
    boton_agregar = tk.Button(frame_agregar, text="AGREGAR AL CARRITO", font=("Arial", 12, "bold"))
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
    boton_quitar = tk.Button(frame_botones, text="QUITAR DEL CARRITO", font=("Arial", 12, "bold"))
    boton_quitar.pack(side="left", padx=5)
    
    # Etiqueto de precio a pagar
    etiqueta_total = tk.Label(frame_botones, text="TOTAL A PAGAR: Bs. 0.00", font=("Arial", 14, "bold"), fg="blue")
    etiqueta_total.pack(side="left", padx=50)
    
    # Botón finalizar compra
    boton_finalizar = tk.Button(frame_botones, text="FINALIZAR COMPRA", font=("Arial", 12, "bold"))
    boton_finalizar.pack(side="right", padx=5)
    
    # Botón cancelar compra
    boton_cancelar = tk.Button(frame_botones, text="CANCELAR COMPRA", font=("Arial", 12, "bold"))
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