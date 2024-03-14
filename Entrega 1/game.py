import random
# Lista de palabras posibles
words = ["python", "programación", "computadora", "código", "desarrollo",
"inteligencia"]

# Elegir una palabra al azar
secret_word = random.choice(words)
# Número de fallos
max_attempts=10
failed_attempts = 0
# Lista para almacenar las letras adivinadas
guessed_letters = []

print("¡Bienvenido al juego de adivinanzas!")
print("Estoy pensando en una palabra. ¿Puedes adivinar cuál es?")

#Cambio la word_displayed dependiendo el nivel seleccionado
posibles_niveles={"Facil","Media","Dificil"}
nivel=input(f"En que nivel desea jugar{posibles_niveles}")
while nivel not in posibles_niveles:
    nivel=(f"Nivel ingresado no disponible, vuelva a elegir {posibles_niveles}")
if nivel=="Facil": #Se muestran todas las vocales
    word_displayed=""
    for i in secret_word:
        if i in "aeiou":
            word_displayed+=i
            #Agrego las vocales a la lista de adivinadas
            guessed_letters.append(i)
        else:
            word_displayed+="_"
elif nivel=="Media":  #Se muestra la primer y ultima letra
    word_displayed = (secret_word[0]+ "-" * (len((secret_word))-2) + secret_word[(len((secret_word))-1)])
    #Agrego a la lista de Adivinadas
    guessed_letters.append(secret_word[0])
    guessed_letters.append(secret_word[(len((secret_word))-1)])
elif nivel=="Dificil": #No se muestra ninguna letra de la palabra
    word_displayed = "_" * len(secret_word)

# Mostrarla palabra parcialmente adivinada
print(f"Palabra: {word_displayed}")

#Puede fallar max_attempts veces
while failed_attempts < max_attempts:
    # Pedir al jugador que ingrese una letra
    letter = input("Ingresa una letra: ").lower()
    
    #Verifico si el input fue "", se cuenta como error y pierde intento
    if letter == "":
        print("Error no se introdujo ninguna letra, vuelva a intentarlo")
        continue
    # Verificar si la letra ya ha sido adivinada
    if letter in guessed_letters:
        print("Ya has intentado con esa letra. Intenta con otra.")
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