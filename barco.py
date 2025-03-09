class Barco:
    def __init__(self, tamano: int, fila: int, columna: int, orientacion: str):
        self.tamano = tamano
        self.fila = fila
        self.columna = columna
        self.orientacion = orientacion
        self.hundido = False

    def posiciones(self):
        if self.orientacion == "H":
            return [(self.fila, self.columna + i) for i in range(self.tamano)]
        return [(self.fila + i, self.columna) for i in range(self.tamano)]
