import pygame, unidecode, script, gui, sys, os, time

WIDTH = 1280
HEIGHT = 720

gui_mode = False

def demo_window(screen, font, inputs, testname):
    
    pygame.display.set_caption("Wordle - " + testname)
    running = True

    indicator_grid = gui.init_keyboard(screen)
    grid = gui.init_grid(screen,len(inputs[0][0]))
    
    i = 0
    for t in inputs:
        current_try = t[0].strip().upper()
        resultat = t[1]
        for letter in range(len(current_try)):
            grid[i][letter].text = current_try[letter]
            
        gui.change_letter_colors(indicator_grid, grid[i], resultat)
        i += 1
            
            
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
        
        pygame.display.flip()
    
    pygame.quit()

def test_script(inputs, gui_mode, testname):
    secret_word = inputs[0]
    inputs = inputs[1:]
    secret_word = unidecode.unidecode(secret_word.strip().upper())
    game = script.Game(secret_word)
    current_tries = 0
    max_tries = 6
    win = False
    print("----Lecture du test---- \n")
    print(f"Nom du test: {testname}")
    print(f"Le mot secret à deviner est: {secret_word} \n")

    for word in inputs:
        if len(word) != len(secret_word):
            print(f"Longueur du mot {word} inégale avec la longueur du mot secret. Arrêt")
            break
        else:
            current_try = word.strip().upper()
            if current_tries > max_tries:
                print("----Affichage des résultas----")
                print("Vous avez perdu ! \nNombre d'essais: 6/6")
                break
        
            print(f"----Essai numéro {current_tries + 1}----")
            print(f"Mot en cours d'essai: {current_try} \n")
            game.lettre = current_try
            resultat = game.valider()
        
            print("Résultats: ")
            for i in range(len(current_try)):
                print(f"{current_try[i]}[{resultat[i]}]", end="")
            print("\n")
        
            current_tries += 1
            if current_try == game.secret:
                print("Vous avez gagné ! \n",f"Nombre d'essais: {len(game.mot_essayer)}/6 \n")
                win = True
                break

    if current_tries < 6 and not win:
        print("----Affichage des résultats---- \n")
        print(f"Le fichier ne contient pas suffisament de mots pour déterminer l'issue. \n Nombre d'essais: {current_tries}/6 \n")


    if gui_mode:
        print("Mode GUI activé. Pour arrêter le programme, fermez la fenêtre Pygame")
    
        font_path = "../assets/fonts/RobotoMono-VariableFont_wght.ttf"
        FONT = pygame.font.Font(font_path, 34)
        SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
        demo_window(SCREEN, FONT, game.mot_essayer, testname)

if len(sys.argv) != 3:
    print(" \n usage: python3 tests.py file_path gui_on/gui_off")
    exit(0)
elif not os.path.exists(sys.argv[1]):
    print(" \n Incorrect path to file \n")
    print("usage: python3 tests.py file_path gui_on/gui_off")
    exit(0)
elif sys.argv[2] == "gui_on":
    gui_mode = True
elif sys.argv[2] == "gui_off":
    gui_mode = False
else:
    print("\nPlease specify for GUI usage \n")
    print("usage: python3 tests.py file_path gui_on/gui_off")
    exit(0)
    
if gui_mode:
    pygame.init()
    
if os.path.isfile(sys.argv[1]):
    path_type = "file"
else:
    if sys.argv[2] == "gui_on":
        print("L'exécution du code sur un dossier avec le GUI activé n'est pas possible.")
        exit(0)
    path_type = "dir"

if path_type == "file":
    with open(sys.argv[1]) as f:
        inputs = f.read().splitlines()
    testname = sys.argv[1]
    test_script(inputs, gui_mode, testname)
else:
    path = sys.argv[1]
    all_files = os.listdir(path)
    print("--------------------DEBUT DU TEST--------------------\n")
    for file in all_files:
        with open(f"{path}/{file}") as f:
            inputs = f.read().splitlines()
            testname = file
        test_script(inputs, gui_mode, testname)
    print("--------------------FIN DU TEST--------------------\n")

