import tkinter as tk
import random
from PIL import Image, ImageTk

TILE_SIZE = 60
ROWS, COLS = 8, 8
WINDOW_SIZE = TILE_SIZE * ROWS

# Posiciones iniciales de los Yoshis (fuera de zonas especiales)
def generar_posiciones_iniciales():
    zonas = {(0,0), (0,1), (0,2), (1,0), (2,0),
             (0,5), (0,6), (0,7), (1,7), (2,7),
             (7,0), (6,0), (5,0), (7,1), (7,2),
             (7,7), (6,7), (5,7), (7,5), (7,6)}
    while True:
        verde = (random.randint(0, 7), random.randint(0, 7))
        rojo = (random.randint(0, 7), random.randint(0, 7))
        if verde != rojo and verde not in zonas and rojo not in zonas:
            return verde, rojo

class YoshiGame:
    def __init__(self, root):
        verde_img = Image.open("imagenes/yoshi.png").resize((TILE_SIZE, TILE_SIZE))
        rojo_img = Image.open("imagenes/yoshi-rojo.png").resize((TILE_SIZE, TILE_SIZE))

        self.yoshi_verde_img = ImageTk.PhotoImage(verde_img)
        self.yoshi_rojo_img = ImageTk.PhotoImage(rojo_img)

        self.canvas = tk.Canvas(root, width=WINDOW_SIZE, height=WINDOW_SIZE)
        self.canvas.pack()
        self.zonas = self.definir_zonas()
        self.casillas_pintadas = {}  # (fila, col): 'verde' o 'rojo'
        self.yoshi_verde, self.yoshi_rojo = generar_posiciones_iniciales()
        self.turno = 'verde'  # Comienza la máquina
        self.zonas_ganadas = {'verde': 0, 'rojo': 0}
        self.dibujar_tablero()
        self.canvas.bind("<Button-1>", self.jugador_mueve)
        self.root = root
        root.after(1000, self.jugada_maquina)  # primer turno máquina

    def definir_zonas(self):
        zonas = {
        0: {(0,0), (0,1), (0,2), (1,0), (2,0)},      # arriba izquierda
        1: {(0,5), (0,6), (0,7), (1,7), (2,7)},      # arriba derecha
        2: {(7,0), (6,0), (5,0), (7,1), (7,2)},      # abajo izquierda
        3: {(7,7), (6,7), (5,7), (7,5), (7,6)},      # abajo derecha
    }   
        return zonas

    def dibujar_tablero(self):
        self.canvas.delete("all")
        for i in range(ROWS):
            for j in range(COLS):
                color = 'white' 
                self.canvas.create_rectangle(j*TILE_SIZE, i*TILE_SIZE,
                                             (j+1)*TILE_SIZE, (i+1)*TILE_SIZE,
                                             fill=color)
        # Pintar zonas especiales
        for zona in self.zonas.values():
            for (i, j) in zona:
                if (i, j) in self.casillas_pintadas:
                    color = 'lightgreen' if self.casillas_pintadas[(i, j)] == 'verde' else 'salmon'
                else:
                    color = 'lightblue'
                self.canvas.create_rectangle(j*TILE_SIZE, i*TILE_SIZE,
                                             (j+1)*TILE_SIZE, (i+1)*TILE_SIZE,
                                             fill=color)

        # Dibujar Yoshis
        self.dibujar_yoshi(self.yoshi_verde, 'green')
        self.dibujar_yoshi(self.yoshi_rojo, 'red')
        

    def dibujar_yoshi(self, pos, color):
        i, j = pos
        x = j * TILE_SIZE + TILE_SIZE // 2
        y = i * TILE_SIZE + TILE_SIZE // 2
        if color == 'green':
            self.canvas.create_image(x, y, image=self.yoshi_verde_img, anchor='center')
        else:
            self.canvas.create_image(x, y, image=self.yoshi_rojo_img, anchor='center')

    def jugador_mueve(self, event):
        if self.turno != 'rojo':
            return
        j = event.x // TILE_SIZE
        i = event.y // TILE_SIZE
        if (i, j) in self.movimientos_legales(self.yoshi_rojo):
            self.yoshi_rojo = (i, j)
            self.pintar_casilla(i, j, 'rojo')
            self.turno = 'verde'
            self.dibujar_tablero()
            self.root.after(1000, self.jugada_maquina)

    def jugada_maquina(self):
        if self.turno != 'verde':
            return
        posibles = self.movimientos_legales(self.yoshi_verde)
        if posibles:
            self.yoshi_verde = random.choice(posibles)  # cambiar por minimax luego
            i, j = self.yoshi_verde
            self.pintar_casilla(i, j, 'verde')
        self.turno = 'rojo'
        self.dibujar_tablero()

    #movimientos en L
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
        zona = self.zonas[idx]
        conteo = {'verde': 0, 'rojo': 0}
        for pos in zona:
            if pos in self.casillas_pintadas:
                conteo[self.casillas_pintadas[pos]] += 1
        total = sum(conteo.values())
        if total == len(zona):  # zona completa
            if conteo['verde'] > conteo['rojo']:
                self.zonas_ganadas['verde'] += 1
            elif conteo['rojo'] > conteo['verde']:
                self.zonas_ganadas['rojo'] += 1
            print(f"Zonas ganadas: Verde: {self.zonas_ganadas['verde']} | Rojo: {self.zonas_ganadas['rojo']}")
            if sum(self.zonas_ganadas.values()) == len(self.zonas):
                self.fin_juego()

    def fin_juego(self):
        ganador = None
        if self.zonas_ganadas['verde'] > self.zonas_ganadas['rojo']:
            ganador = '¡Yoshi Verde gana!'
        elif self.zonas_ganadas['rojo'] > self.zonas_ganadas['verde']:
            ganador = '¡Yoshi Rojo gana!'
        else:
            ganador = '¡Empate!'
        print(ganador)
        self.canvas.unbind("<Button-1>")

root = tk.Tk()
root.title("Yoshi's Zones")
juego = YoshiGame(root)
root.mainloop()
