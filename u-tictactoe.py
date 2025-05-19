"""
El juego del gato para ilustrar los modelos de juegos

"""

from juegos_simplificado import ModeloJuegoZT2
from juegos_simplificado import juega_dos_jugadores
from juegos_simplificado import minimax
from minimax import jugador_negamax

class Gato(ModeloJuegoZT2):
    """
    El juego del gato 

    """
    def inicializa(self):
        """
        Inicializa el estado del juego Ultimate Tic Tac Toe.
        """
        estado = [tuple(9 * [0]) for _ in range(9)]  # 9 tableros pequeños vacíos
        siguiente_tablero = None  # Al inicio, el jugador puede elegir cualquier tablero
        return (estado, siguiente_tablero, 1)  # Estado, tablero siguiente, jugador inicial
    
    def jugadas_legales(self, s, j):
        """
        Devuelve una lista de jugadas legales para el jugador j en el estado s.
        """
        estado, siguiente_tablero, _ = s
        jugadas = []

        if siguiente_tablero is not None:
            # Revisar jugadas legales en el tablero pequeño correspondiente
            if any(celda == 0 for celda in estado[siguiente_tablero]):
                jugadas = [(siguiente_tablero, posicion) for posicion in range(9) if estado[siguiente_tablero][posicion] == 0]
        else:
            # Si no hay restricción, buscar en todos los tableros pequeños
            for tablero_idx, tablero in enumerate(estado):
                if any(celda == 0 for celda in tablero):
                    jugadas.extend([(tablero_idx, posicion) for posicion in range(9) if tablero[posicion] == 0])

        return jugadas
    
    def transicion(self, s, a, j):
        """
        Devuelve el estado que resulta de realizar la jugada a en el estado s para el jugador j.
        """
        estado, _, _ = s
        tablero_idx, posicion = a

        # Actualizar el tablero pequeño correspondiente
        nuevo_tablero = list(estado[tablero_idx])
        nuevo_tablero[posicion] = j
        nuevo_estado = list(estado)
        nuevo_estado[tablero_idx] = tuple(nuevo_tablero)

        # Determinar el siguiente tablero pequeño
        siguiente_tablero = posicion if any(celda == 0 for celda in nuevo_estado[posicion]) else None

        return (nuevo_estado, siguiente_tablero, -j)
    
    def terminal(self, s):
        """
        Devuelve True si es terminal el estado actual,

        """
        if 0 not in s:
            return True
        if s[0] == s[4] == s[8] != 0:
            return True
        if s[2] == s[4] == s[6] != 0:
            return True
        for i in range(3):
            if s[3 * i] == s[3 * i + 1] == s[3 * i + 2] != 0:
                return True
            if s[i] == s[i + 3] == s[i + 6] != 0:
                return True
        return False

    def ganancia(self, s):
        """
        Devuelve la ganancia para el jugador 1 en el estado terminal s

        """
        if s[0] == s[4] == s[8] != 0:
            return s[0]
        if s[2] == s[4] == s[6] != 0:
            return s[2]
        for i in range(3):
            if s[3 * i] == s[3 * i + 1] == s[3 * i + 2] != 0:
                return s[3 * i]
            if s[i] == s[i + 3] == s[i + 6] != 0:
                return s[i]
        return 0    
    
def pprint_gato(s):
    """
    Imprime el estado del juego del gato

    """
    a = [' X ' if x == 1 else ' O ' if x == -1 else str(i).center(3) 
         for (i, x) in enumerate(s)]
    print(a[0] + '|' + a[1] + '|' + a[2])
    print('---+---+---')
    print(a[3] + '|' + a[4] + '|' + a[5])
    print('---+---+---')
    print(a[6] + '|' + a[7] + '|' + a[8])
    
def jugador_manual_gato(juego, s, j):
    """
    Jugador manual para el juego del gato

    """
    jugada = None
    print("Estado actual:")
    pprint_gato(s)
    print("Jugador:", j)
    jugadas = juego.jugadas_legales(s, j)
    print("Jugadas legales:", jugadas)
    while jugada not in jugadas:
        jugada = int(input("Jugada: "))
    return jugada

def jugador_minimax_gato(juego, s, j):
    """
    Jugador minimax para el juego del gato

    """
    return minimax(juego, s, j)

    
def juega_gato(jugador='X'):
    """
    Juega el juego del gato

    """
    if jugador not in ['X', 'O']:
        raise ValueError("El jugador solo puede tener los valores 'X' o 'O'")
    juego = Gato()
    
    print("El juego del gato")
    print(f"Las 'X' siempre empiezan y tu juegas con {jugador}")
    
    if jugador == 'X':
        #g, s = juega_dos_jugadores(juego, jugador_manual_gato, jugador_minimax_gato)
        g, s = juega_dos_jugadores(juego, jugador_manual_gato, jugador_negamax)
    else:
        #g, s = juega_dos_jugadores(juego, jugador_minimax_gato, jugador_manual_gato)
        g, s = juega_dos_jugadores(juego, jugador_negamax, jugador_manual_gato)
    
    print("\nSE ACABO EL JUEGO\n")
    pprint_gato(s)   
    if g == 0:  
        print("\nY termina con un asqueroso empate")
    elif (g == 1 and jugador == 'X') or (g == -1 and jugador == 'O'):
        print("\nGanaste, debe ser suerte")
    else:
        print("\nPerdiste, no tienes remedio, soy muy superior a un simple mortal")
        
        
if __name__ == '__main__':
    juega_gato('O')