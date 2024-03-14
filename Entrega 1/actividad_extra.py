def agregarProducto(inventario):
    #Le pido al usuario
    nombre = input("Ingresar nombre del producto: ")
    cantidad=input("Ingrese la cantidad inicial del producto: ")
    #Caso de producto duplicado, le sumo la cantidad de productos
    if nombre in inventario:
        inventario[nombre]+=cantidad
    else:
        inventario[nombre]=cantidad

def eliminarProducto(inventario):
    #Le pido al usuario el nombre del producto a eliminar y la cantidad
    nombre = input("Ingresar nombre del producto a eliminar: ")
    if nombre in inventario:
        print("Producto eliminado.")
        del inventario[nombre]
    else:
        print(f"No se encontró {nombre} en el inventario")

def mostrarInventario(inventario):
    for i,j in inventario.items():
        print(f"{i} : {j}")

inventario={}
while True:
    menu =int(input(f"""
        ----Elegir una opción:----
            1. Agregar producto
            2. Eliminar producto
            3. Mostrar inventario
            4. Salir del programa 
            Ingresa tu opcion : """))
    if menu == 1:
        agregarProducto(inventario)
    elif menu== 2:
        eliminarProducto(inventario)
    elif menu== 3:
        mostrarInventario(inventario)
    elif menu== 4:
        print("Saliendo del programa.")
        break
    else:
        print("Opcion no valida, volver a ingresar.")