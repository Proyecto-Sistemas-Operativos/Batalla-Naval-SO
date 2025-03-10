from enum import Enum 

class TipoBarco(Enum):
    PORTAAVIONES = 4
    ACORAZADO = 3
    CRUCERO = 2
    DESTRUCTOR = 1

class Barco:
    def __init__(self, tipo: TipoBarco, fila: int, columna: int, orientacion: str):
        self.tipo = tipo
        self.tamano = tipo.value
        self.fila = fila
        self.columna = columna
        self.orientacion = orientacion
        self.hundido = False

    def posiciones(self):
        if self.orientacion == "H":
            return [(self.fila, self.columna + i) for i in range(self.tamano)]
        return [(self.fila + i, self.columna) for i in range(self.tamano)]
