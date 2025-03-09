from typing import List

from jugador import Jugador
from red import Red


class Juego:
    def __init__(self, es_servidor: bool, host: str, tamano_tablero: int = 10):
        self.red = Red(es_servidor, host)
        self.jugador_local = Jugador(
            "Jugador Local" if es_servidor else "Jugador Remoto", tamano_tablero
        )
        self.tamanos_barcos = [4,3,2,1] #PORTAAVIONES ACORAZADO CRUCERO DESTRUCTOR
        self.turno_local = es_servidor  # El servidor empieza

    def iniciar(self):
        self.jugador_local.colocar_barcos_manual()
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
                #Obtener disparo del jugador se ejecuta la funcion disparar
                fila, columna = self.jugador_local.disparar()
                #antes de enviar marca con O donde disparo pero no le dio
                self.jugador_local.tablero_disparos.matriz[fila][columna]="O"

                # Mostrar los tableros actualizados para que el jugador lo vea antes de pasar turno
                self.jugador_local.tablero.mostrar_tableros(
                self.jugador_local.tablero.matriz,
                self.jugador_local.tablero_disparos.matriz,
                "Local",
                "Disparos",
                )


                self.red.enviar({"disparo": f"{chr(columna + ord('A'))}{fila + 1}"})
                resultado = self.red.recibir()["resultado"]
                print(f"Resultado: {resultado}")

                #si acerto el disparo, se actualiza el tablero de disparos con self
                if resultado in ["Impacto", "Hundido"]:
                    self.jugador_local.tablero_disparos.matriz[fila][columna] = "X"
                    print("¡Hundiste un barco!")
            else:
                print("Turno del oponente:")
                #recibir disparo del oponente
                data = self.red.recibir()
                disparo = data["disparo"]
                columna = ord(disparo[0]) - ord("A")
                fila = int(disparo[1:]) - 1

                #aqui se van a mostrar los disparos recibidos del oponente en el tablero de barcos solamente
                resultado = self.jugador_local.tablero.recibir_disparo(
                    fila, columna, self.jugador_local.tablero_disparos.matriz
                )

                print(f"Oponente disparó a {disparo}: {resultado}")
                #antes de enviar actualizamos el tablero si el disparo del opo da a un barco marca X y sino con O
                #if resultado in ["Impacto", "Hundido"]:
                    #self.jugador_local.tablero.matriz[fila][columna]="X" #si le dio
                #else:
                    #self.jugador_local.tablero.matriz[fila][columna]="O" #no le dio

                self.red.enviar({"resultado": resultado})

                hundidos = self.jugador_local.verificar_hundimientos()
                if len(hundidos) == len(self.tamanos_barcos):
                    print("¡Todos tus barcos fueron hundidos! Has perdido.")
                    self.red.enviar({"resultado": "Hundido"})
                    break

            self.turno_local = not self.turno_local

    def cerrar(self):
        self.red.cerrar()
