from enum import Enum

class TipoBarco(Enum):
    PORTAAVIONES = 4
    ACORAZADO = 3
    CRUCERO = 2
    DESTRUCTOR = 1

class Barco:
    def __init__(self, tipo: TipoBarco, fila: int, columna: int, orientacion: str, hundido: bool = False):
        self.tipo = tipo
        self.fila = fila
        self.columna = columna
        self.orientacion = orientacion
        self.hundido = hundido

    def posiciones(self):
        posiciones = []
        if self.orientacion == "H":
            for i in range(self.tipo.value):
                posiciones.append((self.fila, self.columna + i))
        else:  # 'V'
            for i in range(self.tipo.value):
                posiciones.append((self.fila + i, self.columna))
        return posiciones