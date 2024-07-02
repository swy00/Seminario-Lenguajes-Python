import streamlit as st
import pathlib
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
import modules
import os

GEOJSON_PATH = modules.BASE_PATH / "data" / "argentina.geojson"

st.set_page_config(
    page_title="PyTrivia",
    page_icon="🌎",
    layout="centered",
    initial_sidebar_state="auto",
)


def air_map1(airports_df):
    """Generates a map of airports in Argentina using Plotly.

    This function creates a map of airports in Argentina, colored
    according to their elevation (low, medium, high, unknown), and
    visualizes the data on an interactive geographic map.

    Args:
        airports_df (pd.DataFrame): DataFrame containing airport information.
        Must include the columns 'elevation_name', 'latitude_deg',
        'longitude_deg', and 'name'.

    Returns:
        plotly.Figure: Plotly figure with the airport map.
    """
    color = {
        "bajo": "#b5d09c",
        "medio": "#00bfff",
        "altos": "#c32148",
        "Desconocido": "#333333",
    }
    airports_df["elevation_name"] = airports_df["elevation_name"].fillna("Desconocido")
    airports_df["color"] = airports_df["elevation_name"].map(color)
    airports_df.rename(
        columns={"latitude_deg": "latitude", "longitude_deg": "longitude"}
    )

    mapa = json.load(open(GEOJSON_PATH, "r"))
    fig = go.Figure()

    fig.add_trace(
        go.Choropleth(
            geojson=mapa,
            featureidkey="properties.name",
            locations=[feature["properties"]["name"] for feature in mapa["features"]],
            z=[0] * len(mapa["features"]),
            colorscale=[[0, "rgba(0,0,0,0)"], [1, "rgba(0,0,0,0)"]],
            marker=dict(line=dict(width=1, color="grey")),
            showscale=False,
            hoverlabel=dict(namelength=0),
        )
    )

    fig.add_trace(
        go.Scattergeo(
            lon=airports_df["longitude_deg"],
            lat=airports_df["latitude_deg"],
            text=airports_df["name"],
            mode="markers",
            marker=dict(color=airports_df["color"], size=4),
            hoverlabel=dict(namelength=0),
        )
    )
    fig.add_trace(
        go.Scattergeo(
            lon=[None],
            lat=[None],
            mode="markers",
            marker=dict(size=10, color=color["bajo"]),
            legendgroup="bajo",
            showlegend=True,
            name="Bajo",
            hoverlabel=dict(namelength=0),
        )
    )
    fig.add_trace(
        go.Scattergeo(
            lon=[None],
            lat=[None],
            mode="markers",
            marker=dict(size=10, color=color["medio"]),
            legendgroup="Medio",
            showlegend=True,
            name="Medio",
            hoverlabel=dict(namelength=0),
        )
    )
    fig.add_trace(
        go.Scattergeo(
            lon=[None],
            lat=[None],
            mode="markers",
            marker=dict(size=10, color=color["altos"]),
            legendgroup="altos",
            showlegend=True,
            name="Alto",
            hoverlabel=dict(namelength=0),
        )
    )

    fig.update_layout(
        geo_scope="world",
        geo_bgcolor="rgba(0, 0, 0, 0)",
        geo=dict(
            scope="world",
            showcoastlines=True,
            coastlinecolor="black",
            showocean=True,
            oceancolor="#191a1a",
            lakecolor="#191a1a",
            landcolor="#343332",
            showland=True,
            showcountries=True,
            countrycolor="#646464",
            showsubunits=True,
            subunitcolor="Gray",
            projection_type="equirectangular",
            center=dict(lon=-60, lat=-40),
            projection_scale=4,
        ),
    )
    return fig


