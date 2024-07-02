import pathlib
import pandas as pd
import random
import streamlit as st

BASE_PATH = pathlib.Path(__file__).parent


def selected_dataset(subject):
    """Receives a string and returns the name of the dataset.

    Args:
        subject (string): what the dataset is about.

    Returns:
        string: name of the dataset.
    """
    match subject:
        case "Aeropuertos":
            read_data = "ar-airports.csv"
        case "Lagos":
            read_data = "lagos_arg.csv"
        case "Conectividad":
            read_data = "Conectividad_Internet.csv"
        case "Censo 2022":
            read_data = "c2022_tp_c_resumen_adaptado.csv"
    return read_data


def rank():
    """Create a dataframe.

    Returns:
        DataFrame: a dataframe containing users_score.json
    """
    READ_DATA = BASE_PATH / ("data") / ("user_score.json")

    try:
        df = pd.read_json(READ_DATA)
        df = df.sort_values("Puntaje", ascending=False)
        df = df.reset_index(drop=True)
        df.insert(0, "Puesto", [i + 1 for i in df.index])
        return df
    except:
        return pd.DataFrame()


def set_questions(item, columns):
    """Create a dictionary with 4 facts of a given row from a dataframe

    Args:
        item (series): series with a row from dataframe.
        columns (list): columns of the dataframe.

    Returns:
        Dictionary: dictionary with dataframe info.
    """
    # print("set", columns)
    sample_columns = random.sample(columns, k=4)
    data = {"info0": {}, "info1": {}, "info2": {}, "info3": {}}
    for i in range(len(sample_columns)):
        data[f"info{i}"]["question"] = sample_columns[i]
        data[f"info{i}"]["right_answer"] = item[sample_columns[i]]
    return data


def get_questions(atribute_sample, current_question=0):
    """Receives a dictionary with 4 attributes and writes them in screen
    The number of question is shown on screen. If no number is received, it shows question 1

    Args:
        atribute_sample (dictionary): dictionary with 4 attributes.
        current_question (int, optional): the number of the question. Defaults to 0.
    """
    st.header(f"Pregunta {current_question+1}")
    for info in atribute_sample:
        st.markdown(
            f"<h5 style='color:#96a3a6;'>{atribute_sample[info]['question']}: {atribute_sample[info]['right_answer'] if info != 'info3' else ''}</h5>",
            unsafe_allow_html=True,
        )


def emoji_rain(
    emoji: str,
    font_size: int = 64,
    falling_speed: int = 5,
    animation_length: int = 5,
    emoji_count: int = 50,  # Número de emojis
    min_delay: float = 0,  # Mínimo retraso de caída
    max_delay: float = 5,  # Máximo retraso de caída
):
    """
    Creates a CSS animation where input emoji falls from top to bottom of the screen.

    Args:
        emoji (str): Emoji
        font_size (int, optional): Font size. Defaults to 64.
        falling_speed (int, optional): Speed at which the emoji 'falls'. Defaults to 5.
        animation_length (Union[int, str], optional): Length of the animation. Defaults to "infinite".
        emoji_count (int, optional): Number of emojis. Defaults to 50.
        min_delay (float, optional): Minimum delay before the emoji starts falling. Defaults to 0.
        max_delay (float, optional): Maximum delay before the emoji starts falling. Defaults to 5.
    """

    if isinstance(animation_length, int):
        animation_length = f"{animation_length}"

    delays = [
        round(random.uniform(min_delay, max_delay), 2) for _ in range(emoji_count)
    ]

    st.write(
        f"""
    <style>
    body {{
        background: gray;
        margin: 0;
        overflow: hidden;  /* Evita barras de desplazamiento */
    }}

    .emoji {{
        color: #777;
        font-size: {font_size}px;
        font-family: Arial;
    }}

    @-webkit-keyframes emojis-fall {{
        0% {{
            top: -10%;
        }}
        100% {{
            top: 100%;
        }}
    }}
    @-webkit-keyframes emojis-shake {{
        0% {{
            -webkit-transform: translateX(0px);
            transform: translateX(0px);
        }}
        50% {{
            -webkit-transform: translateX(10px);
            transform: translateX(10px);
        }}
        100% {{
            -webkit-transform: translateX(0px);
            transform: translateX(0px);
        }}
    }}
    @keyframes emojis-fall {{
        0% {{
            top: -10%;
        }}
        100% {{
            top: 100%;
        }}
    }}
    @keyframes emojis-shake {{
        0% {{
            transform: translateX(0px);
        }}
        25% {{
            transform: translateX(10px);
        }}
        50% {{
            transform: translateX(-10px);
        }}
        100% {{
            transform: translateX(0px);
        }}
    }}

    .emoji {{
        position: fixed;
        top: -10%;
        z-index: 99999;
        -webkit-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
        user-select: none;
        cursor: default;
        -webkit-animation-name: emojis-fall, emojis-shake;
        -webkit-animation-duration: {falling_speed}s, 3s;
        -webkit-animation-timing-function: linear, ease-in-out;
        -webkit-animation-iteration-count: {animation_length}, {animation_length};
        -webkit-animation-play-state: running, running;
        animation-name: emojis-fall, emojis-shake;
        animation-duration: {falling_speed}s, 3s;
        animation-timing-function: linear, ease-in-out;
        animation-iteration-count: {animation_length}, {animation_length};
        animation-play-state: running, running;
    }}
    """
        + "".join(
            [
                f"""
    .emoji:nth-of-type({i+1}) {{
        left: {i * 100 / emoji_count}%;
        -webkit-animation-delay: {delays[i]}s, {delays[i]}s;
        animation-delay: {delays[i]}s, {delays[i]}s;
    }}
    """
                for i in range(emoji_count)
            ]
        )
        + """
    </style>
    """,
        unsafe_allow_html=True,
    )

    st.write(
        f"""
    <div class="emojis">
        {"".join([f'<div class="emoji">{emoji}</div>' for _ in range(emoji_count)])}
    </div>
    """,
        unsafe_allow_html=True,
    )


def replace_accented_letters(name):
    """This function recieve an string and replace accented vowels for the vowels without accent

    Args:
        name (string)

    Returns:
        string: string without accent vowels.
    """
    vowels = {"á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u"}

    for letter in vowels.keys():
        name = name.replace(letter, vowels[letter])
    return name


def modify_province(p):
    """Modify the province name.

    Args:
        p (string): province name.

    Returns:
        string: modified province name.
    """
    p = replace_accented_letters(p.lower())
    match p:
        case "tierra del fuego, antartida e islas del atlantico sur":
            return "Tierra del Fuego"
        case "buenos aires (autonomous city":
            return "Ciudad Autonoma"
        case "caba":
            return "Ciudad Autonoma"
        case "rio negro / neuquen":  # 80% pertenece a Neuquen
            return "Neuquen"
        case _:
            p = p.title()
            return p
