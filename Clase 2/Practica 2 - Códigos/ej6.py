from collections import Counter
frase= input("Ingrese una frase :")
text=input("Ingrese el string a informar: ").lower()
puntuaciones = ";:,.¿?!¡(){}'"

frase_limpia = ""
for i in frase:
    if i not in puntuaciones:
        frase_limpia += i.lower()
#Creo la lista de palabras
lista= frase_limpia.split(" ")
c={}
c=Counter(lista)

print(f'Para la frase: "{frase}"\nPalabra: {text}\nResultado: {(c[text] if text in c else "No se encuentra en la frase")}')