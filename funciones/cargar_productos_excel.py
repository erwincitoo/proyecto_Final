import os 
import pandas as pd
from tkinter import messagebox
import variables_globales as vg
# Lista para guardar todos los productos de la farmacia
vg.lista_productos = []

# Lista para guardar los productos que el cliente quiere comprar
vg.lista_carrito = []

# Función para cargar los productos desde Excel
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
        
        vg.lista_productos.append(producto_nuevo)
        
        contador = contador + 1
    
    numero_productos = len(vg.lista_productos)
    mensaje = "Se cargaron " + str(numero_productos) + " productos correctamente"
    print(mensaje)
    return True