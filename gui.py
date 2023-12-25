import tkinter as tk
from tkinter import ttk

class MainMenu:
  def __init__(self, window):
    self.window = window
    self.menu_config()
    self.menu_components()
  
  def menu_config(self):
    self.window.title("BubbleBuster")
    self.window.geometry("600x700+500+50")
    self.window.configure(bg='#7700a6')

  def menu_components(self):
    title_label = tk.Label(self.window, text="BubbleBuster", bg='#7700a6', fg='#defe47')
    title_label.configure(font=('Arial', 25))
    title_label.pack(pady=(200,50))

    menu_frame = tk.Frame(self.window, bg='#7700a6')
    menu_frame.pack(pady=10)

    style = ttk.Style()
    style.theme_use('alt')

    style.configure('TButton', font=('Arial', 16, 'bold'), width = 20, padding=5, foreground = '#7700a6', background='#defe47')
    play_button = ttk.Button(menu_frame, text='Play')
    play_button.configure(style='TButton')
    play_button.pack(pady=20)

    exit_button = ttk.Button(menu_frame, text='Exit', command=self.window.destroy)
    exit_button.configure(style='TButton')
    exit_button.pack(pady=10)