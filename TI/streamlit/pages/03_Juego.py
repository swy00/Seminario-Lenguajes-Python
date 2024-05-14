import streamlit as st
import pathlib
import json
import os
import datetime as dt
import random
import csv

custom_airports = pathlib.Path('../datasets/custom_datasets/ar-airports.csv')

campos_utiles_aero = {"type": 2, "name": 3, "elevation_name": 23, "region": 10, "municipality": 13, "iata_code": 16}
campos_utiles_lagos = {"Nombre": 0, "Ubicación": 1, "Superficie (km²)": 2, "Profundidad máxima (m)": 3, "Profundidad media (m)": 4, "Latitud": 5, "Longitud": 6, "Sup tamaño": 7}
campos_utiles_conect = {"Provincia": 0, "Partido": 1, "Localidad": 2, "Poblacion": 3, "ADSL": 4," CABLEMODEM": 5, "DIALUP": 6, "FIBRAOPTICA": 7, "SATELITAL": 8, "WIRELESS": 9, "TELEFONIAFIJA": 10, "3G": 11, "4G": 12}
campos_utiles_censo = {"Jurisdicción": 0, "Total de población": 1, "Varones Total de población": 5, "Mujeres Total de población": 9, "Porcentaje de población en situación de calle": 13}
campos_utiles = {"Aeropuertos": campos_utiles_aero,
                 "Lagos": campos_utiles_lagos, 
                 "Conectividad": campos_utiles_conect, 
                 "Censo 2022": campos_utiles_censo
                 }

read_data = pathlib.Path('./streamlit/data/user_data.json')
with (read_data.open(mode='r', encoding='utf-8') as read_file):
    data_load = json.load(read_file)
    user = map(lambda y: y["Mail"], data_load)
st.header("Bienvenido a Pytrivia!!")
st.subheader("Para comenzar la trivia seleccione el usuario")

player_data = st.empty()
with player_data.form("registration"):
    username = st.selectbox("User", options= sorted(user))
    tema = st.selectbox("Temática",campos_utiles.keys())
    dificultad = st.selectbox("Dificultad",["Alta", "Media", "Fácil"])
    start = st.form_submit_button('Iniciar Juego')

if start:
    game_data = st.empty()
    with game_data.form("trivia"):
        st.header(f"Comenzando la trivia para el usuario")
        st.subheader(username)
        st.subheader(f"Dificultad {dificultad}")
        st.subheader(f"Temática {tema}")
        st.divider()

        match tema:
            case "Aeropuertos": read_data = pathlib.Path('./datasets/custom_datasets/ar-airports.csv')
            case "Lagos": read_data =  pathlib.Path("./datasets/custom_datasets/lagos_arg.csv")
            case "Conectividad": read_data = pathlib.Path('./datasets/custom_datasets/Conectividad_Internet.csv')
            case "Censo 2022": read_data = pathlib.Path('./datasets/custom_datasets/c2022_tp_c_resumen_adaptado.csv')

        puntos = 0

        with (read_data.open(mode='r', encoding='utf-8') as read_file):
            dataset = csv.reader(read_file)
            next(dataset)
            list_dataset = list(dataset)
            
            lines_sample = random.sample(list_dataset, 5)
            for line in lines_sample:
                st.subheader(f"Pregunta {lines_sample.index(line)+1}")
                atribute_sample = random.sample(list(campos_utiles[tema]),k=4)
                for atribute in atribute_sample[0:3]: 
                    st.write(f"{atribute}: {line[campos_utiles[tema][atribute]]}")
                st.write(f"{atribute_sample[3]}")    
# Necesito que esta variable respuesta tenga distinto nombre para cada una de las lineas en la muestra                
                respuesta = st.text_input(f"{atribute_sample[3]}", placeholder="Ingrese su respuesta")
                if respuesta == line[campos_utiles[tema][atribute_sample[3]]]:
                    puntos += 1
                st.divider()
        
        finish = st.form_submit_button('Responder')
    
    if finish:
        st.header(f"Puntaje: {puntos}")