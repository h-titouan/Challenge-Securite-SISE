
import numpy as np
# Fonction pour tirage aléatoire selon le nombre de lignes voulues par l'utilisateur

# Fonctions utilisées dans la fonction principale :
def nb_lignes(nomFichier = "logs_bruts.csv"):

    fin = open(nomFichier, 'r')

    i = 0

    for s in fin:
        i = i+1
    
    fin.close()

    return i-1

def extraction(source, n, N):
    
    lire = open(source, 'r')
    s = lire.readline()
    if len(data < 1):
        data = s
    else:
        data.append(s)

    cpt = 0

    while(n>0):

        s = lire.readline()

        if(N * np.random.rand() <= n):

            data.append(s)

            n -=1

            cpt += 1

        N -= 1
    
    lire.close()

    return data    

# Lancer les fonctions pour afficher le dataframe
N = nb_lignes(nomFichier = "logs_bruts.csv")
data = extraction(source = "logs_bruts.csv", n = 10000, N = N)



