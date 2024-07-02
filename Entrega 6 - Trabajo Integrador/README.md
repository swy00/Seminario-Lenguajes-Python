# Trabajo Integrador - Seminario Lenguajes

Este repositorio contiene el trabajo integrador para el Seminario Lenguajes Python.

En la primera etapa se enfocó el trabajo en el análisis de datos, para su posterior uso en PyTrivia.

En la segunda etapa nos centramos en el desarrollo de la interfaz gráfica con el uso de Streamlit y la lógica del juego.

## Integrantes Grupo 11

- [Francisco Ronga](https://github.com/swy00)
- [Tomas Panelo](https://github.com/tomaspanelo)
- [Simón Mc Govern](https://github.com/SimonMcGovern)
- [Santiago Sanchez](https://github.com/santiagosanchezlp)

## Instalación

Usar Python 3.11 o superior y ejecutar:

- Linux:
```
    python3.11 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
```
- Windows:
```
    py -m venv venv
    source venv/Scripts/activate
    pip install -r requirements.txt
```

## Etapa 1 - Apertura de archivos.

- Archivo procesamiento de datasets:

```
    jupyter notebook .\datasets_processor\dataset_processor.ipynb

```
- Archivo de consultas:

```
    jupyter notebook .\consultas\consultas.ipynb

```

## Etapa 2 - Inicio de PyTrivia


```
    python -m streamlit run streamlit/Inicio.py

```

## Funcionalidades de la aplicacion Streamlit
La aplicación Streamlit contiene las siguientes páginas:

- Inicio: Información fundamental y parámetros básicos para comenzar a jugar.
- Conociendo nuestros datos: Gráficos, tablas y mapas con información de los datasets.
- Juego: juego de trivia.
- Formulario de registro: Permite registrar nuevos usuarios.
- Ranking: Ranking de mejores resultados.
- Estadísticas: Información estadística obtenida del uso del juego.


## License

Este proyecto esta licenciado bajo la *MIT License*, para mas información ir a [LICENSE](https://gitlab.catedras.linti.unlp.edu.ar/python2024/code/grupo11/-/blob/main/LICENSE)