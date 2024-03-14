#Implementa un programa que solicite al usuario que ingrese una lista de números.
#Luego, imprime la lista pero detén la impresión si encuentras un número negativo.
#Nota: utilice la sentencia break cuando haga falta.

lista = input("Introducir lista de números (dejando espacios entre c/u)").split()
for i in lista:
    i=int(i)
    if i>=0:
        print(i)
    else:
        break