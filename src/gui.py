import pygame

pygame.init()

#Constantes

WIDTH = 1280
HEIGHT = 720
FONT = pygame.font.SysFont("arial", 50)

WHITE = (255, 0, 0)
BLACK = (0, 0, 0)

FRENCH_LANG = {"language" : "Langage: FR",
      "main_menu" : "Menu principal",
      "wordle" : "SUTOM",
      "play" : "Jouer",
      "options" : "Paramètres",
      "quit" : "Quitter",
      "back" : "Retour",
      "mode_default" : "Mode: Standard",
      "mode_intermediate" : "Mode: Intermédiaire",
      "mode_hard" : "Mode: Difficile",
      "win_message" : "Vous avez deviné le mot du jour !",
      "lose_message" : "Dommage !"}

ENGLISH_LANG = {"language": "Language: EN",
      "main_menu" : "Main menu",
      "wordle" : "Wordle",
      "play" : "Play",
      "options" : "Options",
      "quit" : "Leave",
      "back" : "Back",
      "mode_default" : "Difficulty: Standard",
      "mode_intermediate" : "Difficulty: Intermediate",
      "mode_hard" : "Difficulty: Hard",
      "win_message" : "You guessed the correct word !",
      "lose_message" : "Nice try !"}

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()
running = True

#Implémentation du visuel

#Boucle du jeu

class Button:

    def __init__(self, text, rgb_color, x, y, width, height):
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = (x, y)
        self.text = text
        self.color = rgb_color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text = FONT.render(self.text, True, (255, 255, 255))
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def on_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if (self.rect.x <= mouse_x <= self.rect.x + self.rect.width 
                    and self.rect.y <= mouse_y <= self.rect.y + self.rect.height):
                    return True
        return False
    
def main():
    lang = FRENCH_LANG
    mode_level = "default"
    screen = "menu"

    while True:

        if screen == "menu":
            screen = main_menu(lang)
        
        elif screen == "options":
            screen, lang, mode_level = options(lang, mode_level)
        
        elif screen == "play":
            play(lang, mode_level)
        else:
            break
    pygame.quit()

def play(lang,mode_level):
    pygame.display.set_caption(lang["wordle"] + " - " + lang["play"])
    while True:
        pass

def options(lang,mode_level):
    pygame.display.set_caption(lang["wordle"] + " - " + lang["options"])
    running = True

    language_btn = Button(lang["language"], BLACK, WIDTH // 2, 200, 490, 60)
    mode_btn = Button(lang["mode_" + mode_level], BLACK, WIDTH // 2, 300, 490, 60)
    back_btn = Button(lang["back"], BLACK, WIDTH // 2, 400, 490, 60)

    while running:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif language_btn.on_click(event):
                if lang == FRENCH_LANG:
                    lang = ENGLISH_LANG
                else:
                    lang = FRENCH_LANG
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
        
        SCREEN.fill((255, 255, 255))
        language_btn.draw(SCREEN)
        mode_btn.draw(SCREEN)
        back_btn.draw(SCREEN)
        pygame.display.update()
        

def main_menu(lang):
    pygame.display.set_caption(lang["wordle"] + '-' + lang["main_menu"])
    running = True

    play_btn = Button(lang["play"], BLACK, WIDTH // 2, 300, 490, 60)
    option_btn = Button(lang["options"], BLACK, WIDTH // 2, 400, 490, 60)
    quit_btn = Button(lang["quit"], BLACK, WIDTH // 2, 500, 490, 60)

    while running:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif play_btn.on_click(event):
                print("bouton jouer appuyé")
            
            elif option_btn.on_click(event):
                return "options"
            
            elif quit_btn.on_click(event):
                running = False
        
        SCREEN.fill((255, 255, 255))
        play_btn.draw(SCREEN)
        option_btn.draw(SCREEN)
        quit_btn.draw(SCREEN)
        pygame.display.update()

main()
pygame.quit()