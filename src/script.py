def verification(mot_secret, mot_essayer): 
    
    resultat = []
    def occurence(mot):
        res = {}
        for i in mot:
            if i in res:
                res[i] += 1
            else:
                res[i] = 1
        return res

    occurences = occurence(mot_secret)

    for i in range(len(mot_essayer)):
        if mot_essayer[i] == mot_secret[i]:
            resultat.append("ok")
            occurences[mot_essayer[i]] -= 1
        elif mot_essayer[i] in mot_secret:
            if occurences[mot_essayer[i]] == 0:
                resultat.append("non")
            else:
                resultat.append("mal placé")
                occurences[mot_essayer[i]] -= 1
        else:
            resultat.append("non")
    
    return resultat

class Game:
    def __init__(self, mot_secret):
        self.secret = mot_secret
        self.lettre = "" # mot en cours de saisie
        self.mot_essayer = [] # historique des essais

    def ajout_lettre(self, lettre):
        self.lettre += lettre

    def supprimer_lettre(self):
        self.lettre = self.lettre[:-1]

    def valider(self):
        # vérifie si le mot est de la bonne longueur
        if len(self.lettre) != len(self.secret):
            return None
        resultat = verification(self.secret, self.lettre)
        # stocke l'essai + résultat
        self.mot_essayer.append((self.lettre, resultat))
        # reset le mot en cours
        self.lettre = ""
        return resultat

    def gagne(self):
        if not self.mot_essayer:
            return False
        # dernier mot essayé
        dernier_mot = self.mot_essayer[-1][0]
        return dernier_mot == self.secret
