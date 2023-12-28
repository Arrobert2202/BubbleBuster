import tkinter as tk
from tkinter import ttk

class BubbleBusterGUI:
  def __init__(self, window):
    self.window = window
    self.menu_config()
    self.menu_components()
  
  def menu_config(self):
    self.window.title("BubbleBuster")
    self.window.geometry("600x700+500+50")
    self.window.configure(bg='#7700a6')

  def menu_components(self):
    self.destroy_widgets()

    title_label = tk.Label(self.window, text="BubbleBuster", bg='#7700a6', fg='#defe47')
    title_label.configure(font=('Arial', 25))
    title_label.pack(pady=(200,50))

    menu_frame = tk.Frame(self.window, bg='#7700a6')
    menu_frame.pack(pady=10)

    style = ttk.Style()
    style.theme_use('alt')

    style.configure('TButton', font=('Arial', 16, 'bold'), width = 20, padding=5, foreground = '#7700a6', background='#defe47')
    play_button = ttk.Button(menu_frame, text='Play', command=self.play_game)
    play_button.configure(style='TButton')
    play_button.pack(pady=20)

    exit_button = ttk.Button(menu_frame, text='Exit', command=self.window.destroy)
    exit_button.configure(style='TButton')
    exit_button.pack(pady=10)
  
  def play_game(self):
    self.destroy_widgets()

    top_frame = tk.Frame(self.window, bg='#7700a6')
    top_frame.pack(fill=tk.X)

    level_label = tk.Label(top_frame, text = "Level 1", font=('Arial', 12, 'bold'), bg='#7700a6', fg='#defe47')
    level_label.pack(pady=5)

    next_bubble_label = tk.Label(top_frame, text = "Next bubble: ", font=('Arial', 12, 'bold'), bg='#7700a6', fg='#defe47')
    next_bubble_label.pack(pady=5)
    
    menu_button = tk.Button(top_frame, text = 'Go to menu', foreground = '#7700a6', background='#defe47', command = self.menu_components)
    menu_button.place(relx=0.97, rely=0.25, anchor=tk.NE)

    game_canvas = tk.Canvas(self.window,width=450, height=550, bg='#092067', highlightbackground='#fe00fe', highlightthickness=10)
    game_canvas.pack(pady=10)

    score_label = tk.Label(self.window, text="Score: ",font=('Arial', 16, 'bold'), bg='#7700a6', fg='#defe47')
    score_label.pack()

  def destroy_widgets(self):
    for widget in self.window.winfo_children():
      widget.destroy()
