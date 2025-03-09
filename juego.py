from typing import List
import os
from jugador import Jugador
from red import Red


class Juego:
    def __init__(self, es_servidor: bool, host: str, tamano_tablero: int = 10):
        self.red = Red(es_servidor, host)
        self.jugador_local = Jugador(
            "Jugador Local" if es_servidor else "Jugador Remoto", tamano_tablero
        )
        self.tamanos_barcos = [2, 3]
        self.turno_local = es_servidor  # El servidor empieza

    def iniciar(self):
        self.jugador_local.colocar_barcos_manual(self.tamanos_barcos)
        print("Esperando al otro jugador...")
        self.jugar()

    def jugar(self):
        while True:
            if self.turno_local:
                print(f"Tu turno:")
                self.jugador_local.tablero.mostrar_tableros(
                    self.jugador_local.tablero.matriz,
                    self.jugador_local.tablero_disparos.matriz,
                    "Local",
                    "Disparos",
                )
                fila, columna = self.jugador_local.disparar()
                self.red.enviar({"disparo": f"{chr(columna + ord('A'))}{fila + 1}"})
                resultado = self.red.recibir()["resultado"]
                print(f"Resultado: {resultado}")
                if resultado == "Tocado":
                    self.jugador_local.tablero_disparos.feedback_disparo(
                        fila, columna, self.jugador_local.tablero_disparos.matriz, True
                    )
                else:
                    self.jugador_local.tablero_disparos.feedback_disparo(
                        fila, columna, self.jugador_local.tablero_disparos.matriz, False
                    )

            else:
                print("Turno del oponente:")
                data = self.red.recibir()
                disparo = data["disparo"]
                columna = ord(disparo[0]) - ord("A")
                fila = int(disparo[1:]) - 1
                resultado = self.jugador_local.tablero.recibir_disparo(
                    fila, columna, self.jugador_local.tablero.matriz
                )
                print(f"Oponente disparó a {disparo}: {resultado}")
                self.red.enviar({"resultado": resultado})
                hundidos = self.jugador_local.verificar_hundimientos()
                if len(hundidos) == len(self.tamanos_barcos):
                    print("¡Todos tus barcos fueron hundidos! Has perdido.")
                    self.red.enviar({"resultado": "Hundido"})
                    break

            self.turno_local = not self.turno_local
        print("Juego terminado")
        os.system("pause")

    def cerrar(self):
        self.red.cerrar()
