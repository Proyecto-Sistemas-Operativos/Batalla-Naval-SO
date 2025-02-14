import random

print("\nBATALLA NAVAL\n")

# Crear el tablero de juego
def crear_tablero(tamaño):
    return [['~'] * tamaño for _ in range(tamaño)]

# Imprimir los tableros de juego en paralelo
def imprimir_tableros(tablero1, tablero2, tipo1, tipo2):
    print(f"\n    {tipo1}          {tipo2}\n")
    print("   A B C D E F G H I J        A B C D E F G H I J")
    for idx, (fila1, fila2) in enumerate(zip(tablero1, tablero2)):
        print(f"{idx+1:<2} " + " ".join(fila1) + "     " + f"{idx+1:<2} " + " ".join(fila2))

# Colocar los barcos en el tablero
def colocar_barcos_manual(tablero, tamaño, nombre_barco):
    while True:
        orientacion = input(f"\nIntroduce la orientación del {nombre_barco} (H para horizontal, V para vertical): ").upper()
        if orientacion not in ['H', 'V']:
            print("Orientación inválida. Por favor, introduce 'H' para horizontal o 'V' para vertical.")
            continue

        posicion = input(f"Introduce la posición inicial del {nombre_barco} (ej. B3): ")
        columna = ord(posicion[0].upper()) - ord('A')
        fila = int(posicion[1:]) - 1

        if orientacion == 'H':
            if columna + tamaño <= len(tablero) and all(tablero[fila][columna + i] == '~' for i in range(tamaño)):
                for i in range(tamaño):
                    tablero[fila][columna + i] = 'B'
                break
        elif orientacion == 'V':
            if fila + tamaño <= len(tablero) and all(tablero[fila + i][columna] == '~' for i in range(tamaño)):
                for i in range(tamaño):
                    tablero[fila + i][columna] = 'B'
                break
        print("Posición inválida o el espacio ya está ocupado. Inténtalo de nuevo.")

# Realizar un disparo
def disparar(tablero_jugador, tablero_disparos, fila, columna):
    if tablero_jugador[fila][columna] == 'B':
        tablero_jugador[fila][columna] = 'X'
        tablero_disparos[fila][columna] = 'X'
        return True
    elif tablero_jugador[fila][columna] == '~':
        tablero_jugador[fila][columna] = 'O'
        tablero_disparos[fila][columna] = 'O'
        return False
    return None

# Verificar si un barco está hundido
def verificar_hundimiento(tablero, tamaños_barcos):
    for tamaño in tamaños_barcos:
        for fila in tablero:
            if fila.count('B') == tamaño:
                if all(celda != 'B' for fila in tablero for celda in fila):
                    return True, tamaño
    return False, 0

# Juego principal
def juego_batalla_naval():
    tamaño = 10
    barcos = [("Portaviones", 4), ("Acorazado", 3), ("Crucero", 2), ("Destructor", 1)]  # Nombre y tamaño de los barcos
    tamaños_barcos = [4, 3, 2, 1]  # Solo tamaños de los barcos para verificación

    victorias_jugador1 = 0
    victorias_jugador2 = 0

    while True:
        tablero_jugador1_barcos = crear_tablero(tamaño)
        tablero_jugador1_disparos = crear_tablero(tamaño)
        tablero_jugador2_barcos = crear_tablero(tamaño)
        tablero_jugador2_disparos = crear_tablero(tamaño)

        print("Jugador 1, coloca tus barcos.")
        for nombre_barco, tamaño in barcos:
            imprimir_tableros(tablero_jugador1_barcos, tablero_jugador1_disparos, "Barcos Jugador 1", "Disparos Jugador 1")
            colocar_barcos_manual(tablero_jugador1_barcos, tamaño, nombre_barco)

        print("\nJugador 2, coloca tus barcos.")
        for nombre_barco, tamaño in barcos:
            imprimir_tableros(tablero_jugador2_barcos, tablero_jugador2_disparos, "Barcos Jugador 2", "Disparos Jugador 2")
            colocar_barcos_manual(tablero_jugador2_barcos, tamaño, nombre_barco)

        turno = 1
        while True:
            print(f"\nTurno del Jugador {turno}")
            if turno == 1:
                imprimir_tableros(tablero_jugador1_barcos, tablero_jugador1_disparos, "Barcos Jugador 1", "Disparos Jugador 1")
            else:
                imprimir_tableros(tablero_jugador2_barcos, tablero_jugador2_disparos, "Barcos Jugador 2", "Disparos Jugador 2")

            posicion = input("\nIntroduce la posición para disparar (ej. B3): ")
            columna = ord(posicion[0].upper()) - ord('A')
            fila = int(posicion[1:]) - 1

            if turno == 1:
                resultado = disparar(tablero_jugador2_barcos, tablero_jugador1_disparos, fila, columna)
                hundido, tamaño = verificar_hundimiento(tablero_jugador2_barcos, tamaños_barcos)
            else:
                resultado = disparar(tablero_jugador1_barcos, tablero_jugador2_disparos, fila, columna)
                hundido, tamaño = verificar_hundimiento(tablero_jugador1_barcos, tamaños_barcos)

            if resultado is None:
                print("Ya disparaste en esa posición.")
            elif resultado:
                print("¡Le diste!")
                if hundido:
                    print(f"¡Has hundido un barco de tamaño {tamaño}!")
            else:
                print("¡Agua!")

            if all(celda != 'B' for fila in tablero_jugador2_barcos for celda in fila):
                print("\n¡Felicidades, hundiste todos los barcos!")
                print("\n¡Jugador 1 gana!")
                victorias_jugador1 += 1
                break
            elif all(celda != 'B' for fila in tablero_jugador1_barcos for celda in fila):
                print("\n¡Felicidades, hundiste todos los barcos!")
                print("\n¡Jugador 2 gana!")
                victorias_jugador2 += 1
                break

            turno = 2 if turno == 1 else 1

        print(f"\nPuntuación actual:\nJugador 1: {victorias_jugador1} victorias\nJugador 2: {victorias_jugador2} victorias")

        continuar = input("\n¿Quieres jugar otra partida? (s/n): ").lower()
        if continuar != 's':
            break

# Ejecutar el juego
juego_batalla_naval()
