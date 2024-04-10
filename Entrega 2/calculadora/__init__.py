def generarEstructura(names,goals,goals_avoided,assists):
    lista_nombres=list(i.strip() for i in names.split(","))
    info = list(zip(goals, goals_avoided, assists))
    diccionario_jugadores=dict(zip(lista_nombres, info))
    return diccionario_jugadores

def goleador(diccionario):
    info_goleador=list((name,data[0]) for name,data in diccionario.items() if data == max(diccionario.values()))[0]
    return (info_goleador[1],info_goleador[0])

def influencia(diccionario):
    influencia = list(map(lambda i: ((i[0] * 1.5) + (i[1] * 1.25) + i[2]), diccionario.values()))
    indice_mayor_influencia= influencia.index(max(influencia))
    nombre_mayor_influencia =list(diccionario.keys())[indice_mayor_influencia]
    return (nombre_mayor_influencia,max(influencia))

def promedioGoles(diccionario):
    goles_totales=sum(diccionario[nombre][0] for nombre in diccionario) 
    return (goles_totales/25)

def promedioGolGoleador(diccionario,nombre_goleador):
    promedio=((diccionario.get(nombre_goleador)[0])/25)
    return promedio