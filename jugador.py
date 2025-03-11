from typing import List
from barco import Barco, TipoBarco
from tablero import Tablero

# Clase que representa un jugador
# El jugador tiene un nombre, un tablero de barcos y un tablero de disparos
# También tiene una lista de sus barcos y una lista de los barcos enemigos
class Jugador:
    def __init__(self, nombre: str, tamano_tablero: int):
        self.nombre = nombre
        self.tablero = Tablero(tamano_tablero)
        self.tablero_disparos = Tablero(tamano_tablero)
        self.barcos = []
        self.barcos_enemigos = []  # Lista para registrar los barcos enemigos

    # Coloca los barcos manualmente en el tablero
    # Se pide al jugador que introduzca la orientación y la posición inicial de cada barco
    def colocar_barcos_manual(self):
        tipos_barcos = [TipoBarco.PORTAAVIONES, TipoBarco.ACORAZADO, TipoBarco.CRUCERO, TipoBarco.DESTRUCTOR]

        # Colocar cada barco en el tablero
        for tipo in tipos_barcos:
            print(f"\nColocando {tipo.name} (Tamaño {tipo.value}) para {self.nombre}")
            while True:
                # Pedir orientación y posición inicial
                orientacion = input("Orientación (H/V): ").upper()
                if orientacion not in ["H", "V"]:
                    print("Usa 'H' o 'V'.")
                    continue
                # Pedir posición inicial
                posicion = input("Posición inicial (ej. B3): ").upper()

                # Verifica que la posición sea válida, que no esté ocupada y/o que quepa el barco
                if (
                    len(posicion) < 2
                    or not posicion[0].isalpha()
                    or not posicion[1:].isdigit()
                ):
                    print("Formato inválido (ej. B3).")
                    continue
                columna = ord(posicion[0]) - ord("A")
                fila = int(posicion[1:]) - 1
                if not self.tablero.esta_dentro(fila, columna):
                    print("Fuera del tablero.")
                    continue
                if self.tablero.esta_libre(fila, columna, tipo.value, orientacion):
                    self.tablero.colocar_barco(fila, columna, tipo.value, orientacion)
                    self.barcos.append(Barco(tipo, fila, columna, orientacion))
                    break
                print("Espacio ocupado o no cabe.")
            self.tablero.mostrar_tableros(
                self.tablero.matriz,
                self.tablero_disparos.matriz,
                "Barcos Jugador 1",
                "Disparos Jugador 1",
            )

    # Dispara a una posición del tablero enemigo
    # Se pide al jugador que introduzca la posición del disparo
    def disparar(self) -> tuple[int, int]:
        while True:
            disparo = input(f"{self.nombre}, introduce disparo (ej. B3): ").upper()
            # Verifica que la posición de disparo sea válida
            if (
                len(disparo) < 2
                or not disparo[0].isalpha()
                or not disparo[1:].isdigit()
            ):
                print("Formato inválido.")
                continue
            # Convierte la posición de disparo a fila y columna
            columna = ord(disparo[0]) - ord("A")
            fila = int(disparo[1:]) - 1
            if self.tablero.esta_dentro(fila, columna):
                return fila, columna
            print("Fuera del tablero.")

    # Verifica si hay barcos enemigos en las posiciones de los disparos
    def verificar_hundimientos(self) -> List[int]:
        barcos_hundidos = []
        for barco in self.barcos:
            posiciones = barco.posiciones()
            # Si un barco enemigo está en una posición de disparo, se marca con una 'X'
            if all(self.tablero.matriz[f][c] == "X" for f, c in posiciones):
                barcos_hundidos.append(barco.tipo.value) 
                barco.hundido = True
        return barcos_hundidos
