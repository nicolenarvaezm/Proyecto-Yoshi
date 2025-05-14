import random

ROWS, COLS = 8, 8
TILE_SIZE = 60

class YoshiGameLogic:
    def __init__(self):
        self.zonas = self.definir_zonas()
        self.casillas_pintadas = {}
        self.yoshi_verde, self.yoshi_rojo = self.generar_posiciones_iniciales()
        self.turno = 'verde'
        self.zonas_ganadas = {'verde': 0, 'rojo': 0}
        self.zonas_completadas = set()
        self.dificultad = 'Principiante'

    def definir_zonas(self):
        return {
            0: {(0,0), (0,1), (0,2), (1,0), (2,0)},
            1: {(0,5), (0,6), (0,7), (1,7), (2,7)},
            2: {(7,0), (6,0), (5,0), (7,1), (7,2)},
            3: {(7,7), (6,7), (5,7), (7,5), (7,6)},
        }

    def generar_posiciones_iniciales(self):
        zonas = set().union(*self.definir_zonas().values())
        while True:
            verde = (random.randint(0, 7), random.randint(0, 7))
            rojo = (random.randint(0, 7), random.randint(0, 7))
            if verde != rojo and verde not in zonas and rojo not in zonas:
                return verde, rojo

    def movimientos_legales(self, pos):
        movimientos = [(2, 1), (1, 2), (-1, 2), (-2, 1),
                       (-2, -1), (-1, -2), (1, -2), (2, -1)]
        legales = []
        for di, dj in movimientos:
            ni, nj = pos[0] + di, pos[1] + dj
            if 0 <= ni < ROWS and 0 <= nj < COLS:
                if (ni, nj) not in self.casillas_pintadas:
                    legales.append((ni, nj))
        return legales

    def pintar_casilla(self, i, j, color):
        for idx, zona in self.zonas.items():
            if (i, j) in zona:
                self.casillas_pintadas[(i, j)] = color
                self.verificar_zona(idx)
                break

    def verificar_zona(self, idx):
        if idx in self.zonas_completadas:
            return False
        zona = self.zonas[idx]
        conteo = {'verde': 0, 'rojo': 0}
        for pos in zona:
            if pos in self.casillas_pintadas:
                conteo[self.casillas_pintadas[pos]] += 1
        total = conteo['verde'] + conteo['rojo']
        if total >= 3:
            if conteo['verde'] > conteo['rojo']:
                self.zonas_ganadas['verde'] += 1
                self.zonas_completadas.add(idx)
            elif conteo['rojo'] > conteo['verde']:
                self.zonas_ganadas['rojo'] += 1
                self.zonas_completadas.add(idx)
            return True
        return False

    def fin_juego(self):
        return sum(self.zonas_ganadas.values()) == len(self.zonas)

    def obtener_ganador(self):
        if self.zonas_ganadas['verde'] > self.zonas_ganadas['rojo']:
            return 'verde'
        elif self.zonas_ganadas['rojo'] > self.zonas_ganadas['verde']:
            return 'rojo'
        return 'empate'