tabla_valores={
        'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 
        'i': 1, 'j': 8,'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 
        'r': 1, 's': 1, 't': 1,'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10}
palabra=input("Ingrese una palabra: ").lower()
valor=0
#Recorro letra por letra, y voy sumando el valor de cada una al total.
for i in palabra:
    valor+= tabla_valores.get(i)

print(f"Palabra: {palabra}\nValor: {valor}")
"""
    if i in "aeioulnrst":
        valor+=1
    elif i in "dg":
        valor+=2
    elif i in "bcmp":
        valor+=3
    elif i in "fhvwy":
        valor+=4
    elif i in "k":
        valor+=5
    elif i in "jx":
        valor+=8
    elif i in "qz":
        valor+=10
    else:
        valor+=0
"""