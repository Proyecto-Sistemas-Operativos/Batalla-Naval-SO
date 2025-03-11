import random

print("\nBATALLA NAVAL\n")


def crear_tablero(tamano):
    return [["~"] * tamano for _ in range(tamano)]


def imprimir_tableros(tablero1, tablero2, tipo1, tipo2):
    print(f"\n    {tipo1}          {tipo2}\n")
    print("   A B C D E F G H I J        A B C D E F G H I J")
    for idx, (fila1, fila2) in enumerate(zip(tablero1, tablero2)):
        print(
            f"{idx+1:<2} "
            + " ".join(fila1)
            + "     "
            + f"{idx+1:<2} "
            + " ".join(fila2)
        )


def colocar_barcos_manual(tablero, tamano, nombre_barco):
    print("-------------\n")
    print("Instrucciones para posicionar")
    print("\nLos barcos son colocados verticalmente de arriba a abajo y horizontalmente de izquierda a derecha")
    print("\nPrincipalmente especifique la orientación de los barcos para colocarlos, luego especifique la posición")
    print("\nPara posicionar verticalmente y horizontalmente los barcos se denota: Columna + Fila. Ejemplo: A1")
    print("\nLas letras representan las columnas (A a la J) y los números representan las filas (1 al 10).")
    print("-------------\n")

    # Coloca cada barco en el tablero
    while True:
        orientacion = input(
            f"\nIntroduce la orientación del {nombre_barco} (H para horizontal, V para vertical): "
        ).upper()

        # Verifica que la orientación sea válida
        if orientacion not in ["H", "V"]:
            print(
                "Orientación inválida. Por favor, introduce 'H' para horizontal o 'V' para vertical."
            )
            continue
        
        # Pide la posición inicial
        posicion = input(f"Introduce la posición inicial del {nombre_barco} (ej. B3): ")

        # Verifica que la posición sea válida
        print(f"POSICION: {posicion}")
        columna = ord(posicion[0].upper()) - ord("A")
        fila = int(posicion[1]) - 1

        # Verifica que la posición del barco esté dentro del tablero de forma horizontal
        if orientacion == "H":
            if columna + tamano <= len(tablero) and all(
                tablero[fila][columna + i] == "~" for i in range(tamano)
            ):
                for i in range(tamano):
                    tablero[fila][columna + i] = "B"
                break
        # Verifica que la posición del barco esté dentro del tablero de forma vertical      
        elif orientacion == "V":
            if fila + tamano <= len(tablero) and all(
                tablero[fila + i][columna] == "~" for i in range(tamano)
            ):
                for i in range(tamano):
                    tablero[fila + i][columna] = "B"
                break

        # Si la posición no es válida, imprime un mensaje de error    
        print("Posición inválida o el espacio ya está ocupado. Inténtalo de nuevo.")

# Manejar el resultado de un disparo efectuado
def disparar(tablero_jugador, tablero_disparos, fila, columna):
    if tablero_jugador[fila][columna] == "B":
        tablero_jugador[fila][columna] = "X"
        tablero_disparos[fila][columna] = "X"
        return True
    elif tablero_jugador[fila][columna] == "~":
        tablero_jugador[fila][columna] = "O"
        tablero_disparos[fila][columna] = "O"
        return False
    return None

# Verificar si un barco fue hundido
def verificar_hundimiento(tablero, tamanos_barcos):
    barcos_hundidos = []
    visitados = set()

    for tamano in sorted(tamanos_barcos, reverse=True):
        # Búsqueda horizontal
        for fila_idx, fila in enumerate(tablero):
            for i in range(len(fila) - tamano + 1):
                segmento = [(fila_idx, i + j) for j in range(tamano)]
                if all(
                    (fila_idx, i + j) not in visitados and fila[i + j] == "X"
                    for j in range(tamano)
                ):
                    barcos_hundidos.append(tamano)
                    visitados.update(segmento)
                    break

        # Búsqueda vertical
        for col_idx in range(len(tablero[0])):
            for i in range(len(tablero) - tamano + 1):
                segmento = [(i + j, col_idx) for j in range(tamano)]
                if all(
                    (i + j, col_idx) not in visitados and tablero[i + j][col_idx] == "X"
                    for j in range(tamano)
                ):
                    barcos_hundidos.append(tamano)
                    visitados.update(segmento)
                    break

    return barcos_hundidos

