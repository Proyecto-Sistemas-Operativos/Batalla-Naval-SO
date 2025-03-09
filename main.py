import os

from dotenv import load_dotenv

from juego import Juego

load_dotenv()


def main():
    modo = input("¿Eres el servidor? (s/n): ").lower() == "s"
    if modo:
        juego = Juego(es_servidor=True, host="0.0.0.0")
    else:
        host = input("Introduce la IP del servidor: ")
        juego = Juego(es_servidor=False, host=str(os.getenv("HOST")))
    try:
        juego.iniciar()
    except Exception as e:
        print("Juego terminado", e)
    finally:
        juego.cerrar()


if __name__ == "__main__":
    main()
