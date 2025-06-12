import pandas as pd
import variables_globales2 as vg2
import traceback
from tkinter import messagebox
import os

# Función Actualizar el documento Excel
def actualizar_excel():
    try:
        # Usar datos_originales en lugar de los datos de la tabla (que pueden estar filtrados)
        columnas = ["CÓDIGO", "NOMBRE", "TIPO", "CATEGORÍA", "LOTE", "CANTIDAD", "PRECIO"]
        df = pd.DataFrame(vg2.datos_originales, columns=columnas)

        ruta_base = os.path.dirname(__file__)
        ruta_excel = os.path.join(ruta_base, "datos_farmacia.xlsx")
        
        print(f"ACTUALIZANDO EXCEL CON {len(vg2.datos_originales)} REGISTROS")
        
        # Guardar Excel
        df.to_excel(ruta_excel, index=False)
        print("EXCEL ACTUALIZADO CORRECTAMENTE")
        
    except Exception as e:
      
        print(traceback.format_exc()) 
        messagebox.showerror("ERROR", f"NO SE PUDO ACTUALIZAR EL ARCHIVO EXCEL: {str(e)}")
