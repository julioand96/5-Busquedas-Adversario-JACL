"""
El juego del gato para ilustrar los modelos de juegos

"""

from juegos_simplificado import ModeloJuegoZT2
from juegos_simplificado import juega_dos_jugadores
from juegos_simplificado import minimax
from minimax import jugador_negamax

class UltimateTicTacToe(ModeloJuegoZT2):
    """
    El juego de Ultimate Tic Tac Toe
    """

    def inicializa(self):
        """
        Inicializa el estado del juego Ultimate Tic Tac Toe.
        """
        tableros = tuple(tuple(9 * [0]) for _ in range(9))  # 9 tableros pequeños vacíos como tuplas
        siguiente_tablero = None  # Al inicio, el jugador puede elegir cualquier tablero
        return (tableros, siguiente_tablero), 1  # Estado y jugador inicial

    def jugadas_legales(self, s, j):
        """
        Devuelve una lista de jugadas legales para el jugador j en el estado s.
        """
        tableros, siguiente_tablero = s
        jugadas = []

        if siguiente_tablero is not None:
            # Revisar jugadas legales en el tablero pequeño correspondiente
            if any(celda == 0 for celda in tableros[siguiente_tablero]):
                jugadas = [(siguiente_tablero, posicion) for posicion in range(9) if tableros[siguiente_tablero][posicion] == 0]
        else:
            # Si no hay restricción, buscar en todos los tableros pequeños
            for tablero_idx, tablero in enumerate(tableros):
                if any(celda == 0 for celda in tablero):
                    jugadas.extend([(tablero_idx, posicion) for posicion in range(9) if tablero[posicion] == 0])

        return jugadas

    def transicion(self, s, a, j):
        """
        Devuelve el estado que resulta de realizar la jugada a en el estado s para el jugador j.
        """
        tableros, _ = s
        tablero_idx, posicion = a

        # Actualizar el tablero pequeño correspondiente
        nuevo_tablero = list(tableros[tablero_idx])
        nuevo_tablero[posicion] = j
        nuevo_tableros = list(tableros)
        nuevo_tableros[tablero_idx] = tuple(nuevo_tablero)

        # Determinar el siguiente tablero pequeño
        siguiente_tablero = posicion if any(celda == 0 for celda in nuevo_tableros[posicion]) else None

        return (tuple(nuevo_tableros), siguiente_tablero)

    def terminal(self, s):
        """
        Devuelve True si es terminal el estado actual.
        """
        tableros, _ = s

        # Verificar si alguien ganó el tablero grande
        tablero_grande = [self.ganancia_tablero(tablero) for tablero in tableros]
        if self.ganancia_tablero(tablero_grande) != 0:
            return True

        # Verificar si todos los tableros pequeños están completos
        if all(all(celda != 0 for celda in tablero) for tablero in tableros):
            return True

        return False

    def ganancia(self, s):
        """
        Devuelve la ganancia para el jugador 1 en el estado terminal s.
        """
        tableros, _ = s

        # Verificar si alguien ganó el tablero grande
        tablero_grande = [self.ganancia_tablero(tablero) for tablero in tableros]
        return self.ganancia_tablero(tablero_grande)

    def ganancia_tablero(self, tablero):
        """
        Devuelve la ganancia para un tablero pequeño.
        """
        if tablero[0] == tablero[1] == tablero[2] != 0:
            return tablero[0]
        if tablero[3] == tablero[4] == tablero[5] != 0:
            return tablero[3]
        if tablero[6] == tablero[7] == tablero[8] != 0:
            return tablero[6]
        if tablero[0] == tablero[3] == tablero[6] != 0:
            return tablero[0]
        if tablero[1] == tablero[4] == tablero[7] != 0:
            return tablero[1]
        if tablero[2] == tablero[5] == tablero[8] != 0:
            return tablero[2]
        if tablero[0] == tablero[4] == tablero[8] != 0:
            return tablero[0]
        if tablero[2] == tablero[4] == tablero[6] != 0:
            return tablero[2]
        return 0 
    
def pprint_gato(s):
    """
    Imprime el estado completo del juego de Ultimate Tic Tac Toe.
    """
    tableros, _ = s  # Extraer los tableros pequeños del estado
    filas = []

    # Construir las filas del tablero grande
    for fila in range(3):  # Hay 3 filas de tableros pequeños
        for subfila in range(3):  # Cada tablero pequeño tiene 3 filas
            linea = []
            for col in range(3):  # Hay 3 tableros pequeños por fila
                tablero_idx = fila * 3 + col
                tablero = tableros[tablero_idx]
                # Extraer la subfila del tablero pequeño con índices locales
                linea.append(
                    ' | '.join(
                        [' X ' if x == 1 else ' O ' if x == -1 else str(i).center(3)
                         for i, x in enumerate(tablero[subfila * 3:(subfila + 1) * 3], start=subfila * 3)]
                    )
                )
            filas.append('   ||   '.join(linea))
        if fila < 2:  # Separador entre filas de tableros pequeños
            filas.append('===' * 20)

    # Imprimir el tablero completo
    print('\n'.join(filas))
    
