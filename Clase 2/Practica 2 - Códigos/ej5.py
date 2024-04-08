article = """ título: Experiences in Developing a Distributed Agent-
based Modeling Toolkit with Python Version 3
resumen: Distributed agent-based modeling (ABM) on high-performance 
computing resources provides the promise of capturing unprecedented 
details of large-scale complex systems. However, the specialized 
knowledge required for developing such ABMs creates barriers to wider 
adoption and utilization. Here we present our experiences in 
developing an initial implementation of Repast4Py, a Python-based 
distributed ABM toolkit. We build on our experiences in developing ABM
toolkits, including Repast for High Performance Computing (Repast 
HPC), to identify the key elements of a useful distributed ABM 
toolkit. We leverage the Numba, NumPy, and PyTorch packages and the 
Python C-API to create a scalable modeling system that can exploit the
largest HPC resources and emerging computing architectures. """

#Encuentro el inicio y fin, ignoro la palabra clave del principio con el "+len(asd)"" y con .strip elimino los espacios vacios
titulo = article[(article.find("título:")+ len("título:")):(article.find("resumen:"))].strip()
resumen = article[(article.find("resumen:")+ len("resumen:")):(len(article))].strip()

#Como los numeros no cuentan, los elimino de los strings
titulo = ''.join(i for i in titulo if not i.isdigit())
resumen = ''.join(i for i in resumen if not i.isdigit())
#Recorro oracion por oracion y veo si cumple las condiciones
oraciones = resumen.split(".")
facil=0
aceptable=0
dificil=0
muy_dificil =0
for i in oraciones:
    palabras_oracion=i.split()
    if len(palabras_oracion) <= 12:
        facil+=1
    elif 13 <= len(palabras_oracion) <= 17:
        aceptable+=1
    elif 18 <= len(palabras_oracion) <= 25:
        dificil += 1
    else:
        muy_dificil += 1

informe_titulo = "not ok" if len(titulo.split()) > 10 else "ok"
print(f"titulo: {informe_titulo}\nCantidad de oraciones faciles de leer: {facil}, aceptables para leer:{aceptable},dificil de leer: {dificil}, muy dificil de leer {muy_dificil}.")