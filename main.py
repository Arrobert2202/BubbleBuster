import tkinter as tk
from game_utils import *
import json

def create_level_table(levels_data):
  game_table = []
  

def main(levels_data):
  current_level = 1
  window = tk.Tk()
  configure_window(window)
  window.mainloop()

if __name__ == "__main__":
  with open('game_data.json') as json_file:
    levels_data = json.load(json_file)
  main(levels_data)