def jugador_manual_gato(juego, s, j):
    """
    Jugador manual para el juego del gato.
    """
    jugada = None
    print("Estado actual:")
    pprint_gato(s)
    print("Jugador:", j)
    jugadas = juego.jugadas_legales(s, j)
    print("Jugadas legales:", jugadas)
    while jugada not in jugadas:
        try:
            entrada = input("Jugada (formato: tablero, posición): ")
            jugada = tuple(map(int, entrada.split(',')))  # Convertir la entrada en una tupla de dos enteros
        except ValueError:
            print("Entrada inválida. Asegúrate de usar el formato: tablero, posición.")
    return jugada

def jugador_minimax_gato(juego, s, j):
    """
    Jugador minimax para el juego del gato

    """
    return minimax(juego, s, j)

def evalua_ultimatettt(s, jugador):
    """
    Evalúa el estado del tablero de Ultimate Tic Tac Toe favoreciendo bloqueos al oponente
    y oportunidades de ganar.

    Parámetros:
    -----------
    s : tuple
        Estado del tablero (lista de 9 tableros pequeños representados como tuplas).
    jugador : int
        Jugador actual (1 para jugador 1, -1 para jugador 2).

    Retorna:
    --------
    float
        Valor heurístico del estado del tablero.
    """
    oponente = -jugador
    valor = 0

    # Evaluar cada tablero pequeño
    for tablero in s[0]:
        # Evaluar líneas en el tablero pequeño
        for i in range(3):
            # Filas
            linea = [tablero[3 * i], tablero[3 * i + 1], tablero[3 * i + 2]]
            valor += evalua_linea(linea, jugador, oponente)
            # Columnas
            linea = [tablero[i], tablero[i + 3], tablero[i + 6]]
            valor += evalua_linea(linea, jugador, oponente)
        # Diagonales
        linea = [tablero[0], tablero[4], tablero[8]]
        valor += evalua_linea(linea, jugador, oponente)
        linea = [tablero[2], tablero[4], tablero[6]]
        valor += evalua_linea(linea, jugador, oponente)

    # Evaluar el tablero grande
    tablero_grande = [ganancia_tablero(tablero) for tablero in s[0]]
    for i in range(3):
        # Filas
        linea = [tablero_grande[3 * i], tablero_grande[3 * i + 1], tablero_grande[3 * i + 2]]
        valor += evalua_linea(linea, jugador, oponente)
        # Columnas
        linea = [tablero_grande[i], tablero_grande[i + 3], tablero_grande[i + 6]]
        valor += evalua_linea(linea, jugador, oponente)
    # Diagonales
    linea = [tablero_grande[0], tablero_grande[4], tablero_grande[8]]
    valor += evalua_linea(linea, jugador, oponente)
    linea = [tablero_grande[2], tablero_grande[4], tablero_grande[6]]
    valor += evalua_linea(linea, jugador, oponente)

    return valor


def evalua_linea(linea, jugador, oponente):
    """
    Evalúa una línea (fila, columna o diagonal) para un tablero pequeño o grande.

    Parámetros:
    -----------
    linea : list
        Línea a evaluar (3 elementos).
    jugador : int
        Jugador actual (1 para jugador 1, -1 para jugador 2).
    oponente : int
        Jugador oponente (-1 para jugador 1, 1 para jugador 2).

    Retorna:
    --------
    int
        Valor heurístico de la línea.
    """
    if linea.count(jugador) == 2 and linea.count(0) == 1:
        return 10  # Oportunidad de ganar
    if linea.count(oponente) == 2 and linea.count(0) == 1:
        return -8  # Bloqueo al oponente
    if linea.count(jugador) == 1 and linea.count(0) == 2:
        return 1  # Jugada favorable
    if linea.count(oponente) == 1 and linea.count(0) == 2:
        return -1  # Jugada desfavorable
    return 0


def ganancia_tablero(tablero):
    """
    Determina el ganador de un tablero pequeño.

    Parámetros:
    -----------
    tablero : tuple
        Tablero pequeño (9 posiciones).

    Retorna:
    --------
    int
        1 si el jugador 1 ganó, -1 si el jugador 2 ganó, 0 si no hay ganador.
    """
    for i in range(3):
        # Filas
        if tablero[3 * i] == tablero[3 * i + 1] == tablero[3 * i + 2] != 0:
            return tablero[3 * i]
        # Columnas
        if tablero[i] == tablero[i + 3] == tablero[i + 6] != 0:
            return tablero[i]
    # Diagonales
    if tablero[0] == tablero[4] == tablero[8] != 0:
        return tablero[0]
    if tablero[2] == tablero[4] == tablero[6] != 0:
        return tablero[2]
    return 0

def juega_gato(jugador='X'):
    """
    Juega el juego del gato

    """
    if jugador not in ['X', 'O']:
        raise ValueError("El jugador solo puede tener los valores 'X' o 'O'")
    juego = UltimateTicTacToe()
    
    print("El juego del gato")
    print(f"Las 'X' siempre empiezan y tu juegas con {jugador}")
    
    profundidad = 3  # Define la profundidad deseada aquí
    
    if jugador == 'X':
        g, s = juega_dos_jugadores(juego, jugador_manual_gato, 
                                   lambda juego, estado, jugador: jugador_negamax(juego, estado, jugador, d=profundidad, evalua=lambda s: evalua_ultimatettt(s, jugador)))
    else:
        g, s = juega_dos_jugadores(juego, 
                                   lambda juego, estado, jugador: jugador_negamax(juego, estado, jugador, d=profundidad, evalua=lambda s: evalua_ultimatettt(s, jugador)), 
                                   jugador_manual_gato)
        
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