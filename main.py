import tkinter as tk
from gui import BubbleBusterGUI
import json

if __name__ == "__main__":
  with open('game_data.json') as json_file:
    game_data = json.load(json_file)

  window = tk.Tk()
  BubbleBusterGUI(window)
  window.mainloop()