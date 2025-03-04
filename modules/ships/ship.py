class Ship:
    def __init__(self, name, size):
        self.name = name
        self.size = size
        self.coordinates = []
        self.sunkCoordinates = []

    def receive_hit(self, coordinate):
        if coordinate in self.sunkCoordinates:
            print(f"¡La pieza del barco en la coordenada ({coordinate}) ya se encuentra hundida!")
            return False
        
        self.sunkCoordinates.append(coordinate)
        return True

    def is_sunk(self):
        return len(self.sunkCoordinates) == len(self.length)