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

ventana.mainloop()