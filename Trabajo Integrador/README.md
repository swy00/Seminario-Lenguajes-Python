# Trabajo Integrador - Seminario Lenguajes

Este repositorio contiene la primera parte del trabajo integrador para el Seminario Lenguajes Python.

## Integrantes Grupo 11

- [Francisco Ronga](https://github.com/swy00)
- [Tomas Panelo](https://github.com/tomaspanelo)
- [Simón Mc Govern](https://github.com/SimonMcGovern)
- [Santiago Sanchez](https://github.com/santiagosanchezlp)

## Instalación

Usar Python 3.11 o superior y ejecutar:

- Linux:
```bash
    python3.11 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
```
- Windows:
```bash
    py -m venv venv
    source venv/Scripts/activate
    pip install -r requirements.txt
```

## Apertura de archivos

- Archivo procesamiento de datasets:

```
jupyter notebook .\datasets_processor\dataset_processor.ipynb

```
- Archivo de consultas:

```
jupyter notebook .\consultas\consultas.ipynb

```

## Inicio de aplicación Streamlit


```
python -m streamlit run streamlit/Inicio.py

```