import csv
import pathlib

custom_airports = pathlib.Path('../datasets/custom_datasets/ar-airports.csv')
custom_lagos = pathlib.Path('../datasets/custom_datasets/lagos_arg.csv')
custom_conectividad = pathlib.Path('../datasets/custom_datasets/Conectividad_Internet.csv')
custom_poblacion = pathlib.Path('../datasets/custom_datasets/c2022_tp_c_resumen_adaptado.csv')

def modify_province(p):
    """
    Modifies the name of the province 'p' according to certain established rules.

    Parameters:
    p (str): The name of the province to be modified.

    Returns:
    str: The modified name of the province.
    """
    p = replace_accented_letters(p)
    match p:
        case 'tierra del fuego':
            return 'tierra del fuego, antartida e islas del atlantico sur'
        case 'buenos aires (autonomous city':
            return 'ciudad autonoma de buenos aires'
        case 'caba':
            return 'ciudad autonoma de buenos aires'
        case 'rio negro / neuquen':  # 80% pertenece a Neuquen
            return 'neuquen'
        case _:
            return p


def filter_provinces(population_num, greater_less):
    """
    Filters the provinces according to their population by accessing a CSV file that contains the data.

    Parameters:
    population_num (int): The population value from which the filter is applied.
    greater_less (str): Indicates whether provinces with population greater or less than population_num are included.

    Returns:
    list: A list of province names that meet the specified criteria.
    """
    with custom_poblacion.open(mode='r', newline='', encoding='utf-8') as read_population:
        population_reader = csv.reader(read_population)
        next(population_reader)  # Saltear header
        next(population_reader)  # Saltear la fila 'Total País'
        if greater_less == "mayor":
            provinces_meet = list(filter(lambda x: int((x[1])) > int(population_num), population_reader))
        else:
            provinces_meet = list(filter(lambda x: int((x[1])) < int(population_num), population_reader))
        provinces = []
        for i in range(len(provinces_meet)):
            c_prov = replace_accented_letters(provinces_meet[i][0].lower())
            provinces.append(c_prov)
    return provinces


def show_info(province):
    """
    Shows airports, lakes, and connectivity information about the given provinces.

    Parameters:
    province (list): List of provinces.
    """
    def info_airports(provinces_meet, province_data):
        with custom_airports.open(mode='r', newline='', encoding='utf-8') as read_airports:
            airports = csv.reader(read_airports)
            next(airports)  # Saltear header
            for row in airports:
                prov_air = modify_province(row[10][:row[10].rfind("Province")].strip().lower())
                if prov_air in provinces_meet:
                    if prov_air not in province_data:
                        province_data[prov_air] = {'airports': [row[3]], 'lagos': [], 'conectividad': {}}
                    else:
                        province_data[prov_air]['airports'].append(row[3])
        return province_data

    def info_lakes(provinces_meet, province_data):
        with custom_lagos.open(mode='r', encoding='utf-8') as read_lakes:
            lakes = csv.reader(read_lakes)
            next(lakes) # Salteo header
            for row in lakes:
                prov_lake = modify_province(row[1].lower())
                if prov_lake in provinces_meet:
                    if prov_lake not in province_data:
                        province_data[prov_lake] = {'lagos': [row[0]]}
                    else:
                        province_data[prov_lake]['lagos'].append(row[0])
        return province_data

    def info_connectivity(provinces_meet, province_data):
        with custom_conectividad.open(mode='r', encoding='utf-8') as read_conect:
            connectivity = csv.reader(read_conect)
            header = next(connectivity)  # Guardo Header
            for row in connectivity:
                prov_connect = modify_province(row[0].title().strip().lower())
                if prov_connect in provinces_meet:
                    for i in range(4, 13):
                        if row[i] == 'SI':
                            province_data[prov_connect]['conectividad'][header[i]] = 'SI'
        return province_data

    def print_info(province_data):
        for province, data in province_data.items():
            print(f"> {province.title().ljust(50)}")
            if 'airports' in data:
                print("\n~Aeropuertos:")
                for aeropuerto in data['airports']:
                    print(f"   - {aeropuerto}")
            if 'lagos' in data:
                print("\n~Lagos:")
                for lago in data['lagos']:
                    print(f"   - {lago}")
            if 'conectividad' in data:
                print("\n~Conectividad:")
                for tipo, valor in data['conectividad'].items():
                    print(f"   - {tipo}: {valor}")
            print("-" * 50)

    province_data = {}
    info_airports(province, province_data)
    info_connectivity(province, province_data)
    info_lakes(province, province_data)
    print_info(province_data)


def show_lake_info(size):
    """
    Shows information about lakes of a specific size.

    Parameters:
    size (str): The size of lakes to be displayed ("small", "medium", or "large").
    """
    sup_size = 7
    read_dataset = pathlib.Path('../datasets/custom_datasets/lagos_arg.csv')
    with read_dataset.open(mode='r', encoding='utf-8') as read_file:
        reader = csv.reader(read_file)
        next(reader)  # Saltea el header
        print(f"> Informacion lagos de tamaño {size}: ")
        for line in reader:
            if line[sup_size] == size:    
                print(f"""
Nombre:             {line[0]}
Provincia:          {line[1]}
Superficie:         {line[2]}
Profundidad Máxima: {line[3] if line[3] else 'No disponible'}
Profundidad Media:  {line[4] if line[4] else 'No disponible'}
Latitud:            {line[5]}
Longitud:           {line[6]}
""")


def replace_accented_letters(name):
    '''
    This function recieve an string and replace accented vowels for the vowels without accent
    '''
    vowels = {"á":"a", "é":"e", "í":"i", "ó":"o", "ú":"u"}

    for letter in vowels.keys():
            name = name.replace(letter, vowels[letter])
    return name

def calculate_gap(men,women):
    """
    Receives two values and calculates the gap between them.
    Args:
        men : int.
        women: int.
    Returns:
        The difference between men and women.
    """
    gap= int(men) - int(women)
    if(gap < 0):
        gap= gap * -1
    return gap
