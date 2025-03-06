import gameboard
from ships.cruiser import Cruiser
from ships.battleship import Battleship
from ships.destroyer import Destroyer
from ships.aircraft_carrier import AircraftCarrier

class BattlefieldGame:
	def __init__(self):
		self.playerA = None
		self.playerB = None
		