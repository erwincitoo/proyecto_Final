from funciones import cargar_productos_desde_excel, crear_interfaz
from funciones_carrito import mostrar_todos_los_productos
import variables_globales as vg

def main():
    # Cargar los productos desde Excel
    resultado = cargar_productos_desde_excel()
    if resultado == False:
        print("ERROR: NO SE PUDIERON CARGAR LOS PRODUCTOS")
        return

    crear_interfaz()
    mostrar_todos_los_productos()
    vg.ventana_principal.mainloop()
main()