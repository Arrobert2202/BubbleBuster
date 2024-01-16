import tkinter as tk
from tkinter import ttk
import random
import math
from collections import Counter

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
    self.x, self.y = self.bubble_position(self.row, self.col, offset)
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

  def bubble_position(self, row, col, offset):
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
  """
  Clasa pentru jocul BubbleBuster
  """
  def __init__(self, window):
    """
    Initializarea unui obiect de tip Game.
    :param window: Fereastra in care va avea loc jocul.
    """
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
    self.menu_components()

  def menu_components(self):
    """
    Creara paginii de meniu.
    """
    for widget in self.window.winfo_children():
      widget.destroy()
    title_label = tk.Label(self.window, text="BubbleBuster", font=('Arial', 25), bg='#7700a6', fg='#defe47')
    title_label.pack(pady=(200,50))

    menu_frame = tk.Frame(self.window, bg='#7700a6')
    menu_frame.pack(pady=10)

    style = ttk.Style()
    style.theme_use('alt')
    style.configure('TButton', font=('Arial', 16, 'bold'), width=20, padding=5, foreground='#7700a6', background='#defe47')
    
    play_button = ttk.Button(menu_frame, text='Play', style='TButton', command=lambda: self.play_game())
    play_button.pack(pady=20)

    exit_button = ttk.Button(menu_frame, text='Exit', style='TButton', command=self.window.destroy)
    exit_button.pack(pady=10)

  def play_game(self):
    """
    Crearea unui nou joc, apasand pe butonul 'Play' din meniu.
    """
    self.game_gui()
    self.create_random_table()
    self.game_loop()

  def create_random_table(self):
    """
    Crearea unei table hexagonale de joc random.
    """
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
    self.current_color = random.choice(list(self.all_colors))
    self.current_bubble = Bubble(15, 5, self.current_color)
    self.current_bubble.draw(self.game_canvas, self.first_row)
    self.next_bubble_color = random.choice(list(self.all_colors))
    self.next_bubble_canvas.create_oval(0, 0, 20, 20, fill = self.next_bubble_color)

  def draw_table(self):
    """
    Desenarea tablei de joc.
    """
    for row in range(MAXHEIGHT):
      for col in range(MAXWIDTH):
        bubble = self.game_table[row][col]
        if bubble:
          bubble.draw(self.game_canvas, self.first_row)
  
  def game_gui(self):
    """
    Crearea interfetei de joc.
    """
    for widget in self.window.winfo_children():
      widget.destroy()

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

  def generate_color_score(self):
    """
    Generarea scorului bulelor, in functie de numarul de culori.
    """
    colors_count = Counter(bubble.color for row in self.game_table for bubble in row if bubble)
    sorted_colors = sorted(colors_count.keys(), key=lambda x: colors_count[x])

    if len(sorted_colors) > 4:
      self.color_score[sorted_colors[0]] = 45
      sorted_colors.pop(0)
      self.color_score[sorted_colors[0]] = 30
      sorted_colors.pop(0)
    elif len(sorted_colors) > 2:
      self.color_score[sorted_colors[0]] = 30
      sorted_colors.pop(0)
    for index, color in enumerate(sorted_colors, start=2):
      self.color_score[color] = 15
    
  def go_to_menu(self):
    """
    Trimiterea jucatorului catre meniul principal si resetarea jocului.
    """
    self.reset_game()
    self.menu_components()

  def reset_game(self):
    """
    Resetarea statutului din joc si a tuturor variabilelor.
    """
    self.window.after_cancel(self.loop_id)
    self.shooting = False
    self.score = 0
    self.game_table.clear()
    self.first_row = 0
    self.drop_counter = 0
    self.is_shaking = False
    self.last_shake = False
    self.game_over = False

    widgets = ['game_canvas', 'next_bubble_canvas', 'message_label']
    for widget in widgets:
      widget = getattr(self, widget, None)
      if widget and widget.winfo_exists():
        widget.pack_forget()

  def start_shooting(self, event):
    """
    Functie apelata atunci cand se apasa click pentru a trage o bula.
    :param event: Event-ul pentru click/Locul unde s-a apasat click.
    """
    self.shooting = True
    self.shooting_event = event

  def game_loop(self):
    """
    Functie ce reprezinta o bucla a jocului.
    """
    if self.game_over:
      return
    
    if self.drop_counter == 3 and not self.is_shaking:
      self.is_shaking = True
      self.shake_canvas_right(1)
    elif self.drop_counter == 4 and not self.is_shaking:
      self.is_shaking = True
      self.shake_canvas_right(2)
    elif self.drop_counter == 5 and not self.is_shaking:
      self.drop_counter = 0
      self.drop_bubbles()
      
    self.check_game_status()
    if self.shooting:
      self.shooting = False
      self.shoot_bubble()
    else:
      for id in self.game_canvas.find_withtag("bubble"):
        bubble_id = int(id)
        if bubble_id != self.current_bubble.get_bubble_id() and not any(bubble.get_bubble_id() == bubble_id for row in self.game_table for bubble in row if bubble):
          self.game_canvas.delete(id)
      self.loop_id = self.window.after(10, self.game_loop)

  def check_game_status(self):
    """
    Verificarea statutului jocului si terminarea acestuia in caz de win/lose.
    """
    if self.game_over:
      return
    counter = sum(1 for row in self.game_table for bubble in row if bubble)
    if counter == 0:
      self.show_message("win")
      self.game_over = True
    else:
      for col in range(MAXWIDTH):
        if self.game_table[14][col]:
          self.show_message("lose")
          self.game_over = True
          break

  def show_message(self, text):
    """
    Afisarea mesajului in caz de terminare a jocului.
    :parama text: Mesajul corespunzator statusului jocului.
    """
    self.stop_shaking()
    self.message_label = tk.Label(self.window, text=text, font=('Arial', 30, 'bold'), bg='#7700a6', fg='#defe47', width=100, height = 2)
    self.message_label.place(relx = 0.5, rely = 0.5, anchor=tk.CENTER)

  def stop_shaking(self):
    """
    Oprirea starii de shake care anunta caderea cu un nivel a bulelor.
    """
    self.last_shake = True
    self.is_shaking = False

  def shake_canvas_right(self, offset):
    """
    Mutarea in dreapta a bulelor(pentru efectul de shake).
    :param offset: Valoarea cu care sa se mute bulele la dreapta.
    """
    self.game_canvas.move("bubble", offset, 0)   
    self.shake_id = self.game_canvas.after(50, lambda: self.shake_canvas_left(offset))
  
  def shake_canvas_left(self, offset):
    """
    Mutarea in stanga a bulelor(pentru efectul de shake).
    :param offset: Valoarea cu care sa se mute bulele la stanga.
    """
    self.game_canvas.move("bubble", offset * (-1), 0)
    if self.last_shake:
      self.last_shake = False
    else:
      self.shake_id1 = self.game_canvas.after(50, lambda: self.shake_canvas_right(offset))
      
  def drop_bubbles(self):
    """
    Scaderea cu un rand a intregii tabele, pentru a ingreuna jocul.
    """
    self.first_row += 1
    self.update_table()
    if self.first_row > 0:
      self.game_canvas.create_rectangle(0, 0, WIDTH, self.first_row * BUBBLESIZE * 0.85, fill = 'gray')
    self.window.update()

  def update_table(self):
    """
    Actualizarea tabelei curente, astfel incat matricea sa mute cu un rand in jos bulele.
    """
    bubbles = [bubble for row in self.game_table for bubble in row if bubble]
    for bubble in bubbles:
      self.game_table[bubble.row][bubble.col] = None

    for bubble in bubbles:
      bubble.row += 1
      self.game_table[bubble.row][bubble.col] = bubble
      self.game_canvas.move(bubble.get_bubble_id(), 0, BUBBLESIZE * 0.85)

  def shoot_bubble(self):
    """
    Functie de declansare a tragerii bulei curente.
    """
    bubble_center_x, bubble_center_y = self.calculate_center(self.current_bubble)
    angle = math.atan2(self.shooting_event.y - bubble_center_y, self.shooting_event.x - bubble_center_x)
    bubble_direction_x = 8.5 * math.cos(angle)
    bubble_direction_y = 8.5 * math.sin(angle)

    self.game_canvas.after(10, self.move_bubble, bubble_direction_x, bubble_direction_y)

  def move_bubble(self, bubble_direction_x, bubble_direction_y):
    """
    Mutarea bulei si verificarea daca aceasta s-a intersecat cu alte bule.
    :param bubble_direction_x: Directia bulei pe axa X.
    :param bubble_direction_y:  Directia bulei pe axa Y.
    """
    self.game_canvas.move(self.current_bubble.get_bubble_id(), bubble_direction_x, bubble_direction_y)
    bubble_center_x, bubble_center_y = self.calculate_center(self.current_bubble)
    self.collision_bubble = None
    for row in self.game_table:
      for bubble in row:
        if bubble is None:  continue
        
        other_center_x, other_center_y = self.calculate_center(bubble)
        if math.sqrt((other_center_x - bubble_center_x)**2  + (other_center_y - bubble_center_y)**2) < BUBBLESIZE:
          self.collision_bubble = bubble
    
    x1, y1, x2, y2 = self.game_canvas.coords(self.current_bubble.get_bubble_id())
    if self.collision_bubble is None and y1 <= BUBBLESIZE * self.first_row * 0.85 + BUBBLESIZE / 2:
      self.handle_collision()
    elif self.collision_bubble is None:
      if x1 <= 0 or x2 >= WIDTH:
        bubble_direction_x *= (-1)
      self.window.after(10, self.move_bubble, bubble_direction_x, bubble_direction_y)
    else:
      self.handle_collision()
  
  def handle_collision(self):
    """
    Functie de handle in caz de coliziune.
    :param bubble_direction_x: Directia bulei pe axa X.
    :param bubble_direction_y:  Directia bulei pe axa Y.
    """
    self.current_bubble.row, self.current_bubble.col = self.new_bubble_position()
    self.current_bubble.destroy(self.game_canvas)
    self.current_bubble.draw(self.game_canvas, self.first_row)
    self.game_table[self.current_bubble.row][self.current_bubble.col] = self.current_bubble

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
  
  def find_color_matches(self, matches, bubble, visited=None):
    """
    Functie de gasire a bulelor de aceeasi culoare cu care bula curenta a interactionat.
    :param matches: Set in care pastram bulele de aceeasi culoare cu bula curenta, inclusiv pe ea.
    :param bubble: Bula pe care o verificam, impreuna cu vecinii sai.
    :param visited: Set in care punem id-urile bulelor, pentru a nu repeta procesul degeaba pentru aceeasi bula de doua sau mai multe ori.
    """
    if visited is None:
      visited = set()
    if bubble.get_bubble_id() in visited:
      return
    visited.add(bubble.get_bubble_id())
    matches.add(bubble)
    neighbor_bubbles = self.get_neighbor_bubbles(bubble)

    for neighbor in neighbor_bubbles:
      if neighbor.color == bubble.color:
        self.find_color_matches(matches, neighbor, visited)

  def get_target_bubbles(self, matches, safe_bubbles = None):
    """
    Determinarea bulelor ce trebuie eliminate pe langa cele de aceeasi culoare cu bula curenta.
    :param matches: Set in care pastram bulele de aceeasi culoare cu bula curenta, inclusiv pe ea.
    :param safe_bubbles: Dictionar in care pastram bulele ce nu trebuie eliminate.
    """
    if safe_bubbles is None:
      safe_bubbles = dict()
    for row in self.game_table:
      for bubble in row:
        if bubble:
          if (bubble.row == self.first_row) or ((bubble.row + self.first_row) % 2 == 0 and (bubble.col == 0 or bubble.col == 11)):
            self.get_safe_neighbors(bubble, matches, safe_bubbles)
    target_bubbles = [bubble for row in self.game_table for bubble in row if bubble and bubble not in safe_bubbles.values()]
    return set(target_bubbles)

  def get_safe_neighbors(self, bubble, matches, safe_bubbles):
    """
    Functie recursiva de aflare a bulelor ce nu trebuie eliminate.
    :param bubble: Bula pentru care cautam vecinii care nu trebuie eliminati.
    :param matches:  Set in care pastram bulele de aceeasi culoare cu bula curenta, inclusiv pe ea.
    :param safe_bubbles:  Dictionar in care pastram bulele ce nu trebuie eliminate.
    """
    if bubble not in matches and (bubble.row, bubble.col) not in safe_bubbles:
      safe_bubbles[(bubble.row, bubble.col)] = bubble
      neighbors = self.get_neighbor_bubbles(bubble)
      for neighbor in neighbors:
        self.get_safe_neighbors(neighbor, matches, safe_bubbles)

  def get_neighbor_bubbles(self, bubble):
    """
    Determinarea vecinilor unei bule.
    :param bubble: Bula pentru care determinam vecinii.
    """
    neighbors = []
    row, col = bubble.row, bubble.col
    if not col == 0 and self.game_table[row][col - 1]:
      neighbors.append(self.game_table[row][col - 1])
    if not col == MAXWIDTH - 1 and self.game_table[row][col + 1]:
      neighbors.append(self.game_table[row][col + 1])
    if not row == 0 and self.game_table[row - 1][col]:
      neighbors.append(self.game_table[row - 1][col])
    if row <= MAXHEIGHT and self.game_table[row + 1][col]:
      neighbors.append(self.game_table[row + 1][col])
    if (row + self.first_row) % 2 == 0:
      if not row == 0 and not col == 0 and self.game_table[row - 1][col - 1]:
        neighbors.append(self.game_table[row - 1][col - 1])
      if row <= MAXHEIGHT and not col == 0 and self.game_table[row + 1][col - 1]:
        neighbors.append(self.game_table[row + 1][col - 1])
    else:
      if not row == 0 and not col == MAXWIDTH - 1 and self.game_table[row - 1][col + 1]:
        neighbors.append(self.game_table[row - 1][col + 1])
      if row <= MAXHEIGHT and not col == MAXWIDTH - 1 and self.game_table[row + 1][col + 1]:
        neighbors.append(self.game_table[row + 1][col + 1])
    return neighbors

  def disolve_bubbles(self, bubbles):
    """
    Stergerea din tabla de joc a bulelor.
    :param bubbles: Lista cu bulele care se vor sterge din tabla de joc.
    """
    for bubble in bubbles:
      bubble.destroy(self.game_canvas)
      self.game_table[bubble.row][bubble.col] = None
      color = bubble.color
      if self.next_bubble_color is not color and not any(bubble.color == color for row in self.game_table for bubble in row if bubble):
        self.all_colors.remove(bubble.color)

  def new_bubble_position(self):
    """
    Calcularea randului si coloanei din tabla de joc a bulei care a fost trase.
    """
    bubble_center_x, bubble_center_y = self.calculate_center(self.current_bubble)
    if self.collision_bubble:
      collision_center_x, collision_center_y = self.calculate_center(self.collision_bubble)
      row = int(collision_center_y / (BUBBLESIZE * 0.85))
      col = int(collision_center_x / BUBBLESIZE)
      if (self.first_row + row) % 2 == 1:
        col -= 1 if collision_center_x % BUBBLESIZE < BUBBLESIZE / 2 else 0
      final_row, final_col = row, col
      if (row + self.first_row) % 2 == 1:
        directions = [(0, 1), (1, 0), (0, -1), (-1, 1), (-1, 0), (1, 1)]
      else:
        directions = [(0, 1), (1, 0), (0, -1), (-1, -1), (-1, 0), (1, -1)]
      min_distance = float('inf')
      for direction in directions:
        new_row, new_col = row + direction[0], col + direction[1]
        if not((self.first_row + new_row) % 2 == 1 and new_col == 11):
          if 0 <= new_row <= MAXHEIGHT and 0 <= new_col < MAXWIDTH and self.game_table[new_row][new_col] is None:
            new_center_x = (new_col * BUBBLESIZE) + BUBBLESIZE / 2 + (BUBBLESIZE /2 if (new_row + self.first_row) %  2 == 1 else 0)
            new_center_y = (new_row * BUBBLESIZE * 0.85) + BUBBLESIZE / 2
            distance = math.sqrt((bubble_center_x - new_center_x)**2 + (bubble_center_y - new_center_y)**2)
            if distance < min_distance:
              min_distance = distance
              final_row, final_col = new_row, new_col
    else:
      final_row = self.first_row
      final_col = int(bubble_center_x / BUBBLESIZE)
    return final_row, final_col

  def update_next_bubbles(self):
    """
    Actualizarea bulei curente si a celei care urmeaza.
    """
    self.current_color =  self.next_bubble_color
    self.next_bubble_color = random.choice(list(self.all_colors))
    self.next_bubble_canvas.create_oval(0, 0, 20, 20, fill = self.next_bubble_color)
    self.current_bubble = Bubble(15, 5, self.current_color)
    self.current_bubble.draw(self.game_canvas, self.first_row)

  def update_score(self, matches, target_bubbles):
    """
    Actualizarea scorului in functie de bulele ce au fost distruse.
    :param matches: Bulele alaturi de care bula curenta a declansat distrugerea.
    :param target_bubbles: Bulele care depindeau de cele ce au declansat distrugerea.
    """
    new_score = 15 * len(matches)
    for bubble in list(target_bubbles - matches):
      new_score += 3 * self.color_score[bubble.color]   
    self.score += new_score
    self.score_text.set(f"Score: {self.score}")

  def calculate_center(self, bubble):
    """
    Functie de calculare a centrului bulei date ca parametru.
    :param bubble: Bula pentru care calculam coordonatele centrului.
    """
    bubble_coords = self.game_canvas.coords(bubble.get_bubble_id())
    bubble_center_x = (bubble_coords[0] + bubble_coords[2]) / 2
    bubble_center_y = (bubble_coords[1] + bubble_coords[3]) / 2
    return bubble_center_x, bubble_center_y
  
def initial_matrix():
  """
  Initializarea matricii ce reprezinta tabela cu valori None.
  """
  return [[None for _ in range(MAXWIDTH)] for _ in range(MAXHEIGHT + 2)]