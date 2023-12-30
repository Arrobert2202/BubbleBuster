import tkinter as tk
from game_utils import *
import json

def main(levels_data):
  game = Game(levels_data)

if __name__ == "__main__":
  with open('game_data.json') as json_file:
    levels_data = json.load(json_file)
  main(levels_data)