def air_map2(airports_df):
    """Generates a choropleth map of the number of airports per province in
    Argentina using Plotly.

    This function creates a choropleth map that shows the number of airports
    per province in Argentina.

    Args:
        airports_df (pd.DataFrame): DataFrame containing airport information.
        Must include the column 'region_name'.

    Returns:
        plotly.Figure: Plotly figure with the airport choropleth map.
    """
    mapa = json.load(open(GEOJSON_PATH, "r"))
    state_id_map = {}
    for feature in mapa["features"]:
        state_id_map[feature["properties"]["name"].strip()] = feature["id"]

    province_id_map = airports_df.groupby("region_name").size().reset_index(name="num")
    province_id_map["region_name"] = province_id_map["region_name"].apply(
        modules.replace_accented_letters
    )
    province_id_map["id"] = province_id_map["region_name"].apply(
        lambda x: state_id_map[x]
    )

    fig = px.choropleth(
        province_id_map,
        locations="id",
        geojson=mapa,
        color="num",
        hover_name="region_name",
        hover_data=["num"],
        color_continuous_scale=px.colors.sequential.Viridis_r,
        # color_continuous_midpoint=0,
    )
    fig.update_layout(
        geo_scope="world",
        geo_bgcolor="rgba(0, 0, 0, 0)",
        geo=dict(
            scope="world",
            showcoastlines=True,
            coastlinecolor="black",
            showocean=True,
            oceancolor="#191a1a",
            lakecolor="#191a1a",
            landcolor="#343332",
            showland=True,
            showcountries=True,
            countrycolor="#646464",
            showsubunits=True,
            subunitcolor="Gray",
            projection_type="equirectangular",
            center=dict(lon=-60, lat=-40),
            projection_scale=4,
        ),
    )
    fig.update_geos(fitbounds="locations", visible=True)
    return fig


def air_sunburst(airport_type_prov_df):
    """Generates a sunburst chart showing the distribution of airport types by
    province in Argentina using Plotly.

    Args:
        airport_type_prov_df (pd.DataFrame): DataFrame containing information
        on airport types and their locations. Must include the columns
        'region_name', 'type', and 'count'.

    Returns:
        plotly.Figure: Plotly figure with the sunburst chart.
    """
    fig = px.sunburst(
        airport_type_prov_df,
        path=["region_name", "type"],
        values="count",
        labels={
            "region_name": "Provincia",
            "type": "Tipo de Aeropuerto",
            "count": "Cantidad",
        },
    )
    fig.update_layout(uniformtext=dict(minsize=10, mode="hide"))
    fig.update_layout(margin=dict(t=21, l=10, r=10, b=10))
    return fig


def lake_map1(lakes_df):
    """Generates a map of lakes in Argentina using Plotly.

    This function creates a map of lakes in Argentina, showing their
    geographic locations on an interactive map.

    Args:
        lakes_df (pd.DataFrame): DataFrame containing lake information. Must
        include the columns 'Longitud', 'Latitud', and 'Nombre'.

    Returns:
        plotly.Figure: Plotly figure with the lake map.
    """
    mapa = json.load(open(GEOJSON_PATH, "r"))
    fig = go.Figure()
    fig.add_trace(
        go.Choropleth(
            geojson=mapa,
            featureidkey="properties.name",
            locations=[feature["properties"]["name"] for feature in mapa["features"]],
            z=[0] * len(mapa["features"]),
            colorscale=[[0, "rgba(0,0,0,0)"], [1, "rgba(0,0,0,0)"]],
            marker=dict(line=dict(width=1, color="grey")),
            showscale=False,
            hoverlabel=dict(namelength=0),
        )
    )

    fig.add_traces(
        go.Scattergeo(
            lon=lakes_df["Longitud"],
            lat=lakes_df["Latitud"],
            text=lakes_df["Nombre"],
            mode="markers",
            marker_color=random_colors,
            marker_size=7,
            hoverlabel=dict(namelength=0),
        )
    )

    fig.update_layout(
        showlegend=False,
        geo=dict(
            scope="world",
            showcoastlines=True,
            coastlinecolor="black",
            showocean=True,
            oceancolor="#191a1a",
            lakecolor="#191a1a",
            landcolor="#343332",
            showland=True,
            showcountries=True,
            countrycolor="#646464",
            showsubunits=True,
            subunitcolor="Gray",
            projection_type="equirectangular",
            center=dict(lon=-65, lat=-45),
            projection_scale=6.5,
        ),
    )
    return fig


