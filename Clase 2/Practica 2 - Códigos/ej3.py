jupyter_info = """ JupyterLab is a web-based interactive development 
environment for Jupyter notebooks, code, and data. JupyterLab is 
flexible: configure and arrange the user interface to support a wide 
range of workflows in data science, scientific computing, and machine 
learning. JupyterLab is extensible and modular: write plugins that add
new components and integrate with existing ones. """

c = jupyter_info.split(' ')
letra=input('Ingresar una letra').lower()
if len(letra)==1 and (letra.isalpha()):
    for i in c:
        i = i.strip(";:,.¿?!¡(){}'")
        if letra in i:
            print(i)
else: 
    print('ERROR, el input no es UNA letra')


