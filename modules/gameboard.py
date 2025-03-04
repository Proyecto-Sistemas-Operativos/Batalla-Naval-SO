import re

class Gameboard:
    def __init__(self, boardSize):
        self.size = boardSize
        self.ships = []

    def getIndexes(self, coordinate):
    	if len(coordinate) > 2:
    		return print(f"Error: la coordenada '{coordinate}'' no es válida.")

    	return { column: ord(coordinate[0].upper()) - ord('A'), row: int(coordinate[1]) - 1 }

    def compoundCoordinate(self, rowIndex, columnIndex):
    	return f"{rowIndex}{columnIndex}"

    def cleanCoordinate(self, coordinate):
    	return bool(re.search(r"^\d+$", coordinate[1:])) and bool(re.search(r"^[a-zA-Z]$", coordinate[0]))

    def searchShipByCoordinate(self, coordinate):
    	for ship in self.ships:
    		if coordinate in ship.coordinates:
    			return ship

    	return None

    def locateShip(self, direction, baseCoordinate, ship):
		# Verificar que sea proporcionado una coordenada válida.
    	if self.checkCoordinate(baseCoordinate):
    		print(f"Error: no se proporcionó una coordenada válida")
    		return False
		# Verificar que sea proporcionado una dirección válida.
    	if direction.upper() not in ["H", "V"]:
    		print(f"Error: no se proporcionó una dirección válida")
    		return False

    	_direction = direction.upper()
    	coordIndexes = self.getIndexes()
		targetIndex = coordIndexes.column if _direction == 'H' else coordIndexes.row if _direction == 'V'

    	# Verificar si el espacio en el tablero es suficiente dada la coordenada y orientación de la flota.
        if targetIndex + ship.size > self.size:
        	print(f"Ups! La flota no entra en esa coordenada, no hay espacio suficiente en el tablero.")
        	return False

		# Verificar si existe un barco en la coordenada dada.
        if searchShipByCoordinate(baseCoordinate) != None:
        	print(f"Ups! Ya hay una flota ubicada en esa coordenada, intenta en un lugar diferente.")
        	return False

        # Se componen las coordenadas que usa el barco.
        for i in range(ship.size):
        	column = ord(baseCoordinate[0].upper())
        	column = chr(column + i) if _direction == 'H' else column
        	row = baseCoordinate[1:]
        	row = int(row + i) if _direction == 'V' else row

			ship.coordinates.append(self.compoundCoordinate(row, column))

		self.ships.append(ship)

	def hitCoordinate(self, coordinate):
		# Verificar si la bala acertó en una coordenada donde hay parte sin destruir de alguna flota.
		if coordinate not in [coordinates for ship in self.ships for coordinates in ship.coordinates]:
			print(f"¡SCUISH! No le has atinado a nada, la bala se hundió en la profundidades.")
			return False

		return self.searchShipByCoordinate(coordinate).receiveHit(coordinate);

	def areUndestroyedShipsRemaining():
		return all(ship.isSunk() for ship in self.ships)