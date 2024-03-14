#Escribe un programa que tome una lista de números enteros como entrada del usuario.
#Luego, convierte cada número en la lista a string y únelos en una sola cadena,
#separados por guiones ('-'). Sin embargo, excluye cualquier número que sea múltiplo
#de 3 de la cadena final.

lista = input("Introducir lista de números (dejando espacios entre c/u)").split()
num=[]
for i in lista:
    if int(i) % 3 != 0:
        num.append(i)
cadena="-".join(num) #Join une una lista de elementos con un separador, en este caso "-"
print(cadena)