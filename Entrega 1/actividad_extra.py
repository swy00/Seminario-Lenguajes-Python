def agregarProducto(inventario):
    #Verifico que se ingrese un nombre y cantidad correcto
    while True:
        nombre = input("\n>Ingresar nombre del producto: ")
        if nombre.isalpha():
            cantidad=input(">Ingrese la cantidad inicial del producto: ")
            if cantidad.isdigit():
                print("\n !!Producto agregado correctamente.")
                break
        print("\n --Error, el nombre debe ser albafético y la cantidad numerica. \n")

    if nombre in inventario:
        inventario[nombre]+=int(cantidad)
    else:
        inventario[nombre]=int(cantidad)

def eliminarProducto(inventario):
    nombre = input("\n>Ingresar nombre del producto a eliminar: ")
    if nombre in inventario:
        print("\n**Producto eliminado.\n")
        del inventario[nombre]
    else:
        print(f"\nNo se encontró {nombre} en el inventario.\n")

def mostrarInventario(inventario):
    if len(inventario) == 0:
        print(f"\n~~El inventario está vacio~~\n")
    else:
        print(f"\n{' ' * 8}{'/' * 30}\n{' ' * 8}{'Producto':<20} {'Cantidad':<10}\n{' ' * 8}{'-' * 30}")
        for i, j in inventario.items():
            print(f"{' ' * 8} {i:<20} {j:<10}")
        print(f"{' ' * 8}{'/' * 30}")

def main():
    inventario={}
    #En un principio lo resolvi con un "try", pero luego de consultar en la practica decidí implementar la forma alternativa sin utilizarlo
    while True:
        menu =(input(f"""
            ----Elegir una opción:----
                1. Agregar producto
                2. Eliminar producto
                3. Mostrar inventario
                4. Salir del programa 
                Ingresa tu opcion : """))
        if not menu.isdigit():
            print("\n**Opcion Inválida.\n")
        else:
            if int(menu) == 1:
                agregarProducto(inventario)
            elif int(menu)== 2:
                eliminarProducto(inventario)
            elif int(menu)== 3:
                mostrarInventario(inventario)
            elif int(menu)== 4:
                print("\n//Saliendo del programa. \n")
                break  
            else:
                print("\n** Opcion inválida, volver a ingresar.\n")

if (__name__ == '__main__'):
    main()