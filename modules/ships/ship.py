class Ship:
    def __init__(self, name, size, coordinates = []):
        self.name = name
        self.size = size
        self.coordinates = coordinates
        self.sunkCoordinates = []

    def receiveHit(self, coordinate):
        if coordinate in self.sunkCoordinates:
            print(f"¡Ya habías destruido una parte de la flota en la coordenada '{coordinate}!")
            return False

        self.sunkCoordinates.append(coordinate)
        return True

    def setCoordinates(self, coordinates):
        self.coordinates = coordinates

    def isSunk(self):
        return len(self.sunkCoordinates) == len(self.size)