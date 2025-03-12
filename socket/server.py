import socket
import threading

address = ('127.0.0.1', 10101)

class Game:
    def __init__(self):
        self.game = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.game.settimeout(1.0)
        self.game.bind(address)
        self.game.listen(5)

        # Esta variable almacena la conexión de los dos jugadores.
        self.players = []

        # Usamos esta variable para terminar la ejecución del juego.
        self.playing = True

        print(f"¡Preparando Batalla!")

    def broadcast(self, message, sender_socket):
        for client in self.players:
            if client != sender_socket:
                try:
                    client.send(message.encode())
                except:
                    self.players.remove(client)

    def handle_client(self, conn, addr):
        self.players.append(conn)
        try:
            while True:
                data = conn.recv(1024).decode()
                if not data or data.lower() == "exit":
                    print(f"Cliente {addr} desconectado.")
                    break
                print(f"Cliente {addr}: {data}")
                self.broadcast(f"Cliente {addr}: {data}", conn)
        except (ConnectionResetError, BrokenPipeError):
            print(f"Conexión cerrada por el cliente {addr}.")
        finally:
            self.players.remove(conn)
            conn.close()

    def run(self):
        """Ejecuta el servidor y maneja múltiples clientes."""
        try:
            while self.playing:
                try:
                    conn, addr = self.game.accept()
                    client_thread = threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True)
                    client_thread.start()
                except socket.timeout:
                    pass  # Evita bloqueos y permite cerrar con Ctrl + C
        except KeyboardInterrupt:
            print("\nServidor detenido con Ctrl + C.")
            self.playing = False
        finally:
            self.game.close()
            print("Servidor cerrado correctamente.")

if __name__ == "__main__":
    game = Game()
    game.run()
