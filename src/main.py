import pygame, random, gui, script, os, json, sys

WIDTH = 1280
HEIGHT = 720
possible_tries = ["CHOCOLAT","VOLCANOS","CLAVIERS","FRAGILES","ENTENDRE","FRANCAIS","FRAISIER"]

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

#Fonction de boucle principale et gestion des fenêtres

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
            screen, lang, results, secret_word, quit_program = play(lang, mode_level, SCREEN, FONT)
            if quit_program:
                running = False
        
        elif screen == "win_message":
            screen = win_screen(results, lang, secret_word, SCREEN, FONT)
            if quit_program:
                running = False
        
        elif screen == "lose_message":
            screen = lose_screen(results, lang, secret_word, SCREEN, FONT)

        else:
            running = False

    pygame.quit()

#Fonctions de fenêtres

def win_screen(results, lang, secret_word, screen, font):
    pygame.display.set_caption(lang["wordle"] + ' - ' + lang["win"])
    text = font.render(lang["win_message"], True, gui.GREEN)
    text_rect = text.get_rect(center=(screen.get_width() // 2, 150))
    text2 = font.render(lang["daily_word"] + secret_word, True, gui.BLACK)
    text_rect2 = text2.get_rect(center=(screen.get_width() // 2, 250))
    text3 = font.render(lang["nb_of_tries"] + str(len(results) + 1), True, gui.BLACK)
    text_rect3 = text3.get_rect(center=(screen.get_width() // 2, 350))

    menu_btn = gui.Button(lang["main_menu"], gui.GREY, WIDTH // 2, 450, 490, 60)
    quit_btn = gui.Button(lang["quit"], gui.YELLOW, WIDTH // 2, 550, 490, 60)

    running = True

    while running:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            elif menu_btn.on_click(event):
                return "menu"
            
            elif quit_btn.on_click(event):
                running = False
        
        screen.fill(gui.WHITE)
        menu_btn.draw(screen, font)
        quit_btn.draw(screen, font)
        screen.blit(text, text_rect)
        screen.blit(text2, text_rect2)
        screen.blit(text3, text_rect3)
        pygame.display.flip()

def lose_screen(results, lang, secret_word, screen, font):
    pygame.display.set_caption(lang["wordle"] + ' - ' + lang["lose"])
    text = font.render(lang["lose_message"], True, gui.RED)
    text_rect = text.get_rect(center=(screen.get_width() // 2, 150))
    text2 = font.render(lang["daily_word"] + secret_word, True, gui.BLACK)
    text_rect2 = text2.get_rect(center=(screen.get_width() // 2, 250))
    text3 = font.render(lang["nb_of_tries"] + str(len(results) + 1), True, gui.BLACK)
    text_rect3 = text3.get_rect(center=(screen.get_width() // 2, 350))

    menu_btn = gui.Button(lang["main_menu"], gui.GREY, WIDTH // 2, 400, 490, 60)
    quit_btn = gui.Button(lang["quit"], gui.YELLOW, WIDTH // 2, 500, 490, 60)

    running = True

    while running:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            elif menu_btn.on_click(event):
                return "menu"
            
            elif quit_btn.on_click(event):
                pygame.quit()
                sys.exit()
        
        screen.fill(gui.WHITE)
        menu_btn.draw(screen, font)
        quit_btn.draw(screen, font)
        screen.blit(text, text_rect)
        screen.blit(text2, text_rect2)
        screen.blit(text3, text_rect3)
        pygame.display.flip()

def play(lang, mode_level, screen, font):
    pygame.display.set_caption(lang["wordle"] + " - " + lang["play"])
    running = True
    quit_program = False
    

    if mode_level == "default":
        word_length = random.randint(6,10)
        grid = gui.init_grid(screen, word_length)
    elif mode_level == "intermediate":
        word_length = 8
        grid = gui.init_grid(screen, 8)
    else:
        word_length = 10
        grid = gui.init_grid(screen, 10)
    
    secret_word = "ENTENDRE"
    game = script.Game(secret_word.upper())
    
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
                pygame.quit()
                sys.exit()

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
                            guess = get_word(current_row)
                            game.lettre = guess
                            if game.lettre not in possible_tries:
                                current_letter = reset_row(current_row)
                            else:
                                resultat = script.verification(game.secret, guess)
                                correct = ["ok" for i in range(word_length)]
                                if resultat == correct:
                                    gui.win_anim(screen, font, indicator_grid, grid, current_row)
                                    return "win_message", lang, game.mot_essayer, secret_word, quit_program
                                else:
                                    if i == 5:
                                        gui.lose_anim(screen, font, resultat, indicator_grid, grid, current_row)
                                        return "lose_message", lang, game.mot_essayer, secret_word, quit_program
                                    else:
                                        gui.change_letter_colors(indicator_grid, current_row, resultat)
                                        i += 1
                                        current_row = grid[i]
                                        current_letter = current_row[0]
                                        current_letter.input_status = "activated"

                                    game.mot_essayer.append(guess)

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
                pygame.quit()
                sys.exit()

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
                pygame.quit()
                sys.exit()

            elif play_btn.on_click(event):
                return "play"
            
            elif option_btn.on_click(event):
                return "options"
            
            elif quit_btn.on_click(event):
                pygame.quit()
                sys.exit()
        
        screen.fill(gui.WHITE)
        play_btn.draw(screen, font)
        option_btn.draw(screen, font)
        quit_btn.draw(screen, font)
        screen.blit(text, text_rect)
        pygame.display.update()
    
#Fonctions utilitaires

def get_word(row):
    word = ""
    for letter in row:
        word += letter.text
    return word

def reset_row(row):
    for letter in row:
        letter.text = ''
        letter.exec = "writable"
        letter.input_status = "deactivated"
    row[0].input_status = "activated"
    return row[0]


languages = loadlang()
default_lang = languages["FR"]
main(default_lang)
pygame.quit()