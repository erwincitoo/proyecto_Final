import variables_globales2 as vg2

# Función para buscar productos por código o nombre
def buscar_producto(event=None):
    termino_busqueda = vg2.busqueda_entry.get().lower().strip()
    
    for item in vg2.tabla_tree.get_children():
        vg2.tabla_tree.delete(item)
    
    # Si no hay término de búsqueda, mostrar todos los datos
    if not termino_busqueda:
        for datos in vg2.datos_originales:
            vg2.tabla_tree.insert("", "end", values=datos)
        return
    
    # Filtrar datos que coincidan con el valor de búsqueda
    resultados_encontrados = False
    for datos in vg2.datos_originales:
        codigo = str(datos[0]).lower()
        nombre = str(datos[1]).lower()
        
        # Buscar a través de un código o nombre
        if termino_busqueda in codigo or termino_busqueda in nombre:
            vg2.tabla_tree.insert("", "end", values=datos)
            resultados_encontrados = True
    
    # Si no se encontraron resultados, mostrar el mensaje
    if not resultados_encontrados and termino_busqueda:
        vg2.tabla_tree.insert("", "end", values=("", "NO RESULTADOS", "", "", "", "", ""))