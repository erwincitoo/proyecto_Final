import os
import pandas as pd
from tkinter import messagebox
import variables_globales2 as vg2

# Función para cargar los datos de Excel
def cargar_datos_excel():
    ruta_actual = os.path.dirname(__file__)
    ruta_excel = os.path.join(ruta_actual, "datos_farmacia.xlsx")
    if os.path.exists(ruta_excel):
        df = pd.read_excel(ruta_excel)
        vg2.datos_originales = []
        for _, fila in df.iterrows():
            valores = tuple(fila)
            vg2.tabla_tree.insert("", "end", values=valores)
            vg2.datos_originales.append(valores)
    else:
        messagebox.showwarning("ADVERTENCIA", "ARCHIVO 'datos_farmacia.xlsx' NO ENCONTRADO.")