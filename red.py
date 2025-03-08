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
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        print(f"Servidor escuchando en {self.host}:{self.port}")
        self.conn, addr = self.socket.accept()
        print(f"Conectado por {addr}")

    def iniciar_cliente(self):
        self.socket.connect((self.host, self.port))
        self.conn = self.socket
        print(f"Conectado al servidor {self.host}:{self.port}")

    def enviar(self, datos: dict):
        self.conn.send(json.dumps(datos).encode())

    def recibir(self) -> dict:
        return json.loads(self.conn.recv(1024).decode())

    def cerrar(self):
        if self.conn:
            self.conn.close()
        self.socket.close()