#Haz un programa que pida al usuario que ingrese una temperatura en grados Celsius y
#luego convierta esa temperatura a grados Fahrenheit, mostrando el resultado.

celcius= int(input("Ingrese una temperatura en grados Celcius(solo numero):")) #Especifico el formato para evitarme limpiar el input
print(f"La temperatura ingresada corresponde a {(celcius*(9/5))+32} °Fahrenheit")