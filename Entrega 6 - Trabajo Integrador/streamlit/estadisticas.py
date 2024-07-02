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

def estadistica_1(df_user_data, df_score):
    """This function generate a pie graph with a percentage of the amount of players by their gender

    Args:
        df_user_data (pd.DataFrame): Dataframe with all users information
        df_score (pd.DataFrame): Dataframe with all the scores in the game
    """
    st.title("Proporcion de jugadores por género")
    conteo_genero = df_user_data[df_user_data.Mail.isin(df_score.Mail)]
    cant_gender = conteo_genero.Género.value_counts()
    plt.pie(cant_gender.values, labels=cant_gender.index, autopct="%1.1f%%")
    st.pyplot(plt)

def estadistica_2(df_score):
    """This function generate a pie graph with the percetage of scores bigger than the mean

    Args:
        df_score (pd.DataFrame): Dataframe with all the scores in the game
    """
    st.title("Proporcion de partidas con puntaje superior al promedio")
    scores = df_score.Puntaje
    prom_score = df_score.Puntaje.mean()
    score_count = [0, 0]
    for score in scores:
        if score > prom_score:
            score_count[0] += 1
        else:
            score_count[1] += 1
    bigger_score = [
        "Puntajes mayores al promedio",
        "Puntajes iguales o menores al promedio",
        ]
    plt.pie(score_count, labels=bigger_score, autopct="%1.1f%%")
    st.pyplot(plt)

def estadistica_3(df_score):
    """This function generate a bar graph with the amount of games played for each day and return the bar graph

    Args:
        df_score (pd.DataFrame): Dataframe with all the scores in the game

    Returns:
        fig_bar: go.Figure created with the data processed
    """
    partidas = df_score["Fecha"].copy()
    dias = []
    for game in partidas.values:
        game = dt.datetime.strptime(game, "%Y-%m-%d %H:%M:%S")
        dias.append(calendar.day_name[game.weekday()])
    dias_df = pd.DataFrame(dict(DiaSemana=dias))
    dias = dias_df.groupby("DiaSemana").nunique()
    games = dias_df.groupby("DiaSemana").DiaSemana.count()
    fig_bar = go.Figure(
        data=[go.Bar(x=dias.index, y=games)],
        layout=go.Layout(
            title=go.layout.Title(text="Cantidad de partidas jugados por dia de semana")
            ),
        )
    return fig_bar

def estadistica_4(df_score):
    """This function show a bar graph with the mean of right answers in the months inputed by the user

    Args:
        df_score (pd.DataFrame): Dataframe with all the scores in the game
    """
    fecha_1 = st.date_input(
            "Ingrese la primer fecha",
            value=None,
            min_value=dt.datetime.today() - dt.timedelta(days=36500),
            max_value=dt.datetime.today() - dt.timedelta(days=31),
            format="DD/MM/YYYY",
        )
    if fecha_1:
            fecha_1 = dt.datetime.combine(fecha_1, dt.datetime.min.time())
            fecha_2 = st.date_input(
                "Ingrese la segunda fecha",
                value=None,
                min_value=fecha_1 + dt.timedelta(days=31),
                max_value=dt.datetime.today(),
                format="DD/MM/YYYY",
            )
            if fecha_2:
                fecha_2 = dt.datetime.combine(fecha_2, dt.datetime.max.time())
                fechas = list(
                    filter(
                        lambda fecha: dt.datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S") > fecha_1
                        and fecha_2 > dt.datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S"),
                        list(df_score.Fecha.values),
                    )
                )
                fechas_df_score = df_score[df_score.Fecha.isin(fechas)]
                fechas_df_score["Mes"] = fechas_df_score["Fecha"].apply(
                    lambda x: calendar.month_name[
                        dt.datetime.strptime(x, "%Y-%m-%d %H:%M:%S").month
                    ]
                )
                prom_answers = fechas_df_score.groupby("Mes").RespuestasCorrectas.mean()
                fig_bar = go.Figure(
                    data=[go.Bar(x=prom_answers.index, y=prom_answers.values)],
                    layout=go.Layout(title=go.layout.Title(text="Promedio de respuestas correctas por mes")
                    ),
                )
                st.plotly_chart(fig_bar)

def estadistica_5(df_score):
    """This function show the TOP 10 users with most points between two dates

    Args:
        df_score (pd.DataFrame): Dataframe with all the scores in the game
    """
    df = modules.rank()
    fecha_1 = st.date_input(
            "Ingrese la primer fecha",
            value=None,
            min_value=dt.datetime.today() - dt.timedelta(days=36500),
            max_value=dt.datetime.today() - dt.timedelta(days=1),
            format="DD/MM/YYYY",
        )
    if fecha_1:
            fecha_1 = dt.datetime.combine(fecha_1, dt.datetime.min.time())
            fecha_2 = st.date_input(
                "Ingrese la segunda fecha",
                value=None,
                min_value=fecha_1 + dt.timedelta(days=1),
                max_value=dt.datetime.today(),
                format="DD/MM/YYYY",
            )
            if fecha_2:
                fecha_2 = dt.datetime.combine(fecha_2, dt.datetime.max.time())
                fechas = list(
                    filter(
                        lambda fecha: dt.datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S")
                        > fecha_1
                        and fecha_2 > dt.datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S"),
                        list(df_score.Fecha.values),
                    )
                )
                fechas_df_score = df_score[df_score.Fecha.isin(fechas)]
                users_in_range = (
                    fechas_df_score.groupby("Mail")
                    .Puntaje.sum()
                    .sort_values(ascending=False)
                )
                st.title("Top 10 con más puntos acumulados")
                st.dataframe(users_in_range[:10], width=1000)

