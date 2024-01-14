import tkinter as tk
from game_utils import *

def main():
  window = tk.Tk()
  game = Game(window)
  window.mainloop()

if __name__ == "__main__":
  main()