def lake_map2(lakes_df):
    """Generates a choropleth map of the number of lakes per province in
    Argentina using Plotly.

    This function creates a choropleth map that shows the number of lakes per
    province in Argentina.

    Args:
        lakes_df (pd.DataFrame): DataFrame containing lake information. Must
        include the column 'Ubicación'.

    Returns:
        plotly.Figure: Plotly figure with the lake choropleth map.
    """
    mapa = json.load(open(GEOJSON_PATH, "r"))

    state_id_map = {
        feature["properties"]["name"].strip(): feature["id"]
        for feature in mapa["features"]
    }

    all_provinces_df = pd.DataFrame(
        list(state_id_map.items()), columns=["Ubicación", "id"]
    )
    province_id_map = lakes_df.groupby("Ubicación").size().reset_index(name="Num Lagos")
    province_id_map["Ubicación"] = province_id_map["Ubicación"].apply(
        modules.modify_province
    )
    province_id_map = pd.merge(
        all_provinces_df, province_id_map, on="Ubicación", how="left"
    ).fillna(0)

    fig = px.choropleth(
        province_id_map,
        locations="id",
        geojson=mapa,
        color="Num Lagos",
        hover_name="Ubicación",
        hover_data=["Num Lagos"],
        color_continuous_scale=px.colors.sequential.Viridis_r,
    )

    fig.update_layout(
        geo_scope="world",
        geo=dict(
            scope="world",
            showcoastlines=True,
            coastlinecolor="black",
            showocean=True,
            oceancolor="#191a1a",
            lakecolor="#191a1a",
            landcolor="#343332",
            showland=True,
            showcountries=True,
            countrycolor="#646464",
            showsubunits=True,
            subunitcolor="Gray",
            projection_type="equirectangular",
            center=dict(lon=-60, lat=-40),
            projection_scale=4,
        ),
    )
    fig.update_geos(fitbounds="locations", visible=True)
    return fig


def lake_grouped_bar_chart(lakes_df):
    """Generates a grouped bar chart showing characteristics of lakes in
    Argentina using Plotly.

    This function creates a grouped bar chart that shows different
    characteristics (surface area, maximum depth, and average depth) of lakes
    in Argentina.

    Args:
        lakes_df (pd.DataFrame): DataFrame containing lake information. Must
        include the columns 'Nombre', 'Superficie (km²)', 'Profundidad máxima
        (m)', and 'Profundidad media (m)'.

    Returns:
        plotly.Figure: Plotly figure with the grouped bar chart.
    """
    subset_df = lakes_df[
        [
            "Nombre",
            "Superficie (km²)",
            "Profundidad máxima (m)",
            "Profundidad media (m)",
        ]
    ]
    subset_df.set_index("Nombre", inplace=True)
    fig = go.Figure()
    # Le voy agregando barra por barra
    for column in subset_df.columns:
        fig.add_trace(go.Bar(x=subset_df.index, y=subset_df[column], name=column))
    fig.update_layout(
        xaxis_title="Nombre Lago",
        yaxis_title="Medida",
        barmode="group",
        legend=dict(title="Característica"),
    )
    return fig


def lake_grouped_bar_chart2(lakes_df):
    """Generates a grouped bar chart showing the distribution of lake sizes by
    province in Argentina using Plotly.

    This function creates a grouped bar chart that shows the distribution of
    lake sizes by province in Argentina.

    Args:
        lakes_df (pd.DataFrame): DataFrame containing lake information. Must
        include the columns 'Ubicación' and 'Sup tamaño'.

    Returns:
        plotly.Figure: Plotly figure with the grouped bar chart.
    """
    lake_dist = (
        lakes_df.groupby(["Ubicación", "Sup tamaño"]).size().unstack(fill_value=0)
    )
    # lake_dist.reset_index(inplace=True)
    fig = go.Figure()
    for i in lake_dist.columns:
        fig.add_trace(
            go.Bar(
                name=(i),
                x=(lake_dist.index),
                y=lake_dist[i],
            )
        )

    fig.update_layout(
        xaxis=dict(title="Provincia"),
        yaxis=dict(title="Cantidad de Lagos"),
        barmode="group",
    )
    return fig


CUSTOM_AIRPORTS = (
    modules.BASE_PATH.parent / ("datasets") / ("custom_datasets") / ("ar-airports.csv")
)
CUSTOM_LAKES = (
    modules.BASE_PATH.parent / ("datasets") / ("custom_datasets") / ("lagos_arg.csv")
)

