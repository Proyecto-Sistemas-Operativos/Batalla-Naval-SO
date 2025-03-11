class Tablero:
    def __init__(self, tamano: int):
        self.tamano = tamano
        self.matriz = [["~"] * tamano for _ in range(tamano)]
        self.barcos = []

    # Muestra el tablero
    def mostrar(self):
        for fila in self.matriz:
            print(fila)

    # Muestra los tableros de barcos y disparos
    def mostrar_tableros(self, tablero1, tablero2, tipo1, tipo2):
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

    # Verifica si una posición está dentro del tablero
    def esta_dentro(self, fila: int, columna: int) -> bool:
        return 0 <= fila < self.tamano and 0 <= columna < self.tamano

    # Verifica si una posición está libre para colocar un barco
    def esta_libre(self, fila: int, columna: int, tamano: int, orientacion: str) -> bool:
        if orientacion == "H":
            if columna + tamano > self.tamano:
                return False
            return all(self.matriz[fila][columna + i] == "~" for i in range(tamano))
        else:  # 'V'
            if fila + tamano > self.tamano:
                return False
            return all(self.matriz[fila + i][columna] == "~" for i in range(tamano))

    # Coloca un barco en el tablero
    # Se actualiza la matriz y se guarda la posición de cada parte del barco en la lista de barcos
    def colocar_barco(self, fila: int, columna: int, tamano: int, orientacion: str):
        posiciones = []
        if orientacion == "H":
            for i in range(tamano):
                self.matriz[fila][columna + i] = "B"
                posiciones.append((fila, columna + i))
        else:  # 'V'
            for i in range(tamano):
                self.matriz[fila + i][columna] = "B"
                posiciones.append((fila + i, columna))
        self.barcos.append(posiciones)

    # Compara la posición del disparo con la posición de los barcos
    def recibir_disparo(self, fila: int, columna: int) -> str:
        # Si la posición del disparo coincide con la posición de un barco, se cambia el valor de la matriz en esa posición a "X"
        if self.matriz[fila][columna] == "B":
            self.matriz[fila][columna] = "X"
            if self.verificar_hundimiento(fila, columna):
                return "Hundido"
            return "Impacto"
        # Si no hay barco en la posición, se cambia el valor de la matriz en esa posición a "O"
        elif self.matriz[fila][columna] == "~":
            self.matriz[fila][columna] = "O"
            return "Fallo"
        return "Ya disparado"  # Si ya se disparó en esa posición

    # Verifica si un barco fue hundido
    # Se recorre la lista de barcos y se verifica si todas las posiciones de un barco tienen el valor "X" en la matriz
    def verificar_hundimiento(self, fila: int, columna: int) -> bool:
        for barco in self.barcos:
            if (fila, columna) in barco:
                if all(self.matriz[f][c] == "X" for f, c in barco):
                    return True
        return False