def estadistica_6(df_score):
    """This function shows a line chart comparing the score progression of two users.

    Args:
        df_score (pd.DataFrame): Dataframe with all the scores in the game
    """
    reduced_df_score = df_score[["Tema", "RespuestasCorrectas"]]
    reduced_df_score["RespuestasIncorrectas"] = reduced_df_score[
            "RespuestasCorrectas"
        ].apply(lambda score: 5 - score)
    datasets_diffs = (
            reduced_df_score.groupby("Tema")
            .RespuestasIncorrectas.mean()
            .sort_values(ascending=False)
        )
    st.title("Datasets ordenados por dificultad")
    st.dataframe(datasets_diffs, width=1000)

def estadistica_7(df_user_data, df_score):
    users = df_user_data["Mail"].values
    user_1 = st.selectbox(
            "Seleccione un usuario",
            options=sorted(users),
            placeholder="Elija el usuario que desea comparar",
            index=None
        )
    user_2 = st.selectbox(
            "Seleccione otro usuario",
            options=sorted(users),
            placeholder="Elija el usuario que desea comparar",
            index=None
        )
    if user_1 and user_2:
            df_scores_users = df_score[
                (df_score["Mail"].values == user_1)
                | (df_score["Mail"].values == user_2)
            ].sort_values(by=['Fecha'])
            fig = px.line(df_scores_users, x="Fecha", y="Puntaje", color="Mail")
            st.plotly_chart(fig)

def gender_best(gender, gender_theme):
    """This function search for a gender the best 'Tema' searching for the mean of rigth answers

    Args:
        gender (str): gender of the player (M, F, X)
        gender_theme (pd.DataFrame): DataFrame reduced with the genders, right answers and category

    Returns:
        best : pd.Series with the best category of the gender
    """
    best = (
         gender_theme[gender_theme['Género'] == gender]
         .groupby('Tema')
         .RespuestasCorrectas.mean()
         .sort_values(ascending=False)
         .head(1)
            )
    return best

def estadistica_8(df_user_data, df_score):
    """This function shows a list of the best category for each gender

    Args:
        df_user_data (pd.DataFrame): Dataframe with all users information
        df_score (pd.DataFrame): Dataframe with all the scores in the game
    """
    gender_tuple = 'Masculino', 'Femenino', 'No Binarix'
    gender_theme = pd.merge(df_user_data, df_score)
    gender_theme = gender_theme[["Género", "RespuestasCorrectas", "Tema"]]
    m_best = gender_best('M', gender_theme)
    f_best = gender_best('F', gender_theme)
    x_best = gender_best('X', gender_theme)
    genders_best = pd.DataFrame(
            index=gender_tuple,
            data=(m_best.keys(), f_best.keys(), x_best.keys()),
            columns=["Tema"],
        )
    st.title("¿En qué tema es mejor cada género?")
    st.dataframe(genders_best, width=1000)

def estadistica_9(df_score):
    """This function show info about the difficulties of the game

    Args:
        df_score (pd.DataFrame): Dataframe with all the scores in the game

    """
    index_diff = df_score.Dificultad.unique()
    mean_by_diff = df_score.groupby("Dificultad").Puntaje.mean().values
    count_diff_pick = df_score.Dificultad.value_counts().values
    data_per_diff = {
            "PuntajePromedio": mean_by_diff,
            "VecesElegida": count_diff_pick,
        }
    df_diff = pd.DataFrame(
            index=index_diff,
            data=data_per_diff,
            columns=["PuntajePromedio", "VecesElegida"],
        )
    st.dataframe(df_diff, width=1000)
    mean_bar_fig = go.Figure(
            go.Bar(x=index_diff, y=df_diff.PuntajePromedio),
            layout=go.Layout(
                title=go.layout.Title(text="Puntaje promedio por dificultad")
            ),
        )
    st.plotly_chart(mean_bar_fig)
    pick_bar_fig = go.Figure(
            go.Bar(x=index_diff, y=df_diff.VecesElegida),
            layout=go.Layout(
                title=go.layout.Title(
                    text="Cantidad de veces que se eligio cada dificultad"
                )
            ),
        )
    st.plotly_chart(pick_bar_fig)

def estadistica_10(df_score):
    """This function show a list of users who has an streak of seven days played with an score bigger than 0

    Args:
        df_score (pd.DataFrame): Dataframe with all the scores in the game
    """
    df_reduced = df_score[["Fecha", "Puntaje", "Mail"]]
    df_reduced["Fecha"] = pd.to_datetime(df_reduced["Fecha"]).dt.date
    a_week_ago = dt.date.today() - dt.timedelta(days=7)
    df_reduced = df_reduced[
            (df_reduced.Fecha > a_week_ago) & (df_reduced.Puntaje > 0)
        ]

        # Group DF by mail and date
    new_df = (
            df_reduced.groupby(["Mail", "Fecha"])
            .size()
            .reset_index(name="Cant_partidas")
        )

        # An user in on streak if days = 7
    streak_users = (
            new_df.groupby("Mail")
            .filter(lambda x: x["Cant_partidas"].count() == 7)["Mail"]
            .unique()
        )
    st.text("Jugadores en racha: ")
    for player in streak_users:
            st.text(f"- {player}")

    new_df = new_df[new_df.Mail.isin(streak_users)]
    st.dataframe(new_df, width=1000)