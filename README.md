# Jeu du SUTOM

## Auteurs et Collaborateurs

### Première partie

_Développement du fonctionnement de base du jeu et de l'interface:_

- **Développement front-end:** [Sofia CETIN](https://code.up8.edu/scetin)
- **Développement back-end:** [Eliase TABBAHK](https://code.up8.edu/etabbakh)

### Deuxième partie

_Développement du solveur:_

- **À déterminer**

## Présentation du SUTOM

Le SUTOM(également connu sous son équivalent anglais Wordle), est un jeu de devinettes de mots. Le concept est simple: l'utilisateur possède un certain nombre de chances pour deviner un mot d'une longueur variable de 6 à 10 lettres. Si l'utilisateur ne devine pas le mot à l'issue de ces 6 chances, il a perdu, et inversement, il gagne.

<img src="assets/grille-sutom-2589165-1200x900.jpg" width="300" alt="Une image du jeu SUTOM français">

_Une image du jeu SUTOM_

## Utilisation

### Prérequis

Ce programme Python fonctionne avec l'import Pygame. Afin de l'installer vous pouvez exécuter la commande pip suivante dans le terminal:

```bash
$pip install pygame
```

Pour plus d'informations sur ce package, vous pouvez consulter le lien officiel de la documentation.
**[Documentation Pygame](https://www.pygame.org/wiki/GettingStarted)**

Vous pouvez également configurer un environnement virtuel pour ne pas avoir à installer le package sur toute votre machine. 
**[Créer un environnement Python virtuel](https://docs.python.org/fr/3.9/library/venv.html)**

_**Attention:** Pygame ne peut pas être installé sous les versions Python 3.14+ faute de mises à jour. C'est pour cela que je vous conseille de déployer un environnement virtuel sous une autre version de Python, comme la version 3.13.9._

### Téléchargement

Une fois le package pygame installé, vous pouvez télécharger le code source du programme afin de l'exécuter, comme suit:

<img src="assets/image_readme.png" width="300" alt="Une image du jeu SUTOM français">

Vous pouvez également cloner le dépôt avec SSH ou HTTPS.

### Exécution

**Si vous souhaitez jouer:**  Vous pouvez vous positionner dans le répertoire source, et lancer avec la commande

```bash
$python3 main.py
```

**Si vous souhaitez exécuter les démos:** Vous pouvez lancer dans le répertoire source la commande, avec le fichier test désiré

```bash
$python3 tests.py < ../tests/test.txt
```

_Notez que les démos avec l'interface graphique ne sont pas disponibles et complexes à implémenter. On n'utilisera donc que l'output du terminal._