import tkinter as tk
from interfaz import YoshiGameGUI

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Yoshi's Zones")
    app = YoshiGameGUI(root)
    root.mainloop()