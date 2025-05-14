import tkinter as tk
from PIL import Image, ImageTk
from game import YoshiGameLogic, TILE_SIZE, ROWS, COLS
import random

class YoshiGameGUI:
    def __init__(self, root):
        self.logic = YoshiGameLogic()
        self.root = root
        self.frame = tk.Frame(root)
        self.frame.pack()

        self.canvas = tk.Canvas(self.frame, width=TILE_SIZE*COLS, height=TILE_SIZE*ROWS)
        self.canvas.grid(row=0, column=0)

        self.sidebar = tk.Frame(self.frame, padx=10, pady=10)
        self.sidebar.grid(row=0, column=1, sticky="n")

        self.yoshi_verde_img = ImageTk.PhotoImage(Image.open("imagenes/yoshi.png").resize((TILE_SIZE, TILE_SIZE)))
        self.yoshi_rojo_img = ImageTk.PhotoImage(Image.open("imagenes/yoshi-rojo.png").resize((TILE_SIZE, TILE_SIZE)))

        self.label_zonas = tk.Label(self.sidebar, text="Zonas ganadas\n🟢 Verde: 0\n🔴 Rojo: 0", font=("Arial", 12))
        self.label_zonas.pack(pady=10)

        self.label_dif = tk.Label(self.sidebar, text="Seleccionar dificultad", font=("Arial", 12))
        self.label_dif.pack(pady=5)

        self.dificultades = ["Principiante", "Amateur", "Experto"]
        self.botones_dificultad = {}

        for dif in self.dificultades:
            btn = tk.Button(self.sidebar, text=dif, width=15, command=lambda d=dif: self.set_dificultad(d))
            btn.pack(pady=2)
            self.botones_dificultad[dif] = btn

        self.btn_jugar = tk.Button(self.sidebar, text="Jugar", state="disabled", command=self.iniciar_juego)
        self.btn_jugar.pack(pady=20)

    def set_dificultad(self, nivel):
        self.logic.dificultad = nivel
        for dif, btn in self.botones_dificultad.items():
            btn.config(bg="SystemButtonFace")
        self.botones_dificultad[nivel].config(bg="lightgreen")
        self.btn_jugar.config(state="normal")

    def iniciar_juego(self):
        self.logic.__init__()  # Reinicia el estado del juego
        self.dibujar_tablero()
        self.canvas.bind("<Button-1>", self.jugador_mueve)
        self.root.after(1000, self.jugada_maquina)

    def dibujar_tablero(self):
        self.canvas.delete("all")
        for i in range(ROWS):
            for j in range(COLS):
                color = 'white'
                self.canvas.create_rectangle(j*TILE_SIZE, i*TILE_SIZE, (j+1)*TILE_SIZE, (i+1)*TILE_SIZE, fill=color)

        for zona in self.logic.zonas.values():
            for (i, j) in zona:
                if (i, j) in self.logic.casillas_pintadas:
                    color = 'lightgreen' if self.logic.casillas_pintadas[(i, j)] == 'verde' else 'salmon'
                else:
                    color = 'lightblue'
                self.canvas.create_rectangle(j*TILE_SIZE, i*TILE_SIZE, (j+1)*TILE_SIZE, (i+1)*TILE_SIZE, fill=color)

        self.dibujar_yoshi(self.logic.yoshi_verde, 'verde')
        self.dibujar_yoshi(self.logic.yoshi_rojo, 'rojo')
        self.actualizar_puntaje()

    def dibujar_yoshi(self, pos, color):
        i, j = pos
        x = j * TILE_SIZE + TILE_SIZE // 2
        y = i * TILE_SIZE + TILE_SIZE // 2
        if color == 'verde':
            self.canvas.create_image(x, y, image=self.yoshi_verde_img, anchor='center')
        else:
            self.canvas.create_image(x, y, image=self.yoshi_rojo_img, anchor='center')

    def jugador_mueve(self, event):
        if self.logic.turno != 'rojo':
            return
        j, i = event.x // TILE_SIZE, event.y // TILE_SIZE
        if (i, j) in self.logic.movimientos_legales(self.logic.yoshi_rojo):
            self.logic.yoshi_rojo = (i, j)
            self.logic.pintar_casilla(i, j, 'rojo')
            self.logic.turno = 'verde'
            self.dibujar_tablero()
            self.root.after(1000, self.jugada_maquina)

    def jugada_maquina(self):
        if self.logic.turno != 'verde':
            return
        posibles = self.logic.movimientos_legales(self.logic.yoshi_verde)
        if posibles:
            self.logic.yoshi_verde = random.choice(posibles)
            i, j = self.logic.yoshi_verde
            self.logic.pintar_casilla(i, j, 'verde')
        self.logic.turno = 'rojo'
        self.dibujar_tablero()

        if self.logic.fin_juego():
            ganador = self.logic.obtener_ganador()
            mensaje = {
                'verde': '¡Yoshi Verde gana!',
                'rojo': '¡Yoshi Rojo gana!',
                'empate': '¡Empate!'
            }[ganador]
            print(mensaje)
            self.canvas.unbind("<Button-1>")

    def actualizar_puntaje(self):
        v = self.logic.zonas_ganadas['verde']
        r = self.logic.zonas_ganadas['rojo']
        self.label_zonas.config(text=f"Zonas ganadas\n🟢 Verde: {v}\n🔴 Rojo: {r}")
