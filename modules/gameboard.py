import re

class Gameboard:
	def __init__(self, boardSize):
		self.size = boardSize
		self.ships = []

	# Utilidades.

	def getIndexes(self, coordinate):
		if len(coordinate) > 2:
			print(f"Error: la coordenada '{coordinate}'' no es válida.")
			return None

		return { "column": ord(coordinate[0].upper()) - ord('A'), "row": int(coordinate[1]) - 1 }

	def compoundCoordinate(self, rowIndex, columnIndex):
		return f"{str(rowIndex)}{str(columnIndex)}"

	def checkCoordinate(self, coordinate):
		return bool(re.search(r"^\d+$", coordinate[1:])) and bool(re.search(r"^[a-zA-Z]$", coordinate[0]))

	def searchShipByCoordinate(self, coordinate):
		for ship in self.ships:
			if coordinate in ship.coordinates:
				return ship

		return None

	# Métodos que serán usados fuera de la clase.

	def locateShip(self, direction, baseCoordinate, ship):
		# Verificar que sea proporcionado una coordenada válida.
		if not self.checkCoordinate(baseCoordinate):
			print(f"Error: no se proporcionó una coordenada válida")
			return False

		# Verificar que sea proporcionado una dirección válida.
		if direction.upper() not in ["H", "V"]:
			print(f"Error: no se proporcionó una dirección válida")
			return False

		_direction = direction.upper()
		coordIndexes = self.getIndexes(baseCoordinate)
		targetIndex = coordIndexes["column"] if _direction == 'H' else coordIndexes["row"]

		# Verificar si el espacio en el tablero es suficiente dada la coordenada y orientación de la flota.
		if targetIndex + ship.size > self.size:
			print(f"Ups! La flota no entra en esa coordenada, no hay espacio suficiente en el tablero.")
			return False

		# Verificar si existe un barco en la coordenada dada.
		if self.searchShipByCoordinate(baseCoordinate) is not None:
			print(f"Ups! Ya hay una flota ubicada en esa coordenada, intenta en un lugar diferente.")
			return False

		# Se componen las coordenadas que usa el barco.
		for i in range(ship.size):
			if _direction == 'H':
				column = chr(ord(baseCoordinate[0].upper()) + i)
				row = baseCoordinate[1:]
			else:
				column = baseCoordinate[0].upper()
				row = str(int(baseCoordinate[1:]) + i)
			ship.coordinates.append(self.compoundCoordinate(row, column))

		self.ships.append(ship)
		return True

	def hitCoordinate(self, coordinate):
		# Verificar si la bala no acertó en una coordenada donde haya alguna flota.
		if not any(coordinate in coordinates for ship in self.ships for coordinates in ship.coordinates):
			print(f"¡SCUISH! No le has atinado a nada, la bala se hundió en la profundidades.")
			return False

		return self.searchShipByCoordinate(coordinate).receiveHit(coordinate);

	def isAllShipsAlreadyDestoyed(self):
		return all(ship.isSunk() for ship in self.ships)

	def display(self, hideShips=True):
		sunkCoordinates = [sunkCoordinates for ship in self.ships for sunkCoordinates in ship.sunkCoordinates for coordinate in sunkCoordinates]
		
		# Ciclo de las filas.
		#for f in range(self.size):
			# Ciclo de las columnas.
			#for c in range(self.size):