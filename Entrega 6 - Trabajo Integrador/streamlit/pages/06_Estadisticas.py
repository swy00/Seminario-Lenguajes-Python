import streamlit as st
import pandas as pd
from pathlib import Path
import json
import matplotlib.pyplot as plt
import datetime as dt
import plotly.express as px
import plotly.graph_objects as go
import calendar
import modules
import estadisticas

st.set_page_config(
    page_title="PyTrivia",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="auto",
)
file_user_score = modules.BASE_PATH / "data" / "user_score.json"
file_user_data = modules.BASE_PATH / "data" / "user_data.json"

st.header("Bienvenidos a la sección de estadísticas")
st.subheader("Seleccione la estadística que desea ver")
selector = st.selectbox(
    "Estadística",
    [
        "",
        "Genero",
        "Superior al promedio",
        "Partidas por día de semana",
        "Preguntas acertadas mensualmente",
        "Top 10 entre dos fechas",
        "Dificultad de los datasets",
        "Comparar usuarios historicamente",
        "Listado mejor tema por genero",
        "Información de cada dificultad",
        "Usuarios en racha",
    ],
)

df_score = pd.read_json(file_user_score)
df_user_data = pd.read_json(file_user_data)
df_score.rename(
    columns={"Respuesta correctas": "RespuestasCorrectas", "Fecha y hora": "Fecha"},
    inplace=True,
)

match selector:
    case "Genero":
        """
        1. Gráfico de torta de usuarios que hayan jugado alguna vez el juego agrupados por género.
        """
        estadisticas.estadistica_1(df_user_data, df_score)
    case "Superior al promedio":
        """
        2. Gráfico de torta con porcentaje de partidas que tienen una puntuación superior a la media (promedio de calificaciones).
        """
        estadisticas.estadistica_2(df_score)
    case "Partidas por día de semana":
        """
       3. Promedio de preguntas acertadas mensuales entre un rango de dos fechas insertadas en dos inputs. 
        """
        fig_bar = estadisticas.estadistica_3(df_score)
        st.plotly_chart(fig_bar)
    case "Preguntas acertadas mensualmente":
        """
        4. Promedio de preguntas acertadas mensuales entre un rango de dos fechas insertadas en dos inputs.
        """
        fig_bar = estadisticas.estadistica_4(df_score)
    case "Top 10 entre dos fechas":
        """
        5. Top 10 de usuarios con mayor cantidad de puntos acumulados entre un rango de dos fechas insertadas por input
        """
        estadisticas.estadistica_5(df_score)
    case "Dificultad de los datasets":
        """
        6. Ordenar los datasets por dificultad donde primero se debe ubicar el dataset que tiene mayor número de errores en las respuestas.
        """
        estadisticas.estadistica_6(df_score)

    case "Comparar usuarios historicamente":
        """
        7. Gráfico de líneas que permita seleccionar dos usuarios para compararlos. Al seleccionarlos se debe mostrar la evolución de su puntaje a lo largo del tiempo.
        """
        estadisticas.estadistica_7(df_user_data, df_score)

    case "Listado mejor tema por genero":
        """
        8. Listar para cada género cuál es la temática en la cual demuestra mayor conocimiento.
        """
        estadisticas.estadistica_8(df_user_data, df_score)
    case "Información de cada dificultad":
        """
        9. Listar cada dificultad de juego junto con el puntaje promedio obtenido en cada una y con la cantidad de veces que fue elegida.
        """
        estadisticas.estadistica_9(df_score)
       
    case "Usuarios en racha":
        """
        10. Listado de usuarios en racha. Lista los usuarios que registran una partida con un puntaje mayor a cero en todos los días durante los últimos 7 días.
        """
        estadisticas.estadistica_10(df_score)
