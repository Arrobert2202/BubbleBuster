import tkinter as tk
from tkinter import ttk
import random
import math

WIDTH = 456
HEIGHT = 550
MAXHEIGHT = 14
MAXWIDTH = 12
BUBBLESIZE = 38

class Bubble:
  def __init__(self, color, row, col):
    self.color = color
    self.row = row
    self.col = col

  def draw(self, game_canvas, offset):
    self.x, self.y = self.bubble_positions(self.row, self.col, offset)
    bubble_radius = BUBBLESIZE // 2
    self.bubble_id = game_canvas.create_oval(self.x - bubble_radius, self.y - bubble_radius, self.x + bubble_radius, self.y + bubble_radius, fill = self.color, tag="bubble")

  def get_bubble_id(self):
    return self.bubble_id
  
  def destroy(self, game_canvas):
    game_canvas.delete(self.get_bubble_id())

  def bubble_positions(self, row, col, offset):
    x = BUBBLESIZE * col + BUBBLESIZE // 2
    if (row + offset) % 2 == 1:
      x += BUBBLESIZE // 2
    y = BUBBLESIZE * row * 0.85 + BUBBLESIZE // 2
    return x, y

class Table:
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

  def get_table(self):
    return self.table

  def delete(self, row, col):
    self.table.pop((row, col), None)
  
  def clear(self):
    self.table.clear()
  
  def print_table(self):
    for row in range(MAXHEIGHT):
      row_data = []
      for col in range(MAXWIDTH):
        bubble = self.get_bubble(row, col)
        if bubble is not None:
          row_data.append(f"({row}, {col}): {bubble.color}")
      print(" | ".join(row_data))

