import tkinter as tk
from tkinter import ttk

class Bubble:
  def __init__(self, color, row, col):
    self.color = color
    self.row = row
    self.col = col

def configure_window(window):
    menu_config(window)
    menu_components(window)
  
def menu_config(window):
  window.title("BubbleBuster")
  window.geometry("600x700+500+50")
  window.configure(bg='#7700a6')

def menu_components(window):
  destroy_widgets(window)

  title_label = tk.Label(window, text="BubbleBuster", bg='#7700a6', fg='#defe47')
  title_label.configure(font=('Arial', 25))
  title_label.pack(pady=(200,50))

  menu_frame = tk.Frame(window, bg='#7700a6')
  menu_frame.pack(pady=10)

  style = ttk.Style()
  style.theme_use('alt')

  style.configure('TButton', font=('Arial', 16, 'bold'), width = 20, padding=5, foreground = '#7700a6', background='#defe47')
  play_button = ttk.Button(menu_frame, text='Play', command=lambda: play_game(window))
  play_button.configure(style='TButton')
  play_button.pack(pady=20)

  exit_button = ttk.Button(menu_frame, text='Exit', command=window.destroy)
  exit_button.configure(style='TButton')
  exit_button.pack(pady=10)

def play_game(window):
  destroy_widgets(window)

  top_frame = tk.Frame(window, bg='#7700a6')
  top_frame.pack(fill=tk.X)

  level_label = tk.Label(top_frame, text = "Level 1", font=('Arial', 12, 'bold'), bg='#7700a6', fg='#defe47')
  level_label.pack(pady=5)

  next_bubble_label = tk.Label(top_frame, text = "Next bubble: ", font=('Arial', 12, 'bold'), bg='#7700a6', fg='#defe47')
  next_bubble_label.pack(pady=5)
  
  menu_button = tk.Button(top_frame, text = 'Go to menu', foreground = '#7700a6', background='#defe47', command =lambda: menu_components(window))
  menu_button.place(relx=0.97, rely=0.25, anchor=tk.NE)

  game_canvas = tk.Canvas(window,width=450, height=550, bg='#092067', highlightbackground='#fe00fe', highlightthickness=10)
  game_canvas.pack(pady=10)

  score_label = tk.Label(window, text="Score: ",font=('Arial', 16, 'bold'), bg='#7700a6', fg='#defe47')
  score_label.pack()

def destroy_widgets(window):
  for widget in window.winfo_children():
    widget.destroy()