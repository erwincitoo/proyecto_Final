import variables_globales as vg

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