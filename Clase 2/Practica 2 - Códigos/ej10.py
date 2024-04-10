names = """ Agustin, Yanina, Andrés, Ariadna, Bautista, CAROLINA, 
CESAR, David, Diego, Dolores, DYLAN, ELIANA, Emanuel, Fabián, Noelia, 
Francsica', FEDERICO, Fernanda, GONZALO, Nancy """
goals = [0, 10, 4, 0, 5, 14, 0, 0, 7, 2, 1, 1, 1, 5, 6, 1, 1, 2, 0, 
11]
goals_avoided = [0, 2, 0, 0, 5, 2, 0, 0, 1, 2, 0, 5, 5, 0, 1, 0, 2, 
3, 0, 0]
assists = [0, 5, 1, 0, 5, 2, 0, 0, 1, 2, 1, 5, 5, 0, 1, 0, 2, 3, 1, 
0]
### PUNTO 1- Generar una estructura con todas las estadisticas asociadas a cada jugador

#Separo los nombres en una lista
lista_nombres=list(i.strip() for i in names.split(","))

#Junto toda la info de goles,goles evitados y asistencias

# info=list((goals[i],goals_avoided[i],assists[i]) for i in range(len(lista_nombres)))
info = list(zip(goals, goals_avoided, assists))

#Armo un diccionario con el nombre y la tupla de info que le corresponde
#El uso de zip me ahorra escribir la iteracion con for -lista_nombres[i]=info[i]-
diccionario_jugadores=dict(zip(lista_nombres, info))

###PUNTO 2- Conocer el nombre y la catidad del mas goleador

nombre_goleador=list((name,data[0]) for name,data in diccionario_jugadores.items() if data == max(diccionario_jugadores.values()))[0]
print(f"\nEl maximo goleador con {nombre_goleador[1]} goles es {nombre_goleador[0]}\n")

###PUNTO 3-Jugador mas influyente

#Accediendo a la info de cada jugador, armo una lista con el valor que posee cada uno
#influencia = list(((i*1.5)+(j*1.25)+(k)) for i,j,k in diccionario_jugadores.values())
influencia = list(map(lambda i: (i[0] * 1.5) + (i[1] * 1.25) + i[2], diccionario_jugadores.values()))

#Encuentro en que posicion se encuentra el que mayor influencia tiene
indice_mayor_influencia= influencia.index(max(influencia))
#A partir del indice, accedo al diccionario y me quedo con el nombre
nombre_mayor_influencia =list(diccionario_jugadores.keys())[indice_mayor_influencia]
print(f"El jugador mas influyente fue {nombre_mayor_influencia} con un valor de {max(influencia)} puntos\n")

###PUNTO 4- El promedio de goles por partido del equipo, se jugaron 25 partidos.
#Sumo todos los goles y divido por el total de partidos
goles_totales=sum(diccionario_jugadores[nombre][0] for nombre in diccionario_jugadores)
print(f"El promedio de gol por partido del equipo es {goles_totales/25}\n")

###PUNTO 5- El promedio de gol por partido del goleador
#Usando lo desarrollado en el punto 2
print(f"El promedio de gol del goleador es de {(diccionario_jugadores.get(nombre_goleador[0])[0])/25} por partido\n")