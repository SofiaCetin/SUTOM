import pygame, random, json, os

pygame.init()

#Constantes

WIDTH = 1280
HEIGHT = 720
FONT = pygame.font.SysFont("arial", 50)
TITLE_FONT = pygame.font.SysFont("arial", 80)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (120,124,127)
GREEN = (108,169,101)
YELLOW = (200,182,83)
ORANGE = (240, 146, 58)

languages = []

for file in os.listdir("lang"):
    file_path = os.path.join("lang",file)
    with open(file_path) as json_f:
        file = json.load(json_f)
        languages.append(file)

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()

#Classes

class Button:

    def __init__(self, text, rgb_color, x, y, width, height):
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = (x, y)
        self.text = text
        self.color = rgb_color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text = FONT.render(self.text, True, WHITE)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def on_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if (self.rect.x <= mouse_x <= self.rect.x + self.rect.width 
                    and self.rect.y <= mouse_y <= self.rect.y + self.rect.height):
                    return True
        return False

class Letter:

    def __init__(self, x, y, width, height, text='', exec="writable", color="GREY", bg_color="WHITE", input_status="deactivated", next = "", previous = ""):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.exec = exec
        self.input_status = input_status
        self.color = color
        self.bg_color = bg_color
        self.next = next 
        self.previous = previous

    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, self.rect)
        pygame.draw.rect(screen, self.color, self.rect, 3)
        text = FONT.render(self.text, True, BLACK)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

#Fonctions de jeu
    
def main():
    lang = languages[1]
    mode_level = "default"
    screen = "menu"
    running = True

    while running:

        if screen == "menu":
            screen = main_menu(lang)
        
        elif screen == "options":
            screen, lang, mode_level = options(lang, mode_level)
        
        elif screen == "play":
            quit_program = play(lang, mode_level)
            if quit_program:
                running = False
        
        else:
            running = False
    pygame.quit()

def play(lang,mode_level):
    pygame.display.set_caption(lang["wordle"] + " - " + lang["play"])
    running = True
    quit_program = False

    if mode_level == "default":
        word_length = random.randint(6,10)
    elif mode_level == "intermediate":
        word_length = 8
    else:
        word_length = 10

    grid = []
    rows = 6

    box_size = 70
    gap = 10

    total_width = word_length * box_size + (word_length - 1) * gap

    start_x = (SCREEN.get_width() - total_width) // 2 
    
    start_y = 10

    for row in range(rows):
        row_list = []

        first_x = start_x
        first_y = start_y
        first_letter = Letter(first_x,first_y,box_size,box_size)
        first_letter.previous = None
        previous_letter = first_letter
        row_list.append(first_letter)
        for col in range(1,word_length):
            x = start_x + col * (box_size + gap)
            y = start_y
            letter = Letter(x,y,box_size,box_size)
            previous_letter.next = letter
            letter.previous = previous_letter
            previous_letter = letter
            row_list.append(letter)

        start_y += box_size + 10
        row_list[-1].next = None
        grid.append(row_list)
    
    keyboard = ["azertyuiop","qsdfghjklm","wxcvbn"]
    indicator_grid = []
    indicator_grid_rows = len(keyboard)
    keyboard_box_size = 65
    keyboard_start_y = SCREEN.get_height() - 3 * (keyboard_box_size + 10)

    for row in range(indicator_grid_rows):
        indicator_row = []
        line_length = len(keyboard[row])
        total_width = line_length * keyboard_box_size + (line_length - 1) * gap
        start_x = (SCREEN.get_width() - total_width) // 2 
        for line in range(len(keyboard[row])):
            x = start_x + line * (keyboard_box_size + gap)
            letter = Letter(x, keyboard_start_y, keyboard_box_size, keyboard_box_size, text=keyboard[row][line])
            indicator_row.append(letter)
        keyboard_start_y += keyboard_box_size + 10
        indicator_grid.append(indicator_row)

    i = 0
    current_row = grid[i]
    current_letter = current_row[0]
    current_letter.input_status = "activated"

    while running:

        SCREEN.fill(WHITE)
        for row in grid:
            for letter in row:
                letter.draw(SCREEN)

        for row in indicator_grid:
            for letter in row:
                letter.draw(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                quit_program = True

            elif event.type == pygame.KEYDOWN:
                if current_letter.input_status == "activated":
                    if event.key == pygame.K_BACKSPACE:
                        if current_letter.text != "":
                            current_letter.text = ""
                            current_letter.exec = "writable"
                        elif current_letter.previous:
                            current_letter.input_status = "deactivated"
                            current_letter = current_letter.previous
                            current_letter.input_status = "activated"
                            current_letter.text = ""
                            current_letter.exec = "writable"

                    elif event.unicode.isalpha():
                        if current_letter.text == "":
                            current_letter.text = event.unicode.upper()
                            current_letter.exec = "clearable"
                        if current_letter.text != "" and current_letter.next:
                            current_letter.input_status = "deactivated"
                            current_letter = current_letter.next
                            current_letter.input_status = "activated"
                
                    elif event.key == pygame.K_RETURN:
                        if current_letter.next == None and current_letter.text != "":
                            current_letter.input_status = "deactivated"
                            if i < 5:
                                i += 1
                                current_row = grid[i]
                                current_letter = current_row[0]
                                current_letter.input_status = "activated"

        pygame.display.flip()
    return "menu", quit_program

def options(lang,mode_level):
    pygame.display.set_caption(lang["wordle"] + " - " + lang["options"])
    running = True

    language_btn = Button(lang["language"], GREEN, WIDTH // 2, 200, 490, 60)
    mode_btn = Button(lang["mode_" + mode_level], ORANGE, WIDTH // 2, 300, 490, 60)
    back_btn = Button(lang["back"], YELLOW, WIDTH // 2, 400, 490, 60)

    while running:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
                return "menu", True

            elif language_btn.on_click(event):
                limit = len(languages)
                i = languages.index(lang)
                lang = languages[(i + 1) % limit]
                return "options", lang, mode_level
            
            elif mode_btn.on_click(event):
                if mode_level == "default":
                    mode_level = "intermediate"
                elif mode_level == "intermediate":
                    mode_level = "hard"
                else:
                    mode_level = "default"
                return "options", lang, mode_level
            
            elif back_btn.on_click(event):
                return "menu", lang, mode_level
        
        SCREEN.fill(WHITE)
        language_btn.draw(SCREEN)
        mode_btn.draw(SCREEN)
        back_btn.draw(SCREEN)
        pygame.display.flip()
    return "menu", False
        

def main_menu(lang):
    pygame.display.set_caption(lang["wordle"] + '-' + lang["main_menu"])
    running = True

    text = TITLE_FONT.render(lang["wordle"], True, BLACK)
    text_rect = text.get_rect(center=(SCREEN.get_width() // 2, 120))
    play_btn = Button(lang["play"], GREEN, WIDTH // 2, 300, 490, 60)
    option_btn = Button(lang["options"], GREY, WIDTH // 2, 400, 490, 60)
    quit_btn = Button(lang["quit"], YELLOW, WIDTH // 2, 500, 490, 60)

    while running:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif play_btn.on_click(event):
                return "play"
            
            elif option_btn.on_click(event):
                return "options"
            
            elif quit_btn.on_click(event):
                running = False
        
        SCREEN.fill(WHITE)
        play_btn.draw(SCREEN)
        option_btn.draw(SCREEN)
        quit_btn.draw(SCREEN)
        SCREEN.blit(text, text_rect)
        pygame.display.update()

def check_input(row):
    pass

main()
pygame.quit()