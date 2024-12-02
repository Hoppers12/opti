

def algorithmeGlouton(Wmax, objets):

    P_total = 0
    score_total = 0
    inclusion = [0] * len(objets)

    for i, obj in enumerate(objets):
        if P_total + obj["poids"] <= Wmax:
            inclusion[i] = 1
            P_total += obj["poids"]
            score_total += obj["score"]

    return P_total, score_total, inclusion




def lire_fichier_instance(fichier):
    """
    Lecture d'une instance depuis un fichier.
    :param fichier: Nom du fichier contenant l'instance.
    :return: Liste des objets et poids maximum autorisé (Wmax).
    """
    objets = []
    with open(fichier, "r") as f:
        n, Wmax = map(int, f.readline().split())  # Lire le nombre d'objets et Wmax

        for ligne in f:
            _, poids, score = map(int, ligne.split())
            objets.append({"poids": poids, "score": score})

    return objets, Wmax

def sommePoids(objets) :
    somme = 0

    if (objets == []) :
        return 0
    else :
        for element in objets :
            somme+= element['poids']
        return somme


def algoBranchAndBound(Wmax,S, best,stats, best_poids) :
    UB = evalS(S)
    poids = evalPoids(S)
    #L correspond aux variables pas encore placés pour le noeud S
    L=S[2]
    stats["noeuds"] +=1
    if Wmax >= poids:
        if L == [] :
            if UB > best:
                best = UB
                #Permet de stocker le poids associé au best score
                best_poids = poids

        else :
            if UB >= best :
                x = choisirVariable(L,Wmax)
                S[0].append(x)
                best, best_poids = algoBranchAndBound(Wmax,[S[0],S[1],L],best,stats, best_poids)
                #on retire la valeur qu'on a ajouté à S[O] au dessus puis on l'ajoute à S[1]
                S[0].pop()
                S[1].append(x)
                best, best_poids = algoBranchAndBound(Wmax,[S[0], S[1], L],best,stats,best_poids)
            else:
                stats['eval_coupe'] += 1  # UB < best a échoué (coupe par evaluation de noeud)
    else:
        stats['contrainte_coupe'] += 1  # Wmax >= poids a échoué (violation de contrainte)
    return best, best_poids

 #On retire de la liste la variable que l'on analyse et on la retourne
def choisirVariable(L,Wmax):
    return L.pop(0)

#Retourne le poids d'un noeud S (somme des poids des variables deja choisies)
def evalPoids(S):
    var_choisi = S[0]
    somme_poids = 0

    # Calculer la somme des scores dans la liste d'indice 0 (deja choisi)
    somme_poids += sum(item['poids'] for item in var_choisi)

    return somme_poids


#Retourne le score maximum qu'un noeuf pourra engendré (somme des x choisis  et des x dans L)
def evalS(S) :

    var_choisi = S[0]
    var_potentielle = S[2]
    somme_scores = 0

    # Calculer la somme des scores dans la liste d'indice 0 (deja choisi)
    somme_scores += sum(item['score'] for item in var_choisi)

    # Calculer la somme des scores dans la liste L
    somme_scores += sum(item['score'] for item in var_potentielle)


    return somme_scores

#Liste des fichiers d'instances
instances = ["inst4obj.txt", "inst5obj.txt", "inst10obj.txt","inst20obj.txt","inst30obj.txt","inst35obj.txt","inst40obj.txt","inst50obj.txt","inst70obj.txt","inst100obj.txt"]


for element in instances :

    Wmax = lire_fichier_instance(element)[1]
    objets = lire_fichier_instance(element)[0]

    result_glouton = algorithmeGlouton(Wmax,objets)
    best = 0
    #1er appel : On donne à L toutes les variables (objets) car aucun n'a été fixé
    # S = [objets fixé à 1, objets fixés à 0, tous les objets non fixés]
    L = objets
    S=[[],[],L]
    stats = {'noeuds': 0, 'contrainte_coupe': 0, 'eval_coupe': 0}  # Statistiques initiales

    print("resultat du glouton : ", algorithmeGlouton(Wmax,objets))
    print("Result Branch and bound : ", algoBranchAndBound(Wmax, S, best, stats, 0), stats)


