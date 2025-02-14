import random
#Matrices de cada jugador
field_player1 = [["" for col in range(10)] for row in range(10)]
field_player2 = [["" for col in range(10)] for row in range(10)]
#Matrices donde cada jugador lanza los ataques
view_player1 = [[0 for col in range(10)] for row in range(10)]
view_player2 = [[0 for col in range(10)] for row in range(10)]
#Locaciones de cada barco
portaaviones_player1 = [(0,0),(0,0),(0,0),(0,0)]
acorazado_player1 = [(0,0),(0,0),(0,0)]
crucero_player1 = [(0,0),(0,0)]
destructor1_player1 = [(0,0)]
destructor2_player1 = [(0,0)]

portaaviones_player2 = [(0,0),(0,0),(0,0),(0,0)]
acorazado_player2 = [(0,0),(0,0),(0,0)]
crucero_player2 = [(0,0),(0,0)]
destructor1_player2 = [(0,0)]
destructor2_player2 = [(0,0)]

def place_destructor(field):
    return

def place_acorazado(horizontal_o_vertical:bool, field):
    return

def place_crucero(horizontal_o_vertical:bool, field):
    return

def place_portaaviones(horizontal_o_vertical:bool, field):
    return

def populate_fields():
    # Estructura para determinar lo que ocupa cada casilla
    # Ejemplo: "0P". 0 significando que la casilla no ha sido atacada P de portaaviones
    # "1D" casilla ha sido atacada D de destructor
    # "1" casilla ha sido atacada pero no habia ningun barco
    # "" casilla no ha sido atacada ni tiene ningun barco
    
    return


if __name__ == "__main__":
    print(random.random())
    print(field_player1)