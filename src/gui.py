import pygame

#Constantes

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (120,124,127)
GREEN = (108,169,101)
YELLOW = (200,182,83)
ORANGE = (240, 146, 58)

#Classes

class Button:

    def __init__(self, text, rgb_color, x, y, width, height):
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = (x, y)
        self.text = text
        self.color = rgb_color

    def draw(self, screen, font):
        pygame.draw.rect(screen, self.color, self.rect)
        text = font.render(self.text, True, WHITE)
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

    def draw(self, screen, font):
        pygame.draw.rect(screen, self.bg_color, self.rect)
        pygame.draw.rect(screen, self.color, self.rect, 3)
        text = font.render(self.text, True, BLACK)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

#Fonctions GUI

def init_grid(screen,word_length):
    grid = []
    rows = 6

    box_size = 70
    gap = 10

    total_width = word_length * box_size + (word_length - 1) * gap

    start_x = (screen.get_width() - total_width) // 2 
    
    start_y = 10

    for i in range(rows):
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

    return grid

def init_keyboard(screen):
    
    keyboard = ["azertyuiop","qsdfghjklm","wxcvbn"]
    indicator_grid = []
    indicator_grid_rows = len(keyboard)
    keyboard_box_size = 65
    keyboard_start_y = screen.get_height() - 3 * (keyboard_box_size + 10)
    gap = 10

    for row in range(indicator_grid_rows):
        indicator_row = []
        line_length = len(keyboard[row])
        total_width = line_length * keyboard_box_size + (line_length - 1) * gap
        start_x = (screen.get_width() - total_width) // 2 
        for line in range(len(keyboard[row])):
            x = start_x + line * (keyboard_box_size + gap)
            letter = Letter(x, keyboard_start_y, keyboard_box_size, keyboard_box_size, text=keyboard[row][line])
            indicator_row.append(letter)
        keyboard_start_y += keyboard_box_size + 10
        indicator_grid.append(indicator_row)
    
    return indicator_grid



def check_input(row):
    pass