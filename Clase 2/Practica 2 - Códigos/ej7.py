text = """ La brecha salarial alcanzó el 27,7%: las mujeres ocupadas 
debieron trabajar 8 días y 10 horas más que los varones ocupados para 
ganar lo mismo que ellos en un mes. """
mayuscula=0
minuscula=0
no_letra=0
for i in text:
    if i.isalpha():
        if i.isupper():
            mayuscula+=1
        else:
            minuscula+=1
    else:
        if i.strip() != "":
            no_letra += 1
text_limpio=""
cantidad_palabras=0
for i in text.split(" "):
    if (len(i)!=0) and (i[0].isalpha() or i[0]=="\n"):
        print(i)
        text_limpio+=" "+i
        cantidad_palabras+=1

print(f"En la frase hay {mayuscula} letras mayuscula,{minuscula} letras minuscula y {no_letra} caracteres especiales.\nEn la frase hay {cantidad_palabras} palabras.")