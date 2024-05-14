import streamlit as st
import pathlib
import json
import os
import datetime as dt

gender_tuple = ("M", "F", "X")

col1, col2 = st.columns([0.7, 0.3])

with col1:
# Formulario de registro
    placeholder = st.empty()
    with placeholder.form("registration", clear_on_submit=True):
        st.header('Registro en el sistema')
        st.subheader('Ingrese la información necesaria para registrarse en el sistema')
        # Lista de nombres de las pestañas (ámbitos)
        username = st.text_input("Ingrese su nombre de usuario", placeholder="Nombre de usuario")
        fullname = st.text_input("Ingrese su nombre y apellido", placeholder="Nombre y apellido")
        email = st.text_input("Ingrese su dirección de correo electrónico", placeholder="Dirección de correo electrónico")
        birthdate = str(st.date_input("Ingrese su fecha de nacimiento", value=None, min_value=dt.datetime.today() - dt.timedelta(days=36500), max_value=dt.datetime.today(), format="DD/MM/YYYY"))
        gender = st.radio('Indique su género', gender_tuple)
        Register = st.form_submit_button('Registrarse')
    read_data = pathlib.Path('./data/user_data.json')
    write_data = pathlib.Path('./data/user_data.json')

    if Register:
        # Verificar todos los campos completos
        if username and fullname and email and birthdate and gender:
            # Diccionario con los datos del usuario
            
            datos_usuario = {
                'Nombre de usuario': username,
                'Nombre Completo': fullname,
                'Mail': email,
                'Fecha de nacimiento': birthdate,
                'Género': gender
            }
            #Guardar o actualizar datos
            
            #Checkeo si existe el archivo y si contiene algo, sino deberia crear la estructura inicial
            if (os.stat(read_data).st_size > 0):
                with (read_data.open(mode='r', encoding='utf-8') as read_file):
                    data_load = json.load(read_file)
            else:
                data_load=[]    
            
            mod = False
            for i, user in enumerate(data_load):
                if user['Mail'] == datos_usuario['Mail']:
                    mod = True
                    data_load[i]= datos_usuario
                    break
            with col2:
                #Informa los datos enviados en el registro
                if (not mod):
                    data_load.append(datos_usuario)
                    st.title("Nuevo usuario ingresado:")
                else:
                    st.title("Usuario modificado:")
                for elem in datos_usuario:
                    st.text(f"{elem}: {datos_usuario[elem]}")
                #Vuelvo a escribir todo el json
                with (write_data.open(mode='w', encoding='utf-8') as write_file):
                    json.dump(data_load, write_file, indent=4)
                
        else:
            st.warning('Completar todos los campos.')
