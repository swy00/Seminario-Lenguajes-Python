import streamlit as st
import pandas as pd
import pathlib
import modules

st.set_page_config(
    page_title="PyTrivia",
    page_icon="🥉",
    layout="centered",
    initial_sidebar_state="auto",
)
STYLE05_PATH = modules.BASE_PATH / "styles" / "style05.css"
with open(STYLE05_PATH) as f:
    css = f.read()
css = f"<style>{css}</style>"
st.markdown(css, unsafe_allow_html=True)

df = modules.rank()
if not df.empty:
    st.markdown(css, unsafe_allow_html=True)
    if df["Mail"].count() >= 3:
        st.markdown(
            f"""
                    <div class="podium-container">
                        <lo class="podium">
                            <li><h1>{df["Mail"][0].split('@')[0]}</h1><h4>Puntaje </h4><h1>{df["Puntaje"][0]}</h1></li>
                            <li><h1>{df["Mail"][1].split('@')[0]}</h1><h1>{df["Puntaje"][1]}</h1></li>
                            <li><h1>{df["Mail"][2].split('@')[0]}</h1><h1>{df["Puntaje"][2]}</h1></li>
                        </lo>
                    </div>""",
            unsafe_allow_html=True,
        )
    st.header("Ranking histórico de puntaje")
    st.dataframe(df[:15], width=1000, height=562, hide_index=True)
else:
    st.header("Para ser el primero adentrate en el mundo de Pytrivia")
    play = st.button("Ir a jugar 🚀")
    if play:
        st.switch_page("pages/03_Juego.py")
