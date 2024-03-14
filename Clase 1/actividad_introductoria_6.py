#Modifique el ejercicio 4 para que dada la lista de número genere dos nuevas listas, una
#con los número pares y otras con los que son impares. Imprima las listas al terminar de
#procesarlas.

lista = input("Introducir lista de números (dejando espacios entre c/u)").split()
lista_pares=[]
lista_impares=[]
for i in lista:
    i=int(i)
    if i%2==0:
        lista_pares.append(i)
    else:
        lista_impares.append(i)
print(f"La lista par {lista_pares} \nLa lista impar {lista_impares}")