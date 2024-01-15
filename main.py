import tkinter as tk
from game_utils import *

def main():
  """
  Functia main a programului.  
  """
  window = tk.Tk()
  window.title("BubbleBuster")
  window.geometry("600x700+500+50")
  window.configure(bg='#7700a6')
  game = Game(window)
  window.mainloop()

if __name__ == "__main__":
  main()
