import streamlit as st
import pathlib
import json
import os
import datetime as dt
import random
import csv
import pandas as pd
import numpy as np
import modules
import time

st.set_page_config(
    page_title="PyTrivia",
    page_icon="🕹️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

DB_SET = ("Aeropuertos", "Lagos", "Conectividad", "Censo 2022")
DIFFICULTY_SET = ("Alta", "Media", "Fácil")
QUESTION_TOTAL = 5
SESSION = st.session_state
STYLE01_PATH = modules.BASE_PATH / "styles" / "style01.css"
with open(STYLE01_PATH) as f:
    css = f.read()
css = f"<style>{css}</style>"
st.markdown(css, unsafe_allow_html=True)


def easy_mode():
    """
    Generates and returns multiple-choice options for the current question in easy mode.

    This function retrieves the correct answer for the current question from the session and
    selects additional unique incorrect answers from the current dataframe to create a list of
    multiple-choice options.

    Returns:
        list: A list of answer options including the correct answer, randomly shuffled.
    """
    sol = SESSION.questions[f"question{SESSION.questions['question_counter']}"][
        "info3"
    ]["right_answer"]
    col = SESSION.questions[f"question{SESSION.questions['question_counter']}"][
        "info3"
    ]["question"]

    o_col = SESSION.questions[f"question{SESSION.questions['question_counter']}"][
        "info2"
    ]["question"]
    o_val = SESSION.questions[f"question{SESSION.questions['question_counter']}"][
        "info2"
    ]["right_answer"]
    # Busco las otras opciones para mostrar
    if (
        f"options_{SESSION.questions['question_counter']}"
        not in SESSION["easy_mode_options"]
    ):
        opt_df = SESSION["current_df"]
        try:
            answers_options = (
                opt_df[col][
                    (opt_df[col] != sol)
                    & (opt_df[col].notna())
                    & (opt_df[o_col] != o_val)
                ]
                .drop_duplicates()
                .sample(n=2, random_state=1)
                .tolist()
            )
        except:
            answers_options = (
                opt_df[col][
                    (opt_df[col] != sol)
                    & (opt_df[col].notna())
                    & (opt_df[o_col] != o_val)
                ]
                .drop_duplicates()
                .sample(n=1, random_state=1)
                .tolist()
            )
        answers_options.append(sol)
        random.shuffle(answers_options)
        SESSION["easy_mode_options"][
            f"options_{SESSION.questions['question_counter']}"
        ] = answers_options
        return answers_options
    else:
        return SESSION["easy_mode_options"][
            f"options_{SESSION.questions['question_counter']}"
        ]


def medium_mode(ans):
    """
    Provides a hint for the current question in medium mode.

    This function displays a hint based on the type and length of the correct answer.

    Args:
        ans (str or int or float): The correct answer to the current question.

    Returns:
        str or int or float: The user's input, converted to the appropriate type if possible.
    """
    if isinstance(ans, str):
        # Si `ans` es una cadena
        ans_len = len(ans.replace(" ", ""))
        ayuda = "".join(["-" if i != " " else " " for i in ans])
        st.write(f"Ayuda: {ayuda} ({ans_len})")
    else:
        # Si `ans` es un número, proporciona otra ayuda
        if isinstance(ans, (int, np.integer)):
            st.write(f"Ayuda: La respuesta tiene {len(str(ans))} dígitos")
        elif isinstance(ans, (float, np.floating)):
            ans_str = str(ans)
            entero, decimal = ans_str.split(".")
            ayuda = (
                f"{''.join(['-' for _ in entero])}.{''.join(['-' for _ in decimal])}"
            )
            st.write(
                f"Ayuda: La respuesta tiene {len(entero)} dígitos en la parte entera y {len(decimal)} dígitos en la parte decimal"
            )
            st.write(f"Ayuda: {ayuda}")

    answer = st.text_input(
        f"Respuesta {SESSION.questions['question_counter']+1}",
        placeholder=f"Ingrese la respuesta {SESSION.questions['question_counter']+1}",
    )
    try:
        if "." in answer:
            answer = float(answer)
        else:
            answer = int(answer)
        return answer
    except ValueError:
        return answer.title()


def hard_mode(answer):
    """
    Converts the user's answer input to the appropriate type for the current question in hard mode.

    Args:
        answer (str): The user's answer input.

    Returns:
        str or int or float: The user's answer, converted to the appropriate type.
    """
    try:
        if "." in answer:
            answer = float(answer)
        else:
            answer = int(answer)
        return answer
    except ValueError:
        return answer.title()


if "game_state" not in SESSION:
    SESSION["game_state"] = {
        "state": "NOT_CREATED",
        "username": None,
        "difficulty": None,
        "subject": None,
        "correct": 0,
        "score": 0,
        "date": None,
    }
if "animation_shown" not in SESSION:
    SESSION["animation_shown"] = False

if SESSION.game_state["state"] == "NOT_CREATED":
    read_data = modules.BASE_PATH / ("data") / ("user_data.json")
    with read_data.open(mode="r", encoding="utf-8") as read_file:
        data_load = json.load(read_file)
        user = map(lambda y: y["Mail"], data_load)
    st.header("Bienvenido a Pytrivia!!")
    st.subheader("Para comenzar la trivia seleccione el usuario")

    player_data = st.empty()
    with player_data.form("registration"):
        # La persona que ingresa al sistema selecciona el usuario que le corresponda.
        username = st.text_input("Usuario", placeholder="Ingrese el e-mail del usuario")
        # El usuario selecciona una temática de 4 posibles
        subject = st.selectbox("Temática", DB_SET)
        # El usuario selecciona una de 3 dificultades: Fácil, Media, Alta
        difficulty = st.selectbox("Dificultad", DIFFICULTY_SET)
        start = st.form_submit_button("Iniciar juego")
    
    col1, col2 = st.columns([0.7,1])
    with col1:
        st.markdown("Si es la primera vez que jugás, no olvides")
    with col2:
        register = st.button("registrarte ✍️")
    if register:
        st.switch_page("pages/04_Formulario_de_registro.py")
    if start:
        if username not in user: 
            st.markdown(
                    f"<div class='user-answer'> ⚠ El usuario ingresado no se encuentra registrado </div>",
                    unsafe_allow_html=True,
                )  
        else:
            SESSION.game_state["state"] = "NEW_QUESTION"
            SESSION.game_state["username"] = username
            SESSION.game_state["difficulty"] = difficulty
            SESSION.game_state["subject"] = subject
            SESSION["easy_mode_options"] = {}
            st.rerun()

elif SESSION.game_state["state"] == "NEW_QUESTION":
    SESSION.game_state["state"] = "NEW_ANSWER"
    if "questions" not in SESSION:
        SESSION["questions"] = {f"question{i}" : {} for i in range(QUESTION_TOTAL)}
        SESSION["questions"]["question_counter"] = 0
    st.header(f"Comenzando la trivia para el usuario")
    st.subheader(f"Usuario: {SESSION.game_state['username']}")
    st.subheader(f"Dificultad: {SESSION.game_state['difficulty']}")
    st.subheader(f"Temática: {SESSION.game_state['subject']}")
    ph = st.empty()
    for secs in range(5, 0, -1):
        ph.markdown(
            f"<div class='counter-circle'><div class='counter'>{secs:01d}</div></div>",
            unsafe_allow_html=True,
        )
        time.sleep(0.5)
    # Se debe considerar mostrar atributos que realmente ayuden al usuario a responder
    read_data = (
        modules.BASE_PATH
        / ("data")
        / ("datasets")
        / modules.selected_dataset(SESSION.game_state["subject"])
    )
    selected_df = pd.read_csv(read_data)
    # Guardo el dataframe en el session state para uso posterior
    SESSION["current_df"] = selected_df
    # La premisa básica es que, al iniciar el juego, se generará de manera aleatoria una lista de 5 preguntas para responder
    row_sample = pd.DataFrame.sample(selected_df, n=QUESTION_TOTAL)
    # En cada pregunta al usuario se le muestran 3 atributos de un lugar y debe responder cuál es el cuarto atributo
    # Se valora si para una misma partida el atributo a descubrir no es siempre el mismo para todas las preguntas.
    for i in range(len(row_sample)):
        SESSION.questions[f"question{i}"] = modules.set_questions(
            row_sample.iloc[i], list(row_sample.columns)[1:]
        )
    st.rerun()

elif SESSION.game_state["state"] == "NEW_ANSWER":
    game_data = st.empty()
    with game_data.form("trivia"):
        # En cada pregunta al usuario se le muestran 3 atributos de un lugar y debe responder cuál es el cuarto atributo
        modules.get_questions(
            SESSION.questions[f"question{SESSION.questions['question_counter']}"],
            SESSION.questions["question_counter"],
        )
        match (SESSION["game_state"]["difficulty"]):
            # Dificultad alta: no se brindan ayudas.
            case "Alta":
                answer = st.text_input(
                    f"Respuesta {SESSION.questions['question_counter']+1}",
                    placeholder=f"Ingrese la respuesta {SESSION.questions['question_counter']+1}",
                )
                # Formateo la respuesta que ingrese
                answer = hard_mode(answer)
            # Dificultad media: se le informa la cantidad de palabras de la respuesta.
            case "Media":
                answer = SESSION.questions[
                    f"question{SESSION.questions['question_counter']}"
                ]["info3"]["right_answer"]

                answer = medium_mode(answer)
            # Dificultad fácil: se le brindan tres respuestas de las cuales una es la correcta.
            case "Fácil":
                answers_options = easy_mode()
                answer = st.radio("Indique la respuesta", answers_options)

        finish = st.form_submit_button("Responder")
        # Barra Progreso
        progress = (SESSION.questions["question_counter"] + 1) / QUESTION_TOTAL * 100
        st.markdown(
            f"""
            <div class='progress-bar'>
                <div style="width: {progress}%; 
                    background-color: #76c7c0; 
                    height: 15px; 
                    border-radius: 25px; 
                    transition: width 0.3s ease;
                    align-items:center">
                </div>
            </div>""",
            unsafe_allow_html=True,
        )

    if finish:
        SESSION.questions["question_counter"] += 1
        SESSION.game_state["state"] = "SCORE"
        if "answers" not in SESSION:
            SESSION["answers"] = {f"answer {i}": None for i in range(QUESTION_TOTAL)}
        SESSION.answers[f"answer{SESSION.questions['question_counter']-1}"] = answer
        st.rerun()

elif SESSION.game_state["state"] == "SCORE":
    # El usuario responderá a las 5 preguntas y luego de ello se pasará a la página de ranking (P5) donde se podrá ver el ranking de mejores resultados
    # (con la información del usuario de cada resultado), el resultado de la partida jugada y las preguntas junto a su respuesta correcta.
    if SESSION.questions["question_counter"] == QUESTION_TOTAL:
        selected_df = SESSION["current_df"]
        # Considerar que dados 3 atributos puede existir más de una respuesta correcta
        # Cargo del session state el DataSet usado y compruebo si las preguntas tenian multiples respuestas, y veo si el usuario adivinó o no
        for i in range(0, QUESTION_TOTAL):
            df = {}
            df[i] = selected_df[
                (
                    selected_df[SESSION.questions[f"question{i}"]["info0"]["question"]]
                    == SESSION.questions[f"question{i}"]["info0"]["right_answer"]
                )
                & (
                    selected_df[SESSION.questions[f"question{i}"]["info1"]["question"]]
                    == SESSION.questions[f"question{i}"]["info1"]["right_answer"]
                )
                & (
                    selected_df[SESSION.questions[f"question{i}"]["info2"]["question"]]
                    == SESSION.questions[f"question{i}"]["info2"]["right_answer"]
                )
            ]

            SESSION.questions[f"question{i}"]["info3"]["right_answer"] = list(
                set(df[i][SESSION.questions[f"question{i}"]["info3"]["question"]])
            )
            asd = SESSION.questions[f"question{i}"]["info3"]["right_answer"]
            # Para obtener el resultado de una partida se debe sumar un punto por respuesta correcta (las incorrectas no restan ni suman).
            if (
                SESSION.answers[f"answer{i}"]
                in SESSION.questions[f"question{i}"]["info3"]["right_answer"]
            ):
                SESSION.game_state["correct"] += 1

        # La dificultad NO solo establece las ayudas que recibirá el usuario al momento de jugar. También afecta el cálculo de puntaje de una partida:
        match SESSION.game_state["difficulty"]:
            # Al resultado de un partida con dificultad baja no se le de aplicar ningún cambio.
            case "Fácil":
                SESSION.game_state["score"] = SESSION.game_state["correct"]
            # Al resultado de una partida con dificultad media se le debe sumar un 50%.
            case "Media":
                SESSION.game_state["score"] = SESSION.game_state["correct"] * 1.5
            # Al resultado de una partida con dificultad alta se le debe sumar un 100%.
            case "Alta":
                SESSION.game_state["score"] = SESSION.game_state["correct"] * 2
        user_score_path = modules.BASE_PATH / ("data") / ("user_score.json")
        # Se debe almacenar en un archivo (formato y organización a elección de cada grupo) la información de cada partida. Es de interés conocer al menos:
        user_and_score = {
            # Usuario: identificador del usuario (mail)
            "Mail": SESSION.game_state["username"],
            # Cantidad de respuestas correctas
            "Respuesta correctas": SESSION.game_state["correct"],
            "Puntaje": SESSION.game_state["score"],
            # Fecha y hora: momento en el cual se responde la trivia.
            "Fecha y hora": dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            # Dificultad: dificultad elegida por el usuario
            "Dificultad": SESSION.game_state["difficulty"],
            # Temática: temática elegida por el usuario
            "Tema": SESSION.game_state["subject"],
        }
        SESSION.game_state["Date"] = user_and_score["Fecha y hora"]
        if os.stat(user_score_path).st_size > 0:
            df_existente = pd.read_json(user_score_path, convert_dates=["Date"])
        else:
            df_existente = pd.DataFrame()

        df_nuevo = pd.DataFrame.from_dict([user_and_score])
        df_combinado = pd.concat([df_existente, df_nuevo], ignore_index=True)
        df_combinado.to_json(
            user_score_path, orient="records", indent=4, date_format="iso"
        )
        SESSION.game_state["state"] = "SCOREBOARD"
    else:
        SESSION.game_state["state"] = "NEW_ANSWER"
    st.rerun()

    # Ranking Otra forma de llegar es luego de haber terminado una partida, en este caso además del ranking de mejores resultados se debe mostrar el resultado de la partida:

elif SESSION.game_state["state"] == "SCOREBOARD":

    st.header("Finalizó su partida")
    # Cantidad de preguntas respondidas correctamente.
    st.text(
        f"{SESSION.game_state['correct']} respuestas correcta de {SESSION.questions['question_counter']}"
    )
    # Puntaje de la partida.
    st.text(f"Resultado final de {SESSION.game_state['score']} punto/s")
    # Posición en el ranking.
    rank_df = modules.rank()
    info_partida = rank_df.loc[rank_df["Fecha y hora"] == SESSION.game_state["Date"]]
    # Animacion de 5 correctas o rank 1
    if not SESSION["animation_shown"]:
        if info_partida["Puesto"].tolist()[0] == 1:
            modules.emoji_rain(
                "🏆", falling_speed=3, animation_length=1, emoji_count=50, max_delay=4
            )
        elif SESSION.game_state["correct"] == SESSION.questions["question_counter"]:
            st.toast("Felicidades!", icon="🎉")
            time.sleep(0.5)
            st.toast("Respondiste correctamente todas las preguntas!", icon="5️⃣")
            st.balloons()
        SESSION["animation_shown"] = True
    st.text(
        f"Su posición en el ranking historico es posicion { info_partida['Puesto'].tolist()[0]} "
    )
    # Preguntas de la partida en conjunto con la respuesta correcta y la respuesta del usuario.
    for i in range(0, QUESTION_TOTAL):
        with st.container():
            st.title(f"Respuesta {i + 1}")
            for j in range(0, 3):
                st.text(
                    f"{SESSION.questions[f'question{i}'][f'info{j}']['question']}: {SESSION.questions[f'question{i}'][f'info{j}']['right_answer']}"
                )
            st.text(
                f"Respuesta correcta para: {SESSION.questions[f'question{i}']['info3']['question']}"
            )
            if len(SESSION.questions[f"question{i}"]["info3"]["right_answer"]) > 1:
                correct_answers_html = " ".join(
                    f"<div class='correct-answer' style='display:inline-block; margin-right: 10px;'>{right_answer}</div>"
                    for right_answer in SESSION.questions[f"question{i}"]["info3"][
                        "right_answer"
                    ]
                )
                st.markdown(
                    f'<div class="scrollable-container">{correct_answers_html}</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"<div class='correct-answer'>{SESSION.questions[f'question{i}']['info3']['right_answer'][0]}</div>",
                    unsafe_allow_html=True,
                )
            if (
                SESSION.answers[f"answer{i}"]
                not in SESSION.questions[f"question{i}"]["info3"]["right_answer"]
            ):
                st.markdown(
                    f"<div class='user-answer'> Respuesta del usuario: {SESSION.answers[f'answer{i}']}</div>",
                    unsafe_allow_html=True,
                )

    rank_df = modules.rank()
    st.header("Ranking Top 5 puntajes")
    st.dataframe(rank_df[:5], width=1000, height=212, hide_index=True)
    col1, col2 = st.columns([1, 1])
    with col1:
        button = st.button("Volver a jugar")
        if button:
            del SESSION["game_state"]
            del SESSION["animation_shown"]
            SESSION.questions["question_counter"] = 0
            st.rerun()
    with col2:
        play = st.button("🥉 Ranking")
        if play:
            st.switch_page("pages/05_Ranking.py")
