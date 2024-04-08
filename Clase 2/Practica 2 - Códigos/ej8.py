palabra = input("Ingresar una palabra o frase: ")
repetida = False
contador = 0
#Limpio la palabra
palabra_limpia = ''.join(caracter.lower() for caracter in palabra if caracter.isalpha())
#Recorro la palabra verificando la cantidad de veces que aparece una letra
for i in palabra_limpia:
    if palabra_limpia.count(i) > 1:
        repetida = True
        break
print("No es un Heterograma" if repetida else "Si es un Heterograma")