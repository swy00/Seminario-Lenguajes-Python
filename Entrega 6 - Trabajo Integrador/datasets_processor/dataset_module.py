import csv
import pathlib

# Database design:
# ar-airports:
elevation_ft_field = 6
air_city_field = 13
region_field = 10

# ar:
city_field = 0
province_field = 5


def define_height(value):
    """Receives a height (numeric value) and returns an str: Elevation criteria."""
    if value < 131:
        return "bajo"
    elif value < 903:
        return "medio"
    else:
        return "alto"


def include_elevation(airport):
    """Receives a list with information of an airport with an especific database design and returns the elevation criteria.
    Parameters:
    airport (list): List with information of an airport with an especific database design.
    Return:
    str: Elevation criteria.
    """
    try:
        if int(airport[elevation_ft_field]) <= 131:
            elevation_name = "bajo"
        elif int(airport[elevation_ft_field]) <= 903:
            elevation_name = "medio"
        else:
            elevation_name = "altos"
    except:
        elevation_name = ""
    return elevation_name


def include_prov(airport):
    """Receives a list with information of an airport with an especific database design and returns the province in which it is located.
    Parameters:
    airport (list): List with information of an airport with an especific database design.
    Return:
    str: Province name.
    """
    read_provinces = pathlib.Path("../datasets/original_datasets/ar.csv")
    with read_provinces.open(mode="r", newline="", encoding="utf-8") as read_provinces:
        provinces = csv.reader(read_provinces)
        for city in provinces:
            if city[city_field] == airport[air_city_field]:
                return city[province_field]
        return airport[region_field][0:-9]


def hyphen_replace(connectivity_map):
    '''This function recieve a dict and transform the strings "--" for the word "NO"'''
    for key, value in connectivity_map.items():
        if value == "--":
            connectivity_map[key] = "NO"
    return connectivity_map


def has_connectivity(connectivity_map):
    """This function recieve a dict and add value to the field "posee_conectividad" if exists,
    if doesn't exist create the field and add the value
    """
    if "SI" in connectivity_map.values():
        connectivity_map["posee_conectividad"] = "SI"
    else:
        connectivity_map["posee_conectividad"] = "--"
    return connectivity_map


def convert_GMS_coordinate(coordinate):
    """
    Converts a coordinate in GMS format (degrees, minutes, and seconds) to DD (decimal degrees).

    Parameters:
    coordinate (str): The coordinate in GMS format.

    Returns:
    float: The coordinate converted to decimal degrees.
    """
    # Degrees, minutes, and seconds
    degrees, rest = coordinate.split("°")
    minutes, rest = rest.split("'")
    seconds, sign = rest.split('"')

    # Decimal degrees
    # N or E are positive values, S or W negative
    sign = -1 if sign == "S" or sign == "W" else 1
    # Formula = Degrees + Minutes/60 + Seconds/3600
    decimal_degree = sign * (
        float(degrees) + (float(minutes) / 60) + (float(seconds)) / 3600
    )

    return round(decimal_degree, 3)


def calculate_percentage(population, street_population):
    """
    Calculates the percentage of the two values it receives as parameters.

    Args:
        population : total value.
        street_population : partial value.

    Returns:
        Percentage between street_population and population.
    """

    result = (float(street_population) / float(population)) * 100
    return round(result, 4)


def replace_values(line):
    """
    Replace '///' o '-' with 0.

    Args:
        line: list.

        Returns:
            List with modified values if the values existed in the list.
    """

    for x in range(len(line)):
        if line[x] == "///" or line[x] == "-":
            line[x] = 0
    return line
