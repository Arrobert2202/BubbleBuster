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
  """
  Clasa pentru bulele din joc.
  """
  def __init__(self, row, col, color):
    """
    Initializarea unui obiect de tip Bubble.
    :param row: Randul pe care se afla bula in tabela hexagonala.
    :param col: Coloana pe care se afla bula in tabela hexagonala.
    :param color: Culoarea bulei.
    """
    self.row = row
    self.col = col
    self.color = color

  def draw(self, game_canvas, offset):
    """
    Deseneaza bula respectiva in canvas.
    :param game_canvas: Canvas-ul pe care desenam bulele.
    :param offset: Numarul de randuri cu care a coborat tabla de joc.
    """
    self.x, self.y = self.bubble_positions(self.row, self.col, offset)
    bubble_radius = BUBBLESIZE // 2
    self.bubble_id = game_canvas.create_oval(self.x - bubble_radius, self.y - bubble_radius, self.x + bubble_radius, self.y + bubble_radius, fill = self.color, tag="bubble")

  def get_bubble_id(self):
    """
    Returneaza id-ul bulei.
    """
    return self.bubble_id
  
  def destroy(self, game_canvas):
    """
    Distruge bula respectiva.
    :param game_canvas: Canvas-ul in care a fost desenata bula pe care o eliminam.
    """
    game_canvas.delete(self.get_bubble_id())

  def bubble_positions(self, row, col, offset):
    """
    Calculeaza coordonatele X si Y ale bulei in canvas.
    :param row: Randul pe care se afla bula in tabela hexagonala.
    :param col: Coloana pe care se afla bula in tabela hexagonala.
    :param offset: Numarul de randuri cu care a coborat tabla de joc.
    """
    bubble_radius = BUBBLESIZE / 2
    x = BUBBLESIZE * col + bubble_radius
    if (row + offset) % 2 == 1:
      x += bubble_radius
    y = BUBBLESIZE * row * 0.85 + bubble_radius
    return x, y

