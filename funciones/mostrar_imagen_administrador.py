import os
import variables_globales2 as vg2
from PIL import ImageTk, Image
from tkinter import messagebox, filedialog
import shutil

def mostrar_imagen_producto(event):
    selected_item = vg2.tabla_tree.selection()
    
    if not selected_item:
        return
    
    valores = vg2.tabla_tree.item(selected_item)["values"]
    codigo_producto = valores[0]  
    
    # Buscar la imagen en el directorio
    directorio_imagenes = "imagenes"
    if not os.path.exists(directorio_imagenes):
        os.makedirs(directorio_imagenes)
    
    # Buscar cualquier archivo con el nombre del código del producto
    imagen_encontrada = False
    for extension in ['.png', '.jpg', '.jpeg', '.gif','.jfif']:
        ruta_imagen = os.path.join(directorio_imagenes, f"{codigo_producto}{extension}")
        if os.path.exists(ruta_imagen):
            try:
                # Cargar y mostrar la imagen
                imagen = Image.open(ruta_imagen)
                imagen = imagen.resize((200, 200))
                imagen_tk = ImageTk.PhotoImage(imagen)
                
                # Mostrar la imagen en el label
                vg2.label_imagen.config(image=imagen_tk)
                vg2.label_imagen.image = imagen_tk 
                imagen_encontrada = True
                break
            except Exception as e:
                print(f"ERROR AL CARGAR LA IMAGEN {ruta_imagen}: {e}")
    
    if not imagen_encontrada:
        vg2.label_imagen.config(image="", text="IMAGEN\nNO DISPONIBLE")

# Función para mostrar las imagenes de los productos
def cargar_imagen():
    selected_item = vg2.tabla_tree.selection()
    
    if not selected_item:
        messagebox.showwarning("ADVERTENCIA", "SELECCIONE UN PRODUCTO PRIMERO.")
        return
    
    valores = vg2.tabla_tree.item(selected_item)["values"]
    
    if valores[1] == "NO SE ENCONTRARON RESULTADOS":
        messagebox.showwarning("ADVERTENCIA", "SELECCIONE UN PRODUCTO VÁLIDO.")
        return
    
    codigo_producto = valores[0]  
    
    # Pedir al usuario seleccionar una imagen
    ruta_imagen = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.gif *.jfif")])
    
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
        vg2.label_imagen.config(image=imagen_tk, text="")
        vg2.label_imagen.image = imagen_tk  
        
        messagebox.showinfo("ÉXITO", f"IMAGEN ASOCIADA AL PRODUCTO {codigo_producto}")