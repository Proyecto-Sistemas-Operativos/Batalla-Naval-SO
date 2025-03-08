import random

print("\nBATALLA NAVAL\n")

def crear_tablero(tamano):
    return [['~'] * tamano for _ in range(tamano)]

def imprimir_tableros(tablero1, tablero2, tipo1, tipo2):
    print(f"\n    {tipo1}          {tipo2}\n")
    print("   A B C D E F G H I J        A B C D E F G H I J")
    for idx, (fila1, fila2) in enumerate(zip(tablero1, tablero2)):
        print(f"{idx+1:<2} " + " ".join(fila1) + "     " + f"{idx+1:<2} " + " ".join(fila2))

def colocar_barcos_manual(tablero, tamano, nombre_barco):
    print("-------------\n")
    print("Instrucciones para posicionar")
    print("\nPara posicionar verticalmente se usa: Columna + Fila")
    print("\nPara posicionar horizontalmente se usa: Fila + Columna")
    print("-------------\n")
    while True:
        orientacion = input(f"\nIntroduce la orientación del {nombre_barco} (H para horizontal, V para vertical): ").upper()
        if orientacion not in ['H', 'V']:
            print("Orientación inválida. Por favor, introduce 'H' para horizontal o 'V' para vertical.")
            continue

        posicion = input(f"Introduce la posición inicial del {nombre_barco} (ej. B3): ")

        print(f"POSICION: {posicion}")
        columna = ord(posicion[0].upper()) - ord('A')
        fila = int(posicion[1]) - 1

        if orientacion == 'H':
            if columna + tamano <= len(tablero) and all(tablero[fila][columna + i] == '~' for i in range(tamano)):
                for i in range(tamano):
                    tablero[fila][columna + i] = 'B'
                break
        elif orientacion == 'V':
            if fila + tamano <= len(tablero) and all(tablero[fila + i][columna] == '~' for i in range(tamano)):
                for i in range(tamano):
                    tablero[fila + i][columna] = 'B'
                break
        print("Posición inválida o el espacio ya está ocupado. Inténtalo de nuevo.")

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

def verificar_hundimiento(tablero, tamanos_barcos):
    barcos_hundidos = []
    visitados = set() 

    for tamano in sorted(tamanos_barcos, reverse=True):  
        # Búsqueda horizontal
        for fila_idx, fila in enumerate(tablero):
            for i in range(len(fila) - tamano + 1):
                segmento = [(fila_idx, i + j) for j in range(tamano)]
                if all((fila_idx, i + j) not in visitados and fila[i + j] == 'X' for j in range(tamano)):
                    barcos_hundidos.append(tamano)
                    visitados.update(segmento)  
                    break 

        # Búsqueda vertical
        for col_idx in range(len(tablero[0])):
            for i in range(len(tablero) - tamano + 1):
                segmento = [(i + j, col_idx) for j in range(tamano)]
                if all((i + j, col_idx) not in visitados and tablero[i + j][col_idx] == 'X' for j in range(tamano)):
                    barcos_hundidos.append(tamano)
                    visitados.update(segmento) 
                    break 

    return barcos_hundidos

def juego_batalla_naval():
    tamano = 10
    barcos = [("Portaviones", 4), ("Acorazado", 3), ("Crucero", 2), ("Destructor #1", 1), ("Destructor #2", 1)]
    tamanos_barcos = [4, 3, 2, 1, 1]

    victorias_jugador1 = 0
    victorias_jugador2 = 0

    while True:
        tablero_jugador1_barcos = crear_tablero(tamano)
        tablero_jugador1_disparos = crear_tablero(tamano)
        tablero_jugador2_barcos = crear_tablero(tamano)
        tablero_jugador2_disparos = crear_tablero(tamano)

        print("\nJugador 1, coloca tus barcos.")
        for nombre_barco, tamano in barcos:
            imprimir_tableros(tablero_jugador1_barcos, tablero_jugador1_disparos, "Barcos Jugador 1", "Disparos Jugador 1")
            colocar_barcos_manual(tablero_jugador1_barcos, tamano, nombre_barco)

        print("\nJugador 2, coloca tus barcos.")
        for nombre_barco, tamano in barcos:
            imprimir_tableros(tablero_jugador2_barcos, tablero_jugador2_disparos, "Barcos Jugador 2", "Disparos Jugador 2")
            colocar_barcos_manual(tablero_jugador2_barcos, tamano, nombre_barco)

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
                barcos_hundidos = verificar_hundimiento(tablero_jugador2_barcos, tamanos_barcos)
            else:
                resultado = disparar(tablero_jugador1_barcos, tablero_jugador2_disparos, fila, columna)
                barcos_hundidos = verificar_hundimiento(tablero_jugador1_barcos, tamanos_barcos)

            if resultado is None:
                print("Ya disparaste en esa posición.")
            elif resultado:
                print("\n¡Tocado!")
                #Preguntar 

                for tamano in barcos_hundidos:
                    print(f"¡Has hundido un barco de {tamano}!")
            else:
                print("\n¡Agua!")

            if all(celda != 'B' for fila in tablero_jugador2_barcos for celda in fila):
                print("\n¡Felicidades, hundiste todos los barcos!")
                print("¡Jugador 1 gana!")
                victorias_jugador1 += 1
                break
            elif all(celda != 'B' for fila in tablero_jugador1_barcos for celda in fila):
                print("\n¡Felicidades, hundiste todos los barcos!")
                print("\n¡Jugador 2 gana!")
                victorias_jugador2 += 1
                break

            turno = 2 if turno == 1 else 1

        print(f"\nPuntuación actual:\nJugador 1: {victorias_jugador1} victorias\nJugador 2: {victorias_jugador2} victorias")

        continuar = input("¿Quieres jugar otra partida? (s/n): ").lower()
        if continuar != 's':
            break
            
juego_batalla_naval()
