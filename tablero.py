from typing import List


class Tablero:
    def __init__(self, tamano: int):
        self.tamano = tamano
        self.matriz = [["~"] * tamano for _ in range(tamano)]

    def mostrar(self):
        for fila in self.matriz:
            print(fila)

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

    def esta_dentro(self, fila: int, columna: int) -> bool:
        return 0 <= fila < self.tamano and 0 <= columna < self.tamano

    def esta_libre(
        self, fila: int, columna: int, tamano: int, orientacion: str
    ) -> bool:
        if orientacion == "H":
            if columna + tamano > self.tamano:
                return False
            return all(self.matriz[fila][columna + i] == "~" for i in range(tamano))
        else:  # 'V'
            if fila + tamano > self.tamano:
                return False
            return all(self.matriz[fila + i][columna] == "~" for i in range(tamano))

    def colocar_barco(self, fila: int, columna: int, tamano: int, orientacion: str):
        if orientacion == "H":
            for i in range(tamano):
                self.matriz[fila][columna + i] = "B"
        else:  # 'V'
            for i in range(tamano):
                self.matriz[fila + i][columna] = "B"

    def recibir_disparo(self, fila: int, columna: int, tablero) -> str:
        if self.matriz[fila][columna] == "B":
            self.matriz[fila][columna] = "X"
            tablero[fila][columna] = "X"
            return "Tocado"
        elif self.matriz[fila][columna] == "~":
            self.matriz[fila][columna] = "O"
            tablero[fila][columna] = "O"
            return "Fallo"
        
    def feedback_disparo(self, fila:int, columna: int, tablero_disparos, hundido: bool):
        if hundido:
            self.matriz[fila][columna] = "X"
            tablero_disparos[fila][columna] = "X"
        else:
            self.matriz[fila][columna] = "O"
            tablero_disparos[fila][columna] = "O"
