import tkinter as tk
from tkinter import ttk
from funciones_carrito import agregar_producto_al_carrito, quitar_producto_del_carrito, finalizar_compra, cancelar_compra, buscar_productos
import variables_globales as vg
import ttkbootstrap as tb
from ttkbootstrap.constants import *

vg.lista_carrito = []
vg.lista_productos = []
import variables_globales as vg
def crear_interfaz():
    
    # Creación de la ventana principal
    vg.ventana_principal = tb.Window(themename="yeti")
    vg.ventana_principal.title("PHARMA - INTERFAZ DE COMPRAS PARA USUARIOS")
    vg.ventana_principal.geometry("1280x720+0+0")
    vg.ventana_principal.resizable(0, 0)
    
    # Frame principal
    frame_principal = tk.Frame(vg.ventana_principal)
    frame_principal.pack(padx=10, pady=10, fill="both", expand=True)
    
    frame_principal.grid_rowconfigure(0, weight=1)
    frame_principal.grid_rowconfigure(2, weight=1)
    frame_principal.grid_columnconfigure(0, weight=1)
    
    frame_productos = tk.LabelFrame(frame_principal, text="PRODUCTOS DISPONIBLES", font=("Verdana", 14, "bold"))
    frame_productos.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

    # Buscador
    tk.Label(frame_productos, text="BUSCAR PRODUCTO:", font=("Verdana", 12, "bold")).pack(pady=5)
    vg.entrada_buscador = tk.Entry(frame_productos, font=("Roboto", 10), width=40)
    vg.entrada_buscador.pack(pady=5)
    vg.entrada_buscador.bind("<KeyRelease>", lambda event: buscar_productos())
    
    # Creación de la tabla de productos
    columnas = ("CÓDIGO", "NOMBRE", "PRECIO", "CANTIDAD")
    vg.tabla_productos = ttk.Treeview(frame_productos, columns=columnas, show="headings", height=10, bootstyle="primary")
    
    # Configuración de las columnas de la tabla
    vg.tabla_productos.heading("CÓDIGO", text="CÓDIGO")
    vg.tabla_productos.heading("NOMBRE", text="NOMBRE")
    vg.tabla_productos.heading("PRECIO", text="PRECIO (Bs.)")
    vg.tabla_productos.heading("CANTIDAD", text="CANTIDAD")
    
    vg.tabla_productos.column("CÓDIGO", width=100, anchor="center")
    vg.tabla_productos.column("NOMBRE", width=200, anchor="center")
    vg.tabla_productos.column("PRECIO", width=100, anchor="center")
    vg.tabla_productos.column("CANTIDAD", width=100, anchor="center")
    
    # Configurar colores para los productos agotados
    vg.tabla_productos.tag_configure("AGOTADO", background="#ffdddd", foreground="red")
    
    vg.tabla_productos.pack(padx=5, pady=5, fill="both", expand=True)


    frame_agregar = tk.Frame(frame_principal)
    frame_agregar.grid(row=1, column=0, pady=10, sticky="ew")
    
    tk.Label(frame_agregar, text="CANTIDAD:", font=("Verdana", 14, "bold")).pack(side="left", padx=5)
    vg.entrada_cantidad = tk.Entry(frame_agregar, font=("Roboto", 10), width=10)
    vg.entrada_cantidad.pack(side="left", padx=5)
    
    boton_agregar = tk.Button(frame_agregar, text="AGREGAR AL CARRITO", font=("Verdana", 12, "bold"), command=agregar_producto_al_carrito)
    boton_agregar.pack(side="left", padx=20)
    
    # Frame del carrito
    frame_carrito = tk.LabelFrame(frame_principal, text="CARRITO DE COMPRAS", font=("Verdana", 14, "bold"))
    frame_carrito.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
    
    # Tabla del carrito
    columnas_carrito = ("CÓDIGO", "NOMBRE", "PRECIO", "CANTIDAD", "SUBTOTAL")
    vg.tabla_carrito = ttk.Treeview(frame_carrito, columns=columnas_carrito, show="headings", height=8, bootstyle="primary")
    
    # Configurar columnas del carrito
    vg.tabla_carrito.heading("CÓDIGO", text="CÓDIGO")
    vg.tabla_carrito.heading("NOMBRE", text="NOMBRE")
    vg.tabla_carrito.heading("PRECIO", text="PRECIO (Bs.)")
    vg.tabla_carrito.heading("CANTIDAD", text="CANTIDAD")
    vg.tabla_carrito.heading("SUBTOTAL", text="SUBTOTAL (Bs.)")
    
    vg.tabla_carrito.column("CÓDIGO", width=80, anchor="center")
    vg.tabla_carrito.column("NOMBRE", width=180, anchor="center")
    vg.tabla_carrito.column("PRECIO", width=100, anchor="center")
    vg.tabla_carrito.column("CANTIDAD", width=80, anchor="center")
    vg.tabla_carrito.column("SUBTOTAL", width=120, anchor="center")
    
    vg.tabla_carrito.pack(padx=5, pady=5, fill="both", expand=True)

    # Botones
    frame_botones = tk.Frame(frame_principal)
    frame_botones.grid(row=3, column=0, pady=10, sticky="ew")
    
    # Botón quitar del carrito
    boton_quitar = tk.Button(frame_botones, text="QUITAR DEL CARRITO", font=("Roboto", 12, "bold"), command=quitar_producto_del_carrito)
    boton_quitar.pack(side="left", padx=5)
    
    # Etiquetz de precio a pagar
    vg.etiqueta_total = tk.Label(frame_botones, text="TOTAL A PAGAR: Bs. 0.00", font=("Roboto", 14, "bold"), fg="blue")
    vg.etiqueta_total.pack(side="left", padx=50)
    
    # Botón finalizar compra
    boton_finalizar = tk.Button(frame_botones, text="FINALIZAR COMPRA", font=("Roboto", 12, "bold"), command=finalizar_compra)
    boton_finalizar.pack(side="right", padx=5)
    
    # Botón cancelar compra
    boton_cancelar = tk.Button(frame_botones, text="CANCELAR COMPRA", font=("Roboto", 12, "bold"), command=cancelar_compra)
    boton_cancelar.pack(side="right", padx=5)