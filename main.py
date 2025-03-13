import os

from dotenv import load_dotenv

from juego import Juego

load_dotenv()


def main():

    while True:
        modo = input("¿Eres el servidor? (s/n): ").lower()
        if modo == "s":
            try:
                juego = Juego(es_servidor=True, host="0.0.0.0")
            except Exception as e:
                print(e)
                continue
        elif modo == "n":
            host = input("Introduce la IP del servidor: ")
            try:
                juego = Juego(es_servidor=False, host=host)
            except Exception as e:
                print(e)
                continue
        else:
            print("Opcion no valida!!")
            continue
        try:
            juego.iniciar()
        except Exception as e:
            print("Juego terminado", e)
        finally:
            juego.cerrar()
            break


if __name__ == "__main__":
    main()