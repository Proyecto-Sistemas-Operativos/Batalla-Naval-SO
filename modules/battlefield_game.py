class GameBoard:
    def __init__(self, squareSize):
        self.size = squareSize
        self.boardPositions = []
        self.shipsPositions = []

        ## Composicion del tablero
        for _ in range(self.size):
            fila = []

            for __ in range(self.size):
                fila.append("-")

            self.boardPositions.append(fila)

    def display(self):
        for boardRow in self.boardPositions:
            print(" ".join(boardRow))

    def 