st.markdown(
    """
    # Conociendo Nuestros Datos

    En esta sección, podrás explorar información sobre los conjuntos de datos utilizados como fuente para el juego. 
    Podrás elegir entre visualizar datos sobre `aeropuertos` o `lagos`, cada uno con sus propios gráficos, tablas y mapas.

    *Usa el selector a continuación para elegir el dataset que deseas visualizar*.
"""
)
# Menu para elegir info de que dataset visualizar
tipo_visualizacion = st.selectbox(
    "Selecciona el dataset a visualizar:",
    ("Aeropuertos", "Lagos"),
    index=None,
    placeholder="Elegir dataset",
)

if tipo_visualizacion == "Aeropuertos":
    airports_df = pd.read_csv(CUSTOM_AIRPORTS)
    airports_df["region_name"] = airports_df["region_name"].str.replace(" Province", "")
    type_change = {
        "large_airport": "Grande",
        "medium_airport": "Mediano",
        "small_airport": "Pequeño",
        "heliport": "Helipuerto",
        "closed": "Cerrado",
        "balloonport": "Balloonport",
    }
    # Cambio los valores de columna
    airports_df = airports_df.replace({"type": type_change}, regex=True)

    st.header("Aeropuertos en Argentina")
    st.markdown(
        "*Información obtenida de [OurAirports Argentina](https://data.humdata.org/dataset/ourairports-arg)*"
    )

    st.subheader("Mapa de Aeropuertos en Argentina")
    tab1, tab2 = st.tabs(
        ["Mapa según Elevación", "Mapa Coroplético de Aeropuertos por Provincia"]
    )

    with tab1:
        st.markdown(
            """
        Este mapa muestra la ubicación de los aeropuertos en Argentina, con puntos de diferentes colores según la elevación:
        - <span style="color: #b5d09c;">**Bajo**</span> : Elevación menor o igual a 40 mts.
        - <span style="color: #00bfff;">**Medio**</span>: Elevación mayor que 40 mts y menor o igual a 275 mts.
        - <span style="color: #c32148;">**Alto**</span> : Elevación mayor a 275 mts.
        """,
            unsafe_allow_html=True,
        )

        st.plotly_chart(air_map1(airports_df))
    with tab2:
        st.markdown(
            """
        Este mapa muestra la cantidad de aeropuertos en cada provincia de Argentina. La progresión del color representa el número de aeropuertos.
        """
        )
        st.plotly_chart(air_map2(airports_df))

    st.subheader("Cantidad de Aeropuertos por Provincia")
    st.markdown(
        """
        Estos gráficos permiten observar la distribución de aeropuertos a lo largo de Argentina, tanto en forma de porcentaje como en cantidad absoluta.
    """
    )
    tab1, tab2 = st.tabs(["Gráfico Circular", "Gráfico de Barras"])

    aeropuertos_por_provincia = airports_df["region_name"].value_counts()
    with tab1:
        fig = go.Figure(
            data=[
                go.Pie(
                    labels=aeropuertos_por_provincia.index,
                    values=aeropuertos_por_provincia,
                )
            ]
        )
        fig.update_traces(textinfo="label+percent")
        st.plotly_chart(fig)
    with tab2:
        fig = go.Figure(
            data=[
                go.Bar(x=aeropuertos_por_provincia.index, y=aeropuertos_por_provincia)
            ]
        )
        fig.update_xaxes(title_text="Provincia")
        fig.update_yaxes(title_text="Cantidad de Aeropuertos")
        st.plotly_chart(fig)

    st.subheader("Tipos de Aeropuertos")
    st.markdown(
        """
    Los aeropuertos se clasifican en diferentes tipos según su funcionalidad y tamaño. A continuación se describen los tipos de aeropuertos representados:
    - `Balloonport`: Área para despegue y aterrizaje de globos aerostáticos.
    - `Cerrado`: Aeropuertos cerrados, fuera de operación.
    - `Helipuerto`: Pista de aterrizaje para helicópteros.
    - `Grande`: Grandes aeropuertos con infraestructura y tráfico significativos, incluyendo vuelos internacionales.
    - `Mediano`: Aeropuertos medianos con tráfico moderado, generalmente doméstico y regional.
    - `Pequeño`: Aeropuertos pequeños con menos infraestructura, usados para vuelos privados y aviación general.
    """
    )

    st.subheader("Distribución Total de Tipos de Aeropuertos")
    aeropuertos_por_type = airports_df["type"].value_counts().reset_index(name="count")
    tab1, tab2 = st.tabs(["Gráfico de Barras", "Gráfico Circular"])
    with tab1:
        # Gráfico de barras
        fig_bar = px.bar(
            aeropuertos_por_type,
            x="type",
            y="count",
            labels={"type": "Tipo de Aeropuerto", "count": "Cantidad"},
            color="type",
        )
        st.plotly_chart(fig_bar)
    with tab2:
        # Gráfico circular
        fig_pie = go.Figure(
            go.Pie(
                labels=aeropuertos_por_type["type"],
                values=aeropuertos_por_type["count"],
                hoverinfo="label+value",
                textinfo="percent",
            )
        )
        st.plotly_chart(fig_pie)

    st.subheader("Distribucion de tipos de aeropuertos segun provincias: ")
    tab1, tab2 = st.tabs(["Gráfico de barras agrupadas", "Gráfico Sunburst"])
    airport_type_prov = airports_df.groupby(["region_name", "type"])["type"].count()
    airport_type_prov_df = airport_type_prov.reset_index(name="count")
    with tab1:
        # Grouped bar chart - Tamaño de aeropuertos en cada provincia
        fig = px.bar(
            airport_type_prov_df,
            x="region_name",
            y="count",
            color="type",
            labels={"region_name": "Provincia", "type": "Tipo"},
            barmode="group",
        )
        st.plotly_chart(fig)
    with tab2:
        # Sunburst chart
        st.plotly_chart(air_sunburst(airport_type_prov_df))

