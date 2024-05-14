import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import pathlib
import folium
from streamlit_folium import st_folium


custom_airports = pathlib.Path('./datasets/custom_datasets/ar-airports.csv')
custom_lakes = pathlib.Path('./datasets/custom_datasets/lagos_arg.csv')

def elevation_map():
    # Me guardo nombre aeropuerto,coords y elevation_name
    st.write("Mapa de Aeropuertos")
    airport_data={}
    coords=[]
    for i,row in airports_df.iterrows():
        
        airport_data[row['name']] = {
        'latitude_deg': row['latitude_deg'],
        'longitude_deg': row['longitude_deg'],
        'elevation_name': row['elevation_name']
        }
        
        coords.append({
                    'name' : row['name'],
                    'latitude': float(row['latitude_deg']),
                    'longitude':float(row['longitude_deg']),
                    'elevation_name': row['elevation_name']
        })

    # Mapa con st.map()
    st.map(coords)
    
    # Mapa con Folium
    map = folium.Map(location=[coords[0]['latitude'], coords[0]['longitude']], zoom_start=4)

    for i in coords:
        location = i['latitude'],i['longitude']
        if i['elevation_name'] == 'bajo':
            folium.Marker(location,popup='green',icon=folium.Icon(color='green')).add_child(folium.Popup(i['name'])).add_to(map)    
        if i['elevation_name'] == 'medio':
            folium.Marker(location,popup='lightblue',icon=folium.Icon(color='lightblue')).add_child(folium.Popup(i['name'])).add_to(map) 
        if i['elevation_name'] == 'altos':
            folium.Marker(location,popup='red',icon=folium.Icon(color='red')).add_child(folium.Popup(i['name'])).add_to(map)  
    st_folium(map)


    # "Mapa" generando puntos con matplotlib    
    #fig, ax = plt.subplots()
    #color_map = {'altos': 'red', 'medio': 'green', 'bajo': 'blue','unknown':'white'}
    #for aeropuerto, info in airport_data.items():
    #    latitud = info['latitude_deg']
    #    longitud = info['longitude_deg']
    #    elevacion = info['elevation_name']
    #    if elevacion in color_map:
    #        ax.scatter(longitud, latitud, color=color_map[elevacion])
    #    else:
    #        ax.scatter(longitud, latitud, color=color_map['unknown'])
    #ax.set_xlabel('Longitud')
    #ax.set_ylabel('Latitud')
    #ax.legend(color_map.keys(), title='Elevación')
    #ax.set_title('Mapa de Aeropuertos')
    #ax.set_xlim(-80,-40)
    #ax.set_ylim(-60,-20)
    #ax.legend()
    #st.pyplot(fig)

def airport_widgets():
    return ''

def coords_map():
    return ''

def lakes_widgets():
    return ''
# Cargo los datos que voy a usar
airports_df = pd.read_csv(custom_airports)
lakes_df = pd.read_csv(custom_lakes)

# Menu para elegir info de que dataset visualizar

tipo_visualizacion = st.selectbox("Selecciona el conjunto de datos a visualizar:", 
                                    ('Aeropuertos', 'Lagos'),
                                    index=None,
                                    placeholder="Elegir dataset")

if tipo_visualizacion == 'Aeropuertos':
    elevation_map()
    airport_widgets()
elif tipo_visualizacion == 'Lagos':
    coords_map()
    lakes_widgets()

