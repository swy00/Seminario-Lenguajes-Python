import streamlit as st
import pathlib
import modules

st.set_page_config(
    page_title="PyTrivia",
    page_icon="🕹️",
    layout="centered",
    initial_sidebar_state="auto",
)

STYLE00_PATH = modules.BASE_PATH / "styles" / "style00.css"
with open(STYLE00_PATH) as f:
    css = f.read()
css = f"<style>{css}</style>"
st.markdown(css, unsafe_allow_html=True)

st.markdown(
    """
    <div class="animation">
        PyTrivia
        <div>PyTrivia</div>
        <div>PyTrivia</div>
        <div>PyTrivia</div>
        <div>PyTrivia</div>
</div>""",
    unsafe_allow_html=True,
)
st.subheader("¡Bienvenido a Pytrivia!")
st.subheader("Breve descripción del juego:")
st.markdown(
    """***Pytrivia*** es un juego de preguntas y respuestas acerca de la temática elegida. ¡Gana puntos por tus respuestas correctas y sube en el ranking!"""
)
st.markdown(
    """
            Niveles de dificultad:
            - **Fácil**: Tendrás 3 posibles respuestas para elegir.
            - **Media**: Tendrás la cantidad de dígitos de la respuesta.
            - **Alta**: No tendrás ayuda.\n
            *Nota: La dificultad elegida afecta la cantidad de puntos obtenidos. Mientras más alta sea la dificultad más puntos obtendrás por respuesta correcta.*
            """
)


st.subheader("Si ya estas registrado puedes comenzar a jugar.")
play = st.button("Ir a jugar 🚀")
if play:
    st.switch_page("pages/03_Juego.py")
st.subheader(
    """
    Si no estás registrado, los datos necesarios para comenzar a jugar son:
    - **Nombre de usuario.**\n
    - **Apellido y nombre.**\n
    - **Mail.**\n
    - **Fecha de nacimiento.**\n
    - **Género.**\n
"""
)
register = st.button("Registrarse ✍️")
if register:
    st.switch_page("pages/04_Formulario_de_registro.py")
