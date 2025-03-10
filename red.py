import socket
import json

class Red:
    def __init__(self, es_servidor: bool, host: str = '0.0.0.0', port: int = 5000):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.es_servidor = es_servidor
        self.host = host
        self.port = port
        self.conn = None
        if es_servidor:
            self.iniciar_servidor()
        else:
            self.iniciar_cliente()

    def iniciar_servidor(self):
        try:
            self.socket.bind((self.host, self.port))
            self.socket.listen(1)
            print(f"Servidor escuchando en {self.host}:{self.port}")
            self.conn, addr = self.socket.accept()
            print(f"Conectado por {addr}")
        except Exception as e:
            print(f"Error al iniciar el servidor: {e}")

    def iniciar_cliente(self):
        try:
            self.socket.connect((self.host, self.port))
            self.conn = self.socket
            print(f"Conectado al servidor {self.host}:{self.port}")
        except Exception as e:
            print(f"Error al conectar al servidor: {e}")

    def enviar(self, datos: dict):
        try:
            self.conn.send(json.dumps(datos).encode())
            print(f"Datos enviados: {datos}")
        except Exception as e:
            print(f"Error al enviar datos: {e}")

    def recibir(self) -> dict:
        try:
            data = self.conn.recv(1024).decode()
            print(f"Datos recibidos: {data}")
            return json.loads(data)
        except Exception as e:
            print(f"Error al recibir datos: {e}")
            return {}

    def cerrar(self):
        try:
            if self.conn:
                self.conn.close()
            self.socket.close()
            print("Conexión cerrada")
        except Exception as e:
            print(f"Error al cerrar la conexión: {e}")