# Organiza y ejecuta el ciclo completo de partidas del juego de batalla naval
def juego_batalla_naval():
    tamano = 10
    barcos = [
        ("Portaviones", 4),
        ("Acorazado", 3),
        ("Crucero", 2),
        ("Destructor #1", 1),
        ("Destructor #2", 1),
    ]
    tamanos_barcos = [4, 3, 2, 1, 1]

    victorias_jugador1 = 0
    victorias_jugador2 = 0

    # Ciclo de partidas
    while True:
        # Inicializa los tableros de los jugadores
        tablero_jugador1_barcos = crear_tablero(tamano)
        tablero_jugador1_disparos = crear_tablero(tamano)
        tablero_jugador2_barcos = crear_tablero(tamano)
        tablero_jugador2_disparos = crear_tablero(tamano)

        # Coloca los barcos del jugador 1
        print("\nJugador 1, coloca tus barcos.")
        for nombre_barco, tamano in barcos:
            imprimir_tableros(
                tablero_jugador1_barcos,
                tablero_jugador1_disparos,
                "Barcos Jugador 1",
                "Disparos Jugador 1",
            )
            colocar_barcos_manual(tablero_jugador1_barcos, tamano, nombre_barco)

        # Coloca los barcos del jugador 2
        print("\nJugador 2, coloca tus barcos.")
        for nombre_barco, tamano in barcos:
            imprimir_tableros(
                tablero_jugador2_barcos,
                tablero_jugador2_disparos,
                "Barcos Jugador 2",
                "Disparos Jugador 2",
            )
            colocar_barcos_manual(tablero_jugador2_barcos, tamano, nombre_barco)

        # Ciclo de turnos
        turno = 1
        while True:
            print(f"\nTurno del Jugador {turno}")
            if turno == 1:
                imprimir_tableros(
                    tablero_jugador1_barcos,
                    tablero_jugador1_disparos,
                    "Barcos Jugador 1",
                    "Disparos Jugador 1",
                )
            else:
                imprimir_tableros(
                    tablero_jugador2_barcos,
                    tablero_jugador2_disparos,
                    "Barcos Jugador 2",
                    "Disparos Jugador 2",
                )

            posicion = input("\nIntroduce la posición para disparar (ej. B3): ")
            columna = ord(posicion[0].upper()) - ord("A")
            fila = int(posicion[1:]) - 1

            # Realiza el disparo y verifica si se hundió un barco
            if turno == 1:
                resultado = disparar(
                    tablero_jugador2_barcos, tablero_jugador1_disparos, fila, columna
                )
                barcos_hundidos = verificar_hundimiento(
                    tablero_jugador2_barcos, tamanos_barcos
                )
            else:
                resultado = disparar(
                    tablero_jugador1_barcos, tablero_jugador2_disparos, fila, columna
                )
                barcos_hundidos = verificar_hundimiento(
                    tablero_jugador1_barcos, tamanos_barcos
                )

            # Imprime el resultado del disparo, si se hundió un barco o no
            if resultado is None:
                print("Ya disparaste en esa posición.")
            elif resultado:
                print("\n¡Tocado!")
                for tamano in barcos_hundidos:
                    print(f"¡Has hundido un barco de {tamano}!")
            else:
                print("\n¡Agua!")

            # Verifica si se hundieron todos los barcos
            if all(celda != "B" for fila in tablero_jugador2_barcos for celda in fila):
                # Si se hundieron todos los barcos del jugador 2, el jugador 1 gana
                print("\n¡Felicidades, hundiste todos los barcos!")
                print("¡Jugador 1 gana!")
                victorias_jugador1 += 1
                break
            elif all(
                celda != "B" for fila in tablero_jugador1_barcos for celda in fila
            ):
                # Si se hundieron todos los barcos del jugador 1, el jugador 2 gana
                print("\n¡Felicidades, hundiste todos los barcos!")
                print("\n¡Jugador 2 gana!")
                victorias_jugador2 += 1
                break

            turno = 2 if turno == 1 else 1

        # Imprime la puntuación actual y pregunta si se desea jugar otra partida
        print(
            f"\nPuntuación actual:\nJugador 1: {victorias_jugador1} victorias\nJugador 2: {victorias_jugador2} victorias"
        )

        continuar = input("¿Quieres jugar otra partida? (s/n): ").lower()
        if continuar != "s":
            break
        
juego_batalla_naval()