elif tipo_visualizacion == "Lagos":
    lakes_df = pd.read_csv(CUSTOM_LAKES)
    # Color random a los puntos
    import numpy as np

    c = np.random.randint(0, len(px.colors.qualitative.Plotly), len(lakes_df))
    random_colors = [px.colors.qualitative.Plotly[i] for i in c]
    st.header("Lagos en Argentina")
    st.markdown(
        """*Información obtenida de [Atlas Hidrográfico de Argentina](https://datos.hidro.gob.ar/)*"""
    )

    st.subheader("Mapa de Lagos en Argentina")
    tab1, tab2 = st.tabs(["Mapa coordenadas", "Mapa coroplético lagos por provincia"])
    with tab1:
        st.markdown(
            """
        Mapa que muestra los lagos segun sus cordenadas, con puntos de diferentes colores.
"""
        )
        st.plotly_chart(lake_map1(lakes_df))
    with tab2:
        st.markdown(
            """
        Este mapa muestra la cantidad de lagos en cada provincia de Argentina. La progresión del color representa el número de lagos.
        """
        )
        st.plotly_chart(lake_map2(lakes_df))

    st.subheader("Cantidad de Lagos por Provincia")
    st.markdown(
        """
        Este gráfico permiten observar la distribución de lagos a lo largo de Argentina.
    """
    )
    lagos_por_provincia = (
        lakes_df["Ubicación"].apply(modules.modify_province).value_counts()
    )

    # Bar Chart, cantidad de lagos por provincia
    fig = go.Figure(data=[go.Bar(x=lagos_por_provincia.index, y=lagos_por_provincia)])
    fig.update_xaxes(title_text="Provincia")
    fig.update_yaxes(title_text="Cantidad de Lagos")
    st.plotly_chart(fig)

    st.subheader("Profundidades y superficie de lagos")
    # Grouped Bar Chart - Lago-ProfMax-ProfMedia
    st.plotly_chart(lake_grouped_bar_chart(lakes_df))

    st.subheader("Distribucion de los lagos segun tamaño")
    st.markdown(
        """
        - Teniendo en cuenta la superficie de cada lago se determinó:
            - `Chico` : lagos con una superficie menor o igual a 17 km².
            - `Medio` : lagos con una superficie mayor que 17 km² y menor o igual a 59 km².
            - `Grande`: lagos con una superficie mayor a 59 km².
"""
    )
    tab1, tab2 = st.tabs(["General", "Por provincia"])
    with tab1:
        # PieChart
        lake_size = lakes_df["Sup tamaño"].value_counts()
        fig = px.pie(lake_size, values=lake_size.values, names=lake_size.index)
        st.plotly_chart(fig)

    with tab2:
        fig = lake_grouped_bar_chart2(lakes_df)
        st.plotly_chart(fig)