class Game:
  def __init__(self, levels_data):
    self.window = tk.Tk()
    self.levels_data = levels_data
    self.game_table = Table()
    self.color_score = dict()
    self.shooting = False
    self.last_shake = False
    self.is_shaking = False
    self.drop_counter = 0
    self.level = 1
    self.score = 0
    self.first_row = 0
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

    self.level_text = tk.StringVar()
    self.level_text.set(f"Level {self.level}")
    level_label = tk.Label(top_frame, textvariable=self.level_text, font=('Arial', 12, 'bold'), bg='#7700a6', fg='#defe47')
    level_label.pack(pady=5)

    self.next_bubble_label = tk.Label(top_frame, text="Next bubble: ", font=('Arial', 12, 'bold'), bg='#7700a6', fg='#defe47')
    self.next_bubble_label.pack(side=tk.LEFT, pady=5)

    self.next_bubble_canvas = tk.Canvas(top_frame, width = 20, height = 20, bg='#7700a6', highlightthickness=0)
    self.next_bubble_canvas.pack(side = tk.LEFT)

    menu_button = tk.Button(top_frame, text='Go to menu', foreground='#7700a6', background='#defe47', command=lambda: self.go_to_menu())
    menu_button.place(relx=0.97, rely=0.25, anchor=tk.NE)

    self.game_canvas = tk.Canvas(self.window, width=456, height=550, bg='#092067', highlightbackground='#fe00fe', highlightthickness=1)
    self.game_canvas.pack(pady=10)
    line_y = (MAXHEIGHT - 2) * BUBBLESIZE + BUBBLESIZE // 2
    self.game_canvas.create_line(70, line_y, 386, line_y, width = 3, fill = '#7700a6')
    self.game_canvas.bind("<Button-1>", self.start_shooting)

    self.score_text = tk.StringVar()
    self.score_text.set(f"Score: {self.score}")
    score_label = tk.Label(self.window, textvariable=self.score_text, font=('Arial', 16, 'bold'), bg='#7700a6', fg='#defe47')
    score_label.pack()

  def destroy_widgets(self):
    for widget in self.window.winfo_children():
      widget.destroy()

  def populate_table(self, bubbles_data):
    for bubble in bubbles_data:
      self.game_table.add(Bubble(bubble['color'], bubble['row'], bubble['col']))
    self.generate_color_score()

  def generate_color_score(self):
    colors = self.game_table.get_colors()
    colors_count = dict()

    for color in colors:
      colors_count[color] = sum(1 for bubble in self.game_table.get_table().values() if bubble.color == color)
    
    sorted_colors = sorted(colors_count.keys(), key=lambda x: (isinstance(x, tuple), colors_count[x]))

    if len(sorted_colors) > 4:
      self.color_score[sorted_colors[0]] = 45
      sorted_colors.remove(sorted_colors[0])
      self.color_score[sorted_colors[1]] = 30
      sorted_colors.remove(sorted_colors[1])
    elif len(sorted_colors) > 2:
      self.color_score[sorted_colors[0]] = 30
      sorted_colors.remove(sorted_colors[0])
    for index, color in enumerate(sorted_colors, start=2):
      self.color_score[color] = 15
    
    print(self.color_score)

  def create_level_table(self, current_level):
    level_data = self.levels_data['levels'][current_level - 1]
    bubbles_data = level_data['bubbles']

    self.populate_table(bubbles_data)

    for row in range(MAXHEIGHT):
      for col in range(MAXWIDTH):
        bubble = self.game_table.get_bubble(row, col)
        if bubble is not None:
          bubble.draw(self.game_canvas, self.first_row)

    self.current_color = self.random_bubble()
    self.draw_current_bubble()
    self.next_bubble_color = self.random_bubble()
    self.draw_next_bubble()
    
  def go_to_menu(self):
    self.reset_game()
    self.menu_components()

  def reset_game(self):
    self.shooting = False
    self.score = 0
    self.game_table.clear()

  def start_shooting(self, event):
    self.shooting = True
    self.shooting_event = event

  def game_loop(self):
    if self.drop_counter == 3 and self.is_shaking == False:
      self.is_shaking = True
      self.shake_canvas_right(1)
    elif self.drop_counter == 4 and self.is_shaking == False:
      self.is_shaking = True
      self.shake_canvas_right(2)
    elif self.drop_counter == 5:
      self.drop_counter = 0
      self.drop_bubbles()
    if self.shooting:
      self.shooting = False
      self.shoot_bubble()
    else:
      self.window.after(10, self.game_loop)

  def stop_shaking(self):
    self.last_shake = True
    self.is_shaking = False

  def shake_canvas_right(self, offset):
    self.game_canvas.move("bubble", offset, 0)   
    self.shake_id = self.game_canvas.after(50, lambda: self.shake_canvas_left(offset))
  
  def shake_canvas_left(self, offset):
    self.game_canvas.move("bubble", offset * (-1), 0)
    if self.last_shake:
      self.last_shake = False
    else:
      self.shake_id1 = self.game_canvas.after(50, lambda: self.shake_canvas_right(offset))
      
  def drop_bubbles(self):
    self.stop_shaking()
    self.update_table()
    self.block_space()
    self.window.update()

  def update_table(self):
    bubbles = list(self.game_table.get_table().values())
    for bubble in bubbles:
      self.game_table.delete(bubble.row, bubble.col)

    for bubble in bubbles:
      self.game_canvas.move(bubble.get_bubble_id(), 0, BUBBLESIZE * 0.85)
      bubble.row += 1
      self.game_table.add(bubble)
    
    self.first_row += 1

  def block_space(self):
    if self.first_row > 0:
      block_height = self.first_row * BUBBLESIZE * 0.85
      self.game_canvas.create_rectangle(0, 0, WIDTH, block_height, fill = 'gray')

  def get_next_bubble(self):
    self.current_color =  self.next_bubble_color
    self.next_bubble_color = self.random_bubble()

  def draw_next_bubble(self):
    self.next_bubble_canvas.create_oval(0, 0, 20, 20, fill = self.next_bubble_color)

  def draw_current_bubble(self):
    self.current_bubble = Bubble(self.current_color, 15, 5)
    self.current_bubble.draw(self.game_canvas, self.first_row)

  def random_bubble(self):
    return random.choice(list(self.game_table.get_colors()))

  def shoot_bubble(self):
    x1, y1, x2, y2 = self.game_canvas.coords(self.current_bubble.get_bubble_id())
    bubble_center_x = (x1 + x2) / 2
    bubble_center_y = (y1 + y2) / 2
    angle = math.atan2(self.shooting_event.y - bubble_center_y, self.shooting_event.x - bubble_center_x)
    bubble_direction_x = 5 * math.cos(angle)
    bubble_direction_y = 5 * math.sin(angle)

    self.game_canvas.after(10, self.move_bubble, bubble_direction_x, bubble_direction_y)

  def move_bubble(self, bubble_direction_x, bubble_direction_y):
    self.game_canvas.move(self.current_bubble.get_bubble_id(), bubble_direction_x, bubble_direction_y)
    bubble_collision = self.check_bubble_collision()
    if bubble_collision is False:
      x1, y1, x2, y2 = self.game_canvas.coords(self.current_bubble.get_bubble_id())
      if x1 <= 0 or x2 >= WIDTH:
        bubble_direction_x *= (-1)
      self.window.after(10, self.move_bubble, bubble_direction_x, bubble_direction_y)
    else:
      self.handle_collision()
  
  def handle_collision(self):
    self.current_bubble.row, self.current_bubble.col = self.new_bubble_position()

    self.current_bubble.destroy(self.game_canvas)
    self.current_bubble.draw(self.game_canvas, self.first_row)
    self.game_table.add(self.current_bubble)
    self.last_bubble = self.current_bubble

    self.game_table.print_table()

    matches = set()
    self.find_color_matches(matches, self.current_bubble)  
    if len(matches) >= 3:
      target_bubbles = self.get_target_bubbles(matches)
      self.update_score(matches, target_bubbles)
      self.disolve_bubbles(target_bubbles)  
    self.update_next_bubbles()
    self.drop_counter += 1
    if self.is_shaking:
      self.stop_shaking()
    self.window.after(10, self.game_loop)
  
  def check_bubble_collision(self):
    x1, y1, x2, y2 = self.game_canvas.coords(self.current_bubble.get_bubble_id())
    if y1 >= self.first_row * BUBBLESIZE + BUBBLESIZE/2:
      collisions = self.game_canvas.find_overlapping(x1, y1, x2, y2)
      collisions = [item for item in collisions if item != self.current_bubble.get_bubble_id()]

      bubble_collisions = self.game_canvas.find_withtag("bubble")
      bubble_collisions = [item for item in bubble_collisions if item in collisions]

      if len(bubble_collisions) == 0:
        return False
      else:
        for collision_id in bubble_collisions:
          x1_c, y1_c, x2_c, y2_c = self.game_canvas.coords(collision_id)
          if y2_c > y1 and x1_c < x2 and x2_c > x1:
            return True
        return False
    return True
  
  def find_color_matches(self, matches, bubble, visited=None):
    if visited is None:
      visited = set()
    row, col, color = bubble.row, bubble.col, bubble.color
    
    if bubble.get_bubble_id() in visited:
      return

    visited.add(bubble.get_bubble_id())
    matches.add(bubble)
    neighbor_bubbles = self.get_neighbor_bubbles(row, col)

    for bubble in neighbor_bubbles:
      if bubble.color == color:
        self.find_color_matches(matches,bubble, visited)

  def get_target_bubbles(self, matches, safe_bubbles = None):
    if safe_bubbles is None:
      safe_bubbles = dict()

    for key in self.game_table.get_table().keys():
      row,col = key
      if row == self.first_row:
        self.get_safe_neighbors(self.first_row, col, matches, safe_bubbles)
      elif (row + self.first_row) % 2 == 0 and (col == 0 or col == 11):
        self.get_safe_neighbors(row, col, matches, safe_bubbles)
    target_bubbles = [bubble for bubble in self.game_table.table.values() if bubble not in safe_bubbles.values()]
    return set(target_bubbles)

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
      bubble.destroy(self.game_canvas)
      self.game_table.delete(bubble.row, bubble.col)  

  def new_bubble_position(self):
    x1, y1, x2, y2 = self.game_canvas.coords(self.current_bubble.get_bubble_id())

    bubble_center_x = (x1 + x2) / 2
    bubble_center_y = (y1 + y2) / 2
    row = int(bubble_center_y / BUBBLESIZE)
    col = int(bubble_center_x / BUBBLESIZE)

    if not self.game_table.get_bubble(row, col) is None:
      row += 1
    
    if (self.first_row + row) % 2 == 1 and col == 11:
      col -= 1
      if not self.game_table.get_bubble(row, col) is None:
        row += 1
    return row, col
  
  def update_next_bubbles(self):
    self.get_next_bubble()
    self.draw_next_bubble()
    self.draw_current_bubble()

  def update_score(self, matches, target_bubbles):
    new_score = 15 * len(matches)
    print(self.color_score)
    for bubble in list(target_bubbles - matches):
      new_score += 3 * self.color_score[bubble.color]
    
    self.score += new_score

    self.score_text.set(f"Score: {self.score}")