import streamlit as st
recognized_women = {
    'Informática': ['Cecilia Berdichevsky', 'Rebeca Cherep De Guber', 'Victoria Raquel Bajar', 'Noemí García ',
                    'Ida Holz','Gladys Beatriz Rizzo','Ida Bianchi'],
    'Ciencia': ['Eugenia Sacerdote de Lutig', 'Carolina Vera', 'Emma Perez Ferreira', 'Silvia Braslavky',
                'Emilia Ferreiro', 'Cecilia Grierson', 'Julieta Lanteri'],
    'Deportes': ['Gabriela Sabatini','Luciana Aymar','Cecilia Carranza Saroli','Noemí Simoneto','Paula Pareto',
                 'Jeanette Campbell', 'Mary Terán'],
    'Cantantes': ['Mariana Bianchini', 'Gilda','Mercedes Sosa','Tita Merello' ,'Lali Espósito']
}
st.title('Mujeres Destacadas en Argentina')

# Lista de nombres de las pestañas (ámbitos)
tabs = list(recognized_women.keys())
selected_tab = st.radio('Selecciona un Ámbito', tabs)
if selected_tab in recognized_women:
        st.subheader(f'{selected_tab.capitalize()}')

        # Obtener la lista de mujeres para la pestaña seleccionada
        women = recognized_women[selected_tab]

        # Mostrar el selectbox con las mujeres en la lista
        selected_mujer = st.selectbox('Selecciona una Mujer', women)

        if selected_mujer:
            st.write(f'Has seleccionado: {selected_mujer}')
            st.write(f'Es reconocida por ...')