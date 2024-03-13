#Cree un programa que dada una lista de números imprima sólo los que son pares.
#Nota: utilice la sentencia continue donde haga falta.

lista_numeros=[24, 10, 45, 5, 49, 15, 33, 12, 39, 28, 19, 21, 4, 37, 42]
for i in lista_numeros:
    if i % 2 !=0: #Si es IMPAR, skipeo
        continue
    else:
        print(f"El numero {i} es PAR")

"""
Otra forma metiendo en otra lista de pares los numeros
lista_numeros=[24, 10, 45, 5, 49, 15, 33, 12, 39, 28, 19, 21, 4, 37, 42]
lista_pares=[]
for i in lista_numeros:
    if i % 2 !=0: #Si es IMPAR, skipeo
        continue
    else:
        lista_pares.append(i)
print(lista_pares)
"""