import random
# Lista de palabras posibles
words = ["python", "programación", "computadora", "código", "desarrollo",
"inteligencia"]
 
# Elegir una palabra al azar
secret_word = random.choice(words)
# Número de fallos
max_attempts=5
failed_attempts = 0
# Lista para almacenar las letras adivinadas
guessed_letters = []
 
print("¡Bienvenido al juego de adivinanzas!")
print("Estoy pensando en una palabra. ¿Puedes adivinar cuál es?")
 
#Cambio la word_displayed dependiendo el nivel seleccionado
posibles_niveles={"1":"Facil","2":"Media","3":"Dificil"}
print(">En que nivel desea jugar:")
for i, j in posibles_niveles.items():
    print(f"{' ' * 4} {i} - {j}")
 
while True:
    nivel=input(f">Elegir un nivel: ")
    if nivel not in posibles_niveles:
        print(f"!Nivel ingresado inexistente, vuelva a elegir ")
    else:
        nivel=int(nivel)
        break
 
word_displayed=""
if nivel == 1: #Se muestran todas las vocales
    for i in secret_word:
        if i in "aeiouáéíóú":
            word_displayed+=i
            guessed_letters.append(i)
        else:
            word_displayed+="_"
elif nivel == 2:  #Se muestra la primer y ultima letra
 
    #Como el ejercicio no especifica se podía hacer :
    #>word_displayed = (secret_word[0]+ "-" * (len((secret_word))-2) + secret_word[(len((secret_word))-1)])<
    #Pero en caso de que alguna de estas dos letras vuelva a aparecer en el medio de la palabra, quedaba sin mostrarse y generaba confusion,
    #por lo tanto decidi mostrar la letra en caso de repetición.
    #Queda por hacer el caso de que haya alguna vocal en las puntas y en el centro esté con acento.
    guessed_letters.append(secret_word[0])
    guessed_letters.append(secret_word[(len((secret_word))-1)])
    for i in secret_word:
        if i in guessed_letters:
            word_displayed+=i
        else:
            word_displayed+="_"
elif nivel == 3: #No se muestra ninguna letra de la palabra
    word_displayed = "_" * len(secret_word)

# Mostrarla palabra parcialmente adivinada
print(f"/Palabra: {word_displayed}")

#Puede fallar max_attempts veces
while failed_attempts < max_attempts:
    # Pedir al jugador que ingrese una letra
    letter = input(">Ingresa una letra: ").lower()
    #Checkeo que el input sea UNA sola letra, y parte del abecedario.
    #Si el input fue "", se cuenta como error 
    if (not letter.isalpha()) or (len(letter)!=1):
        print("!Ingresar UNA letra del abecedario, no puede ser ''.")
        continue

    # Verificar si la letra ya ha sido adivinada
    if letter in guessed_letters:
        print("!Ya has intentado con esa letra. Intenta con otra.")
        continue

    # Agregar la letra a la lista de letras adivinadas
    guessed_letters.append(letter)

    # Verificar si la letra está en la palabra secreta
    if letter in secret_word:
        print("¡Bien hecho! La letra está en la palabra.")
    else:
        failed_attempts += 1
        print(f"Lo siento, la letra no está en la palabra,quedan {(max_attempts-failed_attempts)} intentos")
    # Mostrar la palabra parcialmente adivinada
    letters = []
 
    for letter in secret_word:
        if letter in guessed_letters:
            letters.append(letter)
        else:
            letters.append("_")
    word_displayed = "".join(letters)
 
    print(f"Palabra: {word_displayed}")
    # Verificar si se ha adivinado la palabra completa
    if word_displayed == secret_word:
        print(f"¡Felicidades! Has adivinado la palabra secreta:{secret_word}")
        break
else:
    print(f"¡Oh no! Has llegado a {failed_attempts} intentos.")
    print(f"La palabra secreta era: {secret_word}")