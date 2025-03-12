import socket
import threading
import sys

HOST = '127.0.0.1'
PORT = 10101  # Puerto actualizado a 10101

class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((HOST, PORT))
        print("Conectado al servidor. Escribe 'exit' para salir.")

    def listen_for_messages(self):
        """Escucha mensajes del servidor en un hilo separado."""
        try:
            while True:
                message = self.client.recv(1024).decode()
                if not message:
                    break
                print("\n" + message + "\n> ", end="", flush=True)  # Muestra el mensaje sin romper la entrada
        except:
            pass

    def send_messages(self):
        """Maneja la entrada del usuario y envía mensajes al servidor."""
        try:
            while True:
                message = input("> ")
                if message.lower() == "exit":
                    print("Desconectando del servidor...")
                    self.client.send(message.encode())
                    break
                self.client.send(message.encode())
        except KeyboardInterrupt:
            print("\nCliente cerrado con Ctrl + C.")
        finally:
            self.client.close()
            print("Cliente desconectado correctamente.")
            sys.exit()

    def run(self):
        """Inicia el cliente con hilos para enviar y recibir mensajes simultáneamente."""
        receive_thread = threading.Thread(target=self.listen_for_messages, daemon=True)
        receive_thread.start()
        self.send_messages()

if __name__ == "__main__":
    client = Client()
    client.run()
