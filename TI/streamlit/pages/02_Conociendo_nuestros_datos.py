import streamlit as st
import pathlib
import pandas as pd
#Mapa con streamlit-folium
import folium
from streamlit_folium import st_folium
import matplotlib as mpl
# Mapa - graficos con plotly
import plotly.express as px
import plotly.graph_objects as go
#Mapa con matplotlib
import matplotlib.pyplot as plt
# Para agregarle el fondo al mapa con matplotlib
import contextily as ctx

custom_airports = pathlib.Path('./datasets/custom_datasets/ar-airports.csv')
custom_lakes = pathlib.Path('./datasets/custom_datasets/lagos_arg.csv')

def elevation_map():
    
    st.write("Mapa de Aeropuertos")
    libreria = st.selectbox("Selecciona con que libreria ver mapa:", 
                                    ('Streamlit .map()', 'Streamlit-Folium','Plotly','Matplotlib'),
                                    index=None,
                                    placeholder="Elegir libreria")
    
    #
    coords=[]
    for i,row in airports_df.iterrows():
        coords.append({
                    'name' : row['name'],
                    'latitude': float(row['latitude_deg']),
                    'longitude':float(row['longitude_deg']),
                    'elevation_name': row['elevation_name']
        })

    # Mapa con st.map()
    if libreria == 'Streamlit .map()':
        st.map(coords)
    # Mapa con Folium
    elif libreria == 'Streamlit-Folium':
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
    
    # Mapa con plotly
    elif libreria == 'Plotly':
        #Modifico el dataset para lo que necesito
        color = {
        'bajo' : 'green',
        'medio': 'lightblue',
        'altos': 'red'
        }
        airports_df['color'] = airports_df['elevation_name'].map(color)
        
        fig = go.Figure(data=go.Scattergeo(
            lon = airports_df['longitude_deg'],
            lat = airports_df['latitude_deg'],
            text = airports_df['name'],
            mode = 'markers',
            marker_color=airports_df['color'],
            marker_size=4
            ))

        fig.update_layout(
            title = 'Mapa aeropuertos color segun elevation_name',
            geo_scope='world',
            geo_bgcolor='rgba(0, 0, 0, 0)',  
            geo=dict(
                showland=True,  
                landcolor='rgb(243, 243, 243)',
                showlakes=True,  
                lakecolor='rgb(255, 255, 255)',  
                showocean=True,  
                oceancolor='rgb(255, 255, 255)',  
                showcountries=True,  
                countrycolor='rgb(0, 0, 0)',  
                projection_type='equirectangular',  
                center=dict(lon=-60, lat=-40),  
                projection_scale=3,  
            ),
            width=800,
            height=600,
        )
        st.plotly_chart(fig)
    # "Mapa" generando puntos con matplotlib  
    elif libreria == 'Matplotlib':
        
        fig, ax = plt.subplots()
        color_map = {'altos': 'red', 'medio': 'green', 'bajo': 'blue','unknown':'black'}
        
        for elevacion, data in airports_df.groupby('elevation_name'):
            color = color_map.get(elevacion)
            ax.scatter(data['longitude_deg'], data['latitude_deg'], color=color, label=elevacion,s=4,alpha=.5)
        ax.set_xlabel('Longitud')
        ax.set_ylabel('Latitud')
        ax.legend(color_map.keys(), title='Elevación')
        ax.set_title('Mapa de Aeropuertos')
        ax.set_xlim(-80,-50)
        ax.set_ylim(-60,-20)
        ax.legend()
        ctx.add_basemap(ax, crs='EPSG:4326', url='https://tiles.stadiamaps.com/static/alidade_satellite.jpg?size=1372x883@2x&center=-41.103231693639515,-64.77271035057947&zoom=4')
        #fig.savefig('mapa_aeropuertos.png')
        st.pyplot(fig)


def airport_widgets():

    # Pie chart con plotly
    aeropuertos_por_provincia = airports_df['region_name'].value_counts()
    
    fig = go.Figure(data=[go.Pie(labels=aeropuertos_por_provincia.index, 
                                values=aeropuertos_por_provincia,
                                )])
    fig.update_traces(textinfo='label+percent')
    fig.update_layout(title='Número de Aeropuertos por Provincia')
    st.plotly_chart(fig)

    # Bar Chart
    fig = go.Figure(data=[go.Bar(x=aeropuertos_por_provincia.index, y=aeropuertos_por_provincia)])
    fig.update_layout(title='Cantidad de Aeropuertos por Provincia')
    fig.update_xaxes(title_text='Provincia')
    fig.update_yaxes(title_text='Cantidad de Aeropuertos')
    st.plotly_chart(fig)

    # Bar Chart MatPlotLib
    plt.figure(figsize=(10, 6))
    plt.bar(aeropuertos_por_provincia.index, aeropuertos_por_provincia)
    plt.title('Número de Aeropuertos por Provincia')
    plt.xlabel('Provincia')
    plt.ylabel('Número de Aeropuertos')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(plt)


    # #Choropleth Map Plotly // NO FUNCIONA, muestra mapa vacio
    # import json
    # mapa = json.load(open('./streamlit/data/argentina.geojson','r'))

    # airports_df['region_name'] = airports_df['region_name'].str.strip().replace(" Province", "")
    # print(airports_df.head())
    # province_id_map = airports_df.groupby('region_name').size().reset_index(name='num')
    # province_id_map['provincia_id'] = range(1, len(aeropuertos_por_provincia) + 1)
    # fig = px.choropleth(
    #     province_id_map,
    #     locations="provincia_id",
    #     geojson=mapa,
    #     color="num",
    #     hover_name="region_name",
    #     hover_data=["region_name"],
    #     title="Cantidad de Aeropuertos por Provincia",
    # )
    # #fig.update_geos(fitbounds="locations", visible=False)
    # st.plotly_chart(fig)
def coords_map():
    return ''

def lakes_widgets():
    return ''


# Menu para elegir info de que dataset visualizar
tipo_visualizacion = st.selectbox("Selecciona el conjunto de datos a visualizar:", 
                                    ('Aeropuertos', 'Lagos'),
                                    index=None,
                                    placeholder="Elegir dataset")

if tipo_visualizacion == 'Aeropuertos':

    airports_df = pd.read_csv(custom_airports)
    elevation_map()
    airport_widgets()

elif tipo_visualizacion == 'Lagos':

    lakes_df = pd.read_csv(custom_lakes)
    coords_map()
    lakes_widgets()

