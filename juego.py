from typing import List
import os
from jugador import Jugador
from red import Red
from barco import Barco  

class Juego:
    def __init__(self, es_servidor: bool, host: str, tamano_tablero: int = 10):
        self.red = Red(es_servidor, host)
        self.jugador_local = Jugador(
            "Jugador Local" if es_servidor else "Jugador Remoto", tamano_tablero
        )
        self.tamanos_barcos = [4, 3, 2, 1]  # PORTAAVIONES ACORAZADO CRUCERO DESTRUCTOR
        self.turno_local = es_servidor  # El servidor empieza
        self.cantidad_barcos_enemigos = len(self.tamanos_barcos)  # Cantidad de barcos enemigos

    def iniciar(self):
        self.jugador_local.colocar_barcos_manual()
        print("Esperando al otro jugador...")
        if self.turno_local:
            self.red.enviar({"cantidad_barcos": self.cantidad_barcos_enemigos})
        else:
            data = self.red.recibir()
            self.cantidad_barcos_enemigos = data.get("cantidad_barcos")
        self.jugar()

    def jugar(self):
        while True:
            try:
                if self.turno_local:
                    print("Tu turno:")
                    self.jugador_local.tablero.mostrar_tableros(
                        self.jugador_local.tablero.matriz,
                        self.jugador_local.tablero_disparos.matriz,
                        "Local",
                        "Disparos",
                    )

                    # Disparo del jugador solo una vez
                    fila, columna = self.jugador_local.disparar()
                    self.jugador_local.tablero_disparos.matriz[fila][columna] = "O"
                    self.jugador_local.tablero.mostrar_tableros(
                        self.jugador_local.tablero.matriz,
                        self.jugador_local.tablero_disparos.matriz,
                        "Local",
                        "Disparos",
                    )

                    # Enviar disparo y recibir resultado
                    self.red.enviar({"disparo": f"{chr(columna + ord('A'))}{fila + 1}"})
                    data = self.red.recibir()
                    resultado = data.get("resultado")
                    if resultado is None:
                        raise ValueError("No se recibió el resultado del disparo")
                    print(f"Resultado: {resultado}")

                    # Actualizar tablero
                    if resultado == "Impacto":
                        self.jugador_local.tablero_disparos.matriz[fila][columna] = "X"
                        if self.jugador_local.tablero.verificar_hundimiento(fila, columna):
                            print("¡Hundiste un barco!")
                            self.red.enviar({"resultado": "Hundido"})
                        else:
                            print("No se hundió el barco todavía.")
                        # Si acierta, se queda el turno
                        continue
                    elif resultado == "Hundido":
                        self.jugador_local.tablero_disparos.matriz[fila][columna] = "X"
                        print("¡Hundiste un barco!")
                        # Registrar el hundimiento del barco enemigo
                        self.jugador_local.barcos_enemigos.append(Barco(None, fila, columna, None, hundido=True))
                        # Tras hundir un barco, verificar si se hundió toda la flota enemiga
                        if len(self.jugador_local.barcos_enemigos) == self.cantidad_barcos_enemigos:
                            print("¡Has hundido toda la flota enemiga! Ganaste.")
                            self.red.enviar({"resultado": "derrotado"})
                            break
                        else:
                            print("Aún no has hundido toda la flota enemiga.")
                        # Si hunde, también sigue disparando
                        continue
                    else:
                        print("Fallo. Pasa el turno.")

                    
                    if len(self.jugador_local.verificar_hundimientos()) == len(self.tamanos_barcos):
                        print("¡Todos tus barcos fueron hundidos! Has perdido.")
                        break

                else:
                    print("Turno del oponente:")
                    data = self.red.recibir()
                    if data.get("resultado") == "derrotado":
                        print("¡Has perdido! Todos tus barcos han sido hundidos.")
                        break
                    disparo = data.get("disparo")
                    if disparo is None:
                        raise ValueError("No se recibió el disparo del oponente")

                    columna = ord(disparo[0]) - ord("A")
                    fila = int(disparo[1:]) - 1
                    resultado = self.jugador_local.tablero.recibir_disparo(fila, columna)
                    self.red.enviar({"resultado": resultado})
                    print(f"Oponente disparó a {disparo}: {resultado}")

                    if resultado in ["Impacto", "Hundido"]:
                        self.jugador_local.tablero.mostrar_tableros(
                            self.jugador_local.tablero.matriz,
                            self.jugador_local.tablero_disparos.matriz,
                            "Local",
                            "Disparos",
                        )
                        # Si hay impacto o hundimiento, oponente repite disparo
                        continue

                    if resultado == "Hundido":
                        # Mensaje de hundimiento del oponente
                        print("¡El oponente hundió uno de tus barcos!")
                        # Verificar si todos tus barcos han sido hundidos
                        if len(self.jugador_local.verificar_hundimientos()) == len(self.tamanos_barcos):
                            print("¡Todos tus barcos fueron hundidos! Has perdido.")
                            break

                # Tras un fallo (local) o fallo (enemigo), se alterna el turno
                self.turno_local = not self.turno_local

            except Exception as e:
                print(f"Error durante el juego: {e}")
                break

        print("Juego terminado")
        os.system("pause")

    def cerrar(self):
        self.red.cerrar()

        #comentario de prueba