import pygame, random, gui, script, os, json

WIDTH = 1280
HEIGHT = 720

def loadlang():
    languages = {}

    for file_name in os.listdir("lang"):
        file_path = os.path.join("lang",file_name)
        with open(file_path) as json_f:
            key_name = ""
            for char in file_name:
                if char == ".":
                    break
                else:
                    key_name += char.upper()
            languages[key_name] = json.load(json_f)

    return languages

def main(lang):
    pygame.init()

    FONT = pygame.font.SysFont("arial", 50)
    TITLE_FONT = pygame.font.SysFont("arial", 80)
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

    mode_level = "default"
    screen = "menu"
    running = True

    while running:

        if screen == "menu":
            screen = main_menu(lang, SCREEN, TITLE_FONT, FONT)
        
        elif screen == "options":
            screen, lang, mode_level = options(lang, mode_level, SCREEN, FONT)
        
        elif screen == "play":
            quit_program = play(lang, mode_level, SCREEN, FONT)
            if quit_program:
                running = False
        
        else:
            running = False
    pygame.quit()

def play(lang, mode_level, screen, font):
    pygame.display.set_caption(lang["wordle"] + " - " + lang["play"])
    running = True
    quit_program = False

    if mode_level == "default":
        grid = gui.init_grid(screen, random.randint(6,10))
    elif mode_level == "intermediate":
        grid = gui.init_grid(screen, 8)
    else:
        grid = gui.init_grid(screen, 8)
    
    indicator_grid = gui.init_keyboard(screen)

    i = 0
    current_row = grid[i]
    current_letter = current_row[0]
    current_letter.input_status = "activated"

    while running:

        screen.fill(gui.WHITE)
        for row in grid:
            for letter in row:
                letter.draw(screen, font)

        for row in indicator_grid:
            for letter in row:
                letter.draw(screen, font)

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

def options(lang, mode_level, screen, font):
    pygame.display.set_caption(lang["wordle"] + " - " + lang["options"])
    running = True
    languages_keys = list(languages.keys())

    language_btn = gui.Button(lang["language"], gui.GREEN, WIDTH // 2, 200, 490, 60)
    mode_btn = gui.Button(lang["mode_" + mode_level], gui.ORANGE, WIDTH // 2, 300, 490, 60)
    back_btn = gui.Button(lang["back"], gui.YELLOW, WIDTH // 2, 400, 490, 60)

    while running:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
                return "menu", True

            elif language_btn.on_click(event):
                limit = len(languages_keys)
                current_key = [k for k,v in languages.items() if v == lang][0]
                i = languages_keys.index(current_key)
                next_key = languages_keys[(i + 1) % limit]
                lang = languages[next_key]
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
        
        screen.fill(gui.WHITE)
        language_btn.draw(screen,font)
        mode_btn.draw(screen,font)
        back_btn.draw(screen,font)
        pygame.display.flip()
    return "menu", False
        

def main_menu(lang, screen, title_font, font):
    
    pygame.display.set_caption(lang["wordle"] + '-' + lang["main_menu"])
    running = True

    text = title_font.render(lang["wordle"], True, gui.BLACK)
    text_rect = text.get_rect(center=(screen.get_width() // 2, 120))
    play_btn = gui.Button(lang["play"], gui.GREEN, WIDTH // 2, 300, 490, 60)
    option_btn = gui.Button(lang["options"], gui.GREY, WIDTH // 2, 400, 490, 60)
    quit_btn = gui.Button(lang["quit"], gui.YELLOW, WIDTH // 2, 500, 490, 60)

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
        
        screen.fill(gui.WHITE)
        play_btn.draw(screen, font)
        option_btn.draw(screen, font)
        quit_btn.draw(screen, font)
        screen.blit(text, text_rect)
        pygame.display.update()


languages = loadlang()
default_lang = languages["FR"]
main(default_lang)
pygame.quit()