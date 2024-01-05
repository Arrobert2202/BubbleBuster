import tkinter as tk
from tkinter import ttk
import random
import math

WIDTH = 456
HEIGHT = 550
MAXHEIGHT = 14
MAXWIDTH = 12
BUBBLESIZE = 38

class HexagonalTable:
  def __init__(self):
    self.table = dict()
    self.all_colors = set()
  
  def add(self, bubble):
    self.table[(bubble.row, bubble.col)] = bubble
    self.all_colors.add(bubble.color)
  
  def get_bubble(self, row, col):
    return self.table.get((row, col), None)
  
  def get_colors(self):
    return self.all_colors

  def delete(self, row, col):
    self.table.pop((row, col), None)

class Game:
  def __init__(self, levels_data):
    self.window = tk.Tk()
    self.levels_data = levels_data
    self.game_table = HexagonalTable()
    self.shooting = False
    self.configure_window()
    self.window.mainloop()

  def configure_window(self):
    self.window.title("BubbleBuster")
    self.window.geometry("600x700+500+50")
    self.window.configure(bg='#7700a6')
    self.menu_components()

  def menu_components(self):
    self.destroy_widgets()

    title_label = tk.Label(self.window, text="BubbleBuster", bg='#7700a6', fg='#defe47')
    title_label.configure(font=('Arial', 25))
    title_label.pack(pady=(200,50))

    menu_frame = tk.Frame(self.window, bg='#7700a6')
    menu_frame.pack(pady=10)

    style = ttk.Style()
    style.theme_use('alt')

    style.configure('TButton', font=('Arial', 16, 'bold'), width=20, padding=5, foreground='#7700a6', background='#defe47')
    play_button = ttk.Button(menu_frame, text='Play', command=lambda: self.play_game(current_level=1))
    play_button.configure(style='TButton')
    play_button.pack(pady=20)

    exit_button = ttk.Button(menu_frame, text='Exit', command=self.window.destroy)
    exit_button.configure(style='TButton')
    exit_button.pack(pady=10)

  def play_game(self, current_level):
    self.game_gui()
    self.create_level_table(current_level)
    self.game_loop()

  def game_gui(self):
    self.destroy_widgets()

    top_frame = tk.Frame(self.window, bg='#7700a6')
    top_frame.pack(fill=tk.X)

    level_label = tk.Label(top_frame, text="Level 1", font=('Arial', 12, 'bold'), bg='#7700a6', fg='#defe47')
    level_label.pack(pady=5)

    self.next_bubble_label = tk.Label(top_frame, text="Next bubble: ", font=('Arial', 12, 'bold'), bg='#7700a6', fg='#defe47')
    self.next_bubble_label.pack(side=tk.LEFT, pady=5)

    self.next_bubble_canvas = tk.Canvas(top_frame, width = 20, height = 20, bg='#7700a6', highlightthickness=0)
    self.next_bubble_canvas.pack(side = tk.LEFT)

    menu_button = tk.Button(top_frame, text='Go to menu', foreground='#7700a6', background='#defe47', command=lambda: self.menu_components())
    menu_button.place(relx=0.97, rely=0.25, anchor=tk.NE)

    self.game_canvas = tk.Canvas(self.window, width=456, height=550, bg='#092067', highlightbackground='#fe00fe', highlightthickness=1)
    self.game_canvas.pack(pady=10)
    line_y = (MAXHEIGHT - 2) * BUBBLESIZE + BUBBLESIZE // 2
    self.game_canvas.create_line(70, line_y, 386, line_y, width = 3, fill = '#7700a6')
    self.game_canvas.bind("<Button-1>", self.start_shooting)

    score_label = tk.Label(self.window, text="Score: ", font=('Arial', 16, 'bold'), bg='#7700a6', fg='#defe47')
    score_label.pack()

  def destroy_widgets(self):
    for widget in self.window.winfo_children():
      widget.destroy()

  def populate_table(self, bubbles_data):
    for bubble in bubbles_data:
      self.game_table.add(Bubble(bubble['color'], bubble['row'], bubble['col']))

  def create_level_table(self, current_level):
    level_data = self.levels_data['levels'][current_level - 1]
    bubbles_data = level_data['bubbles']

    self.populate_table(bubbles_data)

    for row in range(MAXHEIGHT):
      for col in range(MAXWIDTH):
        bubble = self.game_table.get_bubble(row, col)
        if bubble is not None:
          bubble.draw(self.game_canvas)

    self.current_color = self.random_bubble()
    self.draw_current_bubble()
    self.next_bubble_color = self.random_bubble()
    self.draw_next_bubble()
    
  def game_loop(self):
    if self.shooting:
      print("Shooting")
      self.shoot_bubble()
      print("Finished shooting")

      self.shooting = False
    self.window.after(10, self.game_loop)

  def get_next_bubble(self):
    self.current_color =  self.next_bubble_color
    self.next_bubble_color = self.random_bubble()
  
  def draw_next_bubble(self):
    self.next_bubble_canvas.create_oval(0, 0, 20, 20, fill = self.next_bubble_color)

  def draw_current_bubble(self):
    self.current_bubble = Bubble(self.current_color, 15, 5)
    self.current_bubble.draw(self.game_canvas)

  def random_bubble(self):
    return random.choice(list(self.game_table.get_colors()))
  
  def start_shooting(self, event):
    self.shooting = True
    self.shooting_event = event

  def shoot_bubble(self):
    x1, y1, x2, y2 = self.game_canvas.coords(self.current_bubble.get_bubble_id())
    bubble_center_x = (x1 + x2) / 2
    bubble_center_y = (y1 + y2) / 2
    angle = math.atan2(self.shooting_event.y - bubble_center_y, self.shooting_event.x - bubble_center_x)
    bubble_direction_x = 5 * math.cos(angle)
    bubble_direction_y = 5 * math.sin(angle)

    self.game_canvas.after(30, self.move_bubble, bubble_direction_x, bubble_direction_y)

  def move_bubble(self, bubble_direction_x, bubble_direction_y):
    self.game_canvas.move(self.current_bubble.get_bubble_id(), bubble_direction_x, bubble_direction_y)
    
    x1, y1, x2, y2 = self.game_canvas.coords(self.current_bubble.get_bubble_id())
    if x1 <= 0 or x2 >= WIDTH:
      bubble_direction_x *= (-1)
    if y1 <= 0 or y2 >= HEIGHT:
      bubble_direction_y *= (-1)

    bubble_collision = self.check_bubble_collision()
    if bubble_collision is False:
      self.window.after(10, self.move_bubble, bubble_direction_x, bubble_direction_y)
    else:
      self.handle_collision()
  
  def handle_collision(self):
    self.current_bubble.row, self.current_bubble.col = self.new_bubble_position()

    self.current_bubble.destroy(self.game_canvas)
    self.current_bubble.draw(self.game_canvas)
    self.game_table.add(self.current_bubble)
    self.last_bubble = self.current_bubble

    matches = list()
    print(matches)
    self.find_color_matches(matches, self.current_bubble)  
    if len(matches) >= 3:
      target_bubbles = self.get_dependent_bubbles(matches)
      self.disolve_bubbles(matches + target_bubbles)  
    self.update_next_bubbles()
  
  def find_color_matches(self, matches, bubble, visited=None):
    if visited is None:
      visited = set()
    row, col, color = bubble.row, bubble.col, bubble.color
    
    if bubble.get_bubble_id() in visited:
      return

    visited.add(bubble.get_bubble_id())
    matches.append(bubble)
    neighbor_bubbles = self.get_neighbor_bubbles(row, col)

    for bubble in neighbor_bubbles:
      # if bubble is not None and bubble.get_bubble_id() not in visited and bubble.color == color:
      if bubble.color == color:
        self.find_color_matches(matches,bubble, visited)

  def get_dependent_bubbles(self, matches, safe_bubbles = None):
    if safe_bubbles is None:
      safe_bubbles = dict()

    for col in range(12):
      self.get_safe_neighbors(0, col, matches, safe_bubbles)
    
    target_bubbles = [bubble for bubble in self.game_table.table.values() if bubble not in safe_bubbles.values()]
    return target_bubbles

  def get_safe_neighbors(self, row, col, matches, safe_bubbles):
    bubble = self.game_table.get_bubble(row, col)
    if bubble not in matches and (row, col) not in safe_bubbles:
      safe_bubbles[(row, col)] = bubble
      neighbors = self.get_neighbor_bubbles(row, col)
      for neighbor in neighbors:
        self.get_safe_neighbors(neighbor.row, neighbor.col, matches, safe_bubbles)


  def get_neighbor_bubbles(self, row, col):
    neighbors = []

    if not self.game_table.get_bubble(row, col - 1) is None:
      neighbors.append(self.game_table.get_bubble(row, col - 1))
    if not self.game_table.get_bubble(row, col + 1) is None:
      neighbors.append(self.game_table.get_bubble(row, col + 1))
    if not self.game_table.get_bubble(row - 1, col) is None:
      neighbors.append(self.game_table.get_bubble(row - 1, col))
    if not self.game_table.get_bubble(row + 1, col) is None:
      neighbors.append(self.game_table.get_bubble(row + 1, col))
    if row % 2 == 0:
      if not self.game_table.get_bubble(row - 1, col - 1) is None:
        neighbors.append(self.game_table.get_bubble(row - 1, col - 1))
      if not self.game_table.get_bubble(row + 1, col - 1) is None:
        neighbors.append(self.game_table.get_bubble(row + 1, col - 1))
    else:
      if not self.game_table.get_bubble(row - 1, col + 1) is None:
        neighbors.append(self.game_table.get_bubble(row - 1, col + 1))
      if not self.game_table.get_bubble(row + 1, col + 1) is None:
        neighbors.append(self.game_table.get_bubble(row + 1, col + 1))
    
    return neighbors

  def disolve_bubbles(self, matches):
    for bubble in matches:
      print(f"{bubble.row}, {bubble.col}")
      self.game_table.delete(bubble.row, bubble.col)
      bubble.destroy(self.game_canvas)  

  def new_bubble_position(self):
    x1, y1, x2, y2 = self.game_canvas.coords(self.current_bubble.get_bubble_id())

    bubble_center_x = (x1 + x2) / 2
    bubble_center_y = (y1 + y2) / 2

    row = int(bubble_center_y / BUBBLESIZE)
    col = int(bubble_center_x / BUBBLESIZE)

    if not self.game_table.get_bubble(row,col) is None:
      print("1")
      row += 1
    if row % 2 == 1 and col == 11:
      if not self.game_table.get_bubble(row, col - 1) is None:
        print("2")
        row += 1
      else:
        print("3")
        col -= 1
    if not self.game_table.get_bubble(row - 1, col) is None:
      if row % 2 == 1 and self.game_table.get_bubble(row - 1, col).x > bubble_center_x:
        print("4")
        col -= 1
    return row, col
  
  def update_next_bubbles(self):
    self.get_next_bubble()
    self.draw_next_bubble()
    self.draw_current_bubble()

  def check_bubble_collision(self):
    x1, y1, x2, y2 = self.game_canvas.coords(self.current_bubble.get_bubble_id())
    collisions = self.game_canvas.find_overlapping(x1, y1, x2, y2)
    collisions = [item for item in collisions if item != self.current_bubble.get_bubble_id()]

    bubble_collisions = self.game_canvas.find_withtag("bubble")
    bubble_collisions = [item for item in bubble_collisions if item in collisions]

    if len(bubble_collisions) == 0:
      return False
    return True

class Bubble:
  def __init__(self, color, row, col):
    self.color = color
    self.row = row
    self.col = col

  def draw(self, game_canvas):
    self.x, self.y = bubble_positions(self.row, self.col)
    bubble_radius = BUBBLESIZE // 2
    self.bubble_id = game_canvas.create_oval(self.x - bubble_radius, self.y - bubble_radius, self.x + bubble_radius, self.y + bubble_radius, fill = self.color, tag="bubble")

  def get_bubble_id(self):
    return self.bubble_id
  
  def destroy(self, game_canvas):
    game_canvas.delete(self.get_bubble_id())
  
def bubble_positions(row, col):
  x = BUBBLESIZE * col + BUBBLESIZE // 2
  if row % 2 == 1:
    x += BUBBLESIZE // 2
  y = BUBBLESIZE * row * 0.86 + BUBBLESIZE // 2
  return x, y 