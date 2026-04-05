import script

mode = input()

secret_word = input().strip().upper()
game = script.Game(secret_word)
max_tries = 6
current_tries = 0

try:
    while True:
        current_try = input().strip().upper()
        if current_tries == max_tries:
            print("Nombre d'essais dépassé, vous avez perdu")
            break

        game.lettre = current_try
        resultat = game.valider()

        if resultat is None:
            print("Mot de longueur incorrecte")
            continue

        for i in range(len(current_try)):
            print(f"{current_try[i]}[{resultat[i]}]", end="")
        print("\n")
            
        current_tries += 1
        if current_try == game.secret:
            print("Gagné !",f"Essais: {len(game.mot_essayer)}")
            break

except EOFError:
    print("Perdu",f"Essais: {len(game.mot_essayer)}")
    pass