class Game:
  def __init__(self, window):
    self.window = window
    self.game_table = initial_matrix()
    self.all_colors = set()
    self.color_score = dict()
    self.shooting = False
    self.last_shake = False
    self.is_shaking = False
    self.drop_counter = 0
    self.score = 0
    self.first_row = 0
    self.loop_id = None
    self.game_over = False
    self.configure_window()

  def configure_window(self):
    self.window.title("BubbleBuster")
    self.window.geometry("600x700+500+50")
    self.window.configure(bg='#7700a6')
    self.menu_components()

  def menu_components(self):
    self.destroy_widgets()
    title_label = tk.Label(self.window, text="BubbleBuster", font=('Arial', 25), bg='#7700a6', fg='#defe47')
    title_label.pack(pady=(200,50))

    menu_frame = tk.Frame(self.window, bg='#7700a6')
    menu_frame.pack(pady=10)

    style = ttk.Style()
    style.theme_use('alt')
    style.configure('TButton', font=('Arial', 16, 'bold'), width=20, padding=5, foreground='#7700a6', background='#defe47')
    
    play_button = ttk.Button(menu_frame, text='Play', style='TButton', command=lambda: self.play_game(current_level=1))
    play_button.pack(pady=20)

    exit_button = ttk.Button(menu_frame, text='Exit', style='TButton', command=self.window.destroy)
    exit_button.pack(pady=10)

  def play_game(self, current_level):
    self.game_gui()
    self.create_random_table()
    self.game_loop()

  def create_random_table(self):
    self.all_colors = {"#08deea", "#c4ffff", "#fd8090", "#1261d1"}
    self.game_table = initial_matrix()

    for row in range(7):
      for col in range(MAXWIDTH):
        if row % 2 == 1 and col == MAXWIDTH - 1:
          continue
        else:
          color = random.choice(list(self.all_colors))
          self.game_table[row][col] = Bubble(row, col, color)

    self.generate_color_score()
    self.draw_table()

    self.current_color = self.random_bubble()
    self.draw_current_bubble()
    self.next_bubble_color = self.random_bubble()
    self.draw_next_bubble()

  def draw_table(self):
    for row in range(MAXHEIGHT):
      for col in range(MAXWIDTH):
        bubble = self.game_table[row][col]
        if bubble is not None:
          bubble.draw(self.game_canvas, self.first_row)
  
  def game_gui(self):
    self.destroy_widgets()

    top_frame = tk.Frame(self.window, bg='#7700a6')
    top_frame.pack(fill=tk.X)

    self.next_bubble_label = tk.Label(top_frame, text="Next bubble: ", font=('Arial', 12, 'bold'), bg='#7700a6', fg='#defe47')
    self.next_bubble_label.pack(side=tk.LEFT, pady=5)

    self.next_bubble_canvas = tk.Canvas(top_frame, width = 20, height = 20, bg='#7700a6', highlightthickness=0)
    self.next_bubble_canvas.pack(side = tk.LEFT)

    menu_button = tk.Button(top_frame, text='Go back', fg='#7700a6', bg='#defe47', command=lambda: self.go_to_menu())
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

  def generate_color_score(self):
    colors_count = dict()
    for color in self.all_colors:
      colors_count[color] = sum(1 for row in self.game_table for bubble in row if not bubble is None and bubble.color == color)
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
    
  def go_to_menu(self):
    self.reset_game()
    self.menu_components()

  def reset_game(self):
    self.window.after_cancel(self.loop_id)
    self.shooting = False
    self.score = 0
    self.game_table.clear()
    self.first_row = 0
    self.drop_counter = 0
    self.is_shaking = False
    self.last_shake = False
    self.game_over = False

    widgets_to_check = ['game_canvas', 'next_bubble_canvas', 'message_label']
    for widget_name in widgets_to_check:
      widget = getattr(self, widget_name, None)
      if widget and widget.winfo_exists():
        widget.pack_forget()

  def start_shooting(self, event):
    self.shooting = True
    self.shooting_event = event

  def game_loop(self):
    if self.game_over:
      return
    
    self.check_game_status()

    if self.shooting:
      self.shooting = False
      self.shoot_bubble()
    else:
      for item_id in self.game_canvas.find_withtag("bubble"):
        bubble_id = int(item_id)
        if bubble_id != self.current_bubble.get_bubble_id() and not any(bubble.get_bubble_id() == bubble_id for row in self.game_table for bubble in row if bubble is not None):
          self.game_canvas.delete(item_id)
      self.loop_id = self.window.after(10, self.game_loop)
    
    if self.drop_counter == 3 and self.is_shaking == False:
      self.is_shaking = True
      self.shake_canvas_right(1)
    elif self.drop_counter == 4 and self.is_shaking == False:
      self.is_shaking = True
      self.shake_canvas_right(2)
    elif self.drop_counter == 5 and self.is_shaking == False:
      self.drop_counter = 0
      self.drop_bubbles()

  def check_game_status(self):
    counter = 0
    for row in self.game_table:
      for bubble in row:
        if bubble is not None:
          counter += 1
    if counter == 0:
      self.show_message("win")
      self.game_over = True
    else:
      for col in range(MAXWIDTH):
        if not self.game_table[14][col] is None:
          self.show_message("lose")
          self.game_over = True

  def show_message(self, text):
    self.message_label = tk.Label(self.window, text=text, font=('Arial', 30, 'bold'), bg='#7700a6', fg='#defe47')
    self.message_label.pack(fill='both', expand=True)

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
    self.first_row += 1
    self.stop_shaking()
    self.update_table()
    self.block_space()
    self.window.update()

  def update_table(self):
    bubbles = [bubble for row in self.game_table for bubble in row if bubble is not None]
    for bubble in bubbles:
      self.game_table[bubble.row][bubble.col] = None

    for bubble in bubbles:
      bubble.row += 1
      self.game_table[bubble.row][bubble.col] = bubble
      self.game_canvas.move(bubble.get_bubble_id(), 0, BUBBLESIZE * 0.85)

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
    self.current_bubble = Bubble(15, 5, self.current_color)
    self.current_bubble.draw(self.game_canvas, self.first_row)

  def random_bubble(self):
    return random.choice(list(self.all_colors))

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
    if self.check_collision(bubble_direction_x, bubble_direction_y) is False:
      x1, y1, x2, y2 = self.game_canvas.coords(self.current_bubble.get_bubble_id())
      if x1 <= 0 or x2 >= WIDTH:
        bubble_direction_x *= (-1)
      self.window.after(10, self.move_bubble, bubble_direction_x, bubble_direction_y)
    else:
      self.handle_collision(bubble_direction_x, bubble_direction_y)
  
  def handle_collision(self, bubble_direction_x, bubble_direction_y):
    self.current_bubble.row, self.current_bubble.col = self.new_bubble_position(bubble_direction_x, bubble_direction_y)
    self.current_bubble.destroy(self.game_canvas)
    self.current_bubble.draw(self.game_canvas, self.first_row)
    self.game_table[self.current_bubble.row][self.current_bubble.col] = self.current_bubble
    self.last_bubble = self.current_bubble

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
    self.loop_id = self.window.after(50, self.game_loop)
  
  def check_collision(self, bubble_direction_x, bubble_direction_y):
    x1, y1, x2, y2 = self.game_canvas.coords(self.current_bubble.get_bubble_id())
    if y1 >= self.first_row * BUBBLESIZE * 0.85 + BUBBLESIZE/2:
      collisions = self.game_canvas.find_overlapping(x1, y1, x2, y2)
      collisions = [item for item in collisions if item != self.current_bubble.get_bubble_id()]

      bubbles = self.game_canvas.find_withtag("bubble")
      bubble_collisions = [item for item in bubbles if item in collisions]

      if len(bubble_collisions) == 0:
        return None
    return True
  
  def find_color_matches(self, matches, bubble, visited=None):
    if visited is None:
      visited = set()
    
    if bubble.get_bubble_id() in visited:
      return

    visited.add(bubble.get_bubble_id())
    matches.add(bubble)
    neighbor_bubbles = self.get_neighbor_bubbles(bubble.row, bubble.col)

    for neighbor in neighbor_bubbles:
      if neighbor.color == bubble.color:
        self.find_color_matches(matches, neighbor, visited)

  def get_target_bubbles(self, matches, safe_bubbles = None):
    if safe_bubbles is None:
      safe_bubbles = dict()

    for row in self.game_table:
      for bubble in row:
        if bubble is not None:
          if bubble.row == self.first_row:
            self.get_safe_neighbors(self.first_row, bubble.col, matches, safe_bubbles)
          elif (bubble.row + self.first_row) % 2 == 0 and (bubble.col == 0 or bubble.col == 11):
            self.get_safe_neighbors(bubble.row, bubble.col, matches, safe_bubbles)
    target_bubbles = [bubble for row in self.game_table for bubble in row if bubble is not None and bubble not in safe_bubbles.values()]
    return set(target_bubbles)

  def get_safe_neighbors(self, row, col, matches, safe_bubbles):
    bubble = self.game_table[row][col]
    if bubble not in matches and (row, col) not in safe_bubbles:
      safe_bubbles[(row, col)] = bubble
      neighbors = self.get_neighbor_bubbles(row, col)
      for neighbor in neighbors:
        self.get_safe_neighbors(neighbor.row, neighbor.col, matches, safe_bubbles)

  def get_neighbor_bubbles(self, row, col):
    neighbors = []
    
    if not col == 0 and not self.game_table[row][col - 1] is None:
      neighbors.append(self.game_table[row][col - 1])
    if not col == MAXWIDTH - 1 and not self.game_table[row][col + 1] is None:
      neighbors.append(self.game_table[row][col + 1])
    if not row == 0 and not self.game_table[row - 1][col] is None:
      neighbors.append(self.game_table[row - 1][col])
    if not row == MAXHEIGHT and not self.game_table[row + 1][col] is None:
      neighbors.append(self.game_table[row + 1][col])
    if (row + self.first_row) % 2 == 0:
      if not row == 0 and not col == 0 and not self.game_table[row - 1][col - 1] is None:
        neighbors.append(self.game_table[row - 1][col - 1])
      if not row == MAXHEIGHT and not col == 0 and not self.game_table[row + 1][col - 1] is None:
        neighbors.append(self.game_table[row + 1][col - 1])
    else:
      if not row == 0 and not col == MAXWIDTH - 1 and not self.game_table[row - 1][col + 1] is None:
        neighbors.append(self.game_table[row - 1][col + 1])
      if not row == MAXHEIGHT and not col == MAXWIDTH - 1 and not self.game_table[row + 1][col + 1] is None:
        neighbors.append(self.game_table[row + 1][col + 1])
    
    return neighbors

  def disolve_bubbles(self, matches):
    for bubble in matches:
      print(f"{bubble.row},{bubble.col}: {bubble.color}")
      bubble.destroy(self.game_canvas)
      self.game_table[bubble.row][bubble.col] = None
      color = bubble.color
      if self.next_bubble_color is not color and not any(bubble.color == color for row in self.game_table for bubble in row if bubble is not None):
        self.all_colors.remove(bubble.color)

  def new_bubble_position(self, bubble_direction_x, bubble_direction_y):
    x1, y1, x2, y2 = self.game_canvas.coords(self.current_bubble.get_bubble_id())
    print(f"new pos: {x1}, {y1}, {x2}, {y2}")
    bubble_center_x = (x1 + x2) / 2
    bubble_center_y = (y1 + y2) / 2
    col = int(bubble_center_x / BUBBLESIZE) + int(abs(bubble_direction_x)/5)
    row = int(bubble_center_y / (BUBBLESIZE * 0.85)) + int(abs(bubble_direction_y)/5) 
    # if (row + self.first_row) % 2 == 1:
    #     col -= 1

    print(f"{row}, {col}")
    if self.game_table[row - 1][col] is None:
      if self.game_table[row - 1][col - 1] is not None or self.game_table[row - 1][col + 1] is not None:
        row -= 1
    if col == 11 and (row + self.first_row) % 2 == 1:
      if self.game_table[row][col - 1] is not None:
        row += 1
      else:
        col -= 1

    print(f"{row}, {col}")
    return row, col
  
  def update_next_bubbles(self):
    self.get_next_bubble()
    self.draw_next_bubble()
    self.draw_current_bubble()

  def update_score(self, matches, target_bubbles):
    new_score = 15 * len(matches)
    for bubble in list(target_bubbles - matches):
      new_score += 3 * self.color_score[bubble.color]
    
    self.score += new_score

    self.score_text.set(f"Score: {self.score}")

def initial_matrix():
  game_table = [[None for _ in range(MAXWIDTH)] for _ in range(MAXHEIGHT + 2)]
  return game_table