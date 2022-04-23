from tkinter import *
from math import *
from time import *
class Graphe(object):
    def __init__(self,graphe_dict=None):
        if graphe_dict==None:
            graphe_dict={}
        self._graphe_dict = graphe_dict

    def arretes(self,sommet):
        return self._graphe_dict[sommet]
    def arretes_liste(self,sommet):
        a=[]
        if sommet in self._graphe_dict[sommet]:
            for b in self._graphe_dict[sommet]:
                a.append(b)
        return a
    def all_sommets(self):
        a=[]
        for i in self._graphe_dict:
            a.append(i)
        return a

    def all_arretes(self):
        return self.__list_aretes()

    def add_sommet(self,sommet):
        if sommet not in self._graphe_dict:
            self._graphe_dict[sommet]=list()
        else:
            print("Element déjà existant")

    def add_arete(self,arete):
        self._graphe_dict[arete[0]].append(arete[1])

    def __list_aretes(self):
        a=[]
        for i in self._graphe_dict:
            for j in self._graphe_dict[i]:
                a.append(set((i,j)))
        return a

    def __iter__(self):
        self._iter_obj= iter(self._graphe_dict)
        return self._iter_obj

    def __next__(self):
        return next(self._iter_obj)

    def __str__(self):
        res="sommets: "
        for k in self._graphe_dict:
            res+=str(k) + " "
        res+="\naretes: "
        for arete in self.__list_aretes():
            res+=str(arete) + " "
        return res
    def nombrepossibilite(self,liste,som):
        T=dict() # dictionnaire qui associe pour chaque sommets liés au sommet passé en paramètre et qui n'est pas encore visité, le nombre de sommmets que le prochain sommet peut encore visiter
        for j in self.arretes(som):
            if liste[j]==0:
                T[j]=0
                for h in self._graphe_dict[j]:
                    if liste[h]==0:
                        T[j]+=1
        res=[]
        for i in range(len(T)): # transforme le dictionnaire en liste en gardant que les indices et en le triant
            min=len(self.all_sommets())+1
            indmin=len(self.all_sommets())+1
            for i in T.keys():
                if T[i]<min:
                    min=T[i]
                    indmin=i
            res.append(indmin)
            T.pop(indmin)
        return res
    def cavalier(self,dep,taille,somvisite=0,liste=[]):
        if dep[0]>=0 and dep[0]<taille and dep[1]>=0 and dep[1]<taille: # vérification que le sommet passé en paramètre soit bien valide
            if liste==[]: # si c'est la première occurence
                liste=[0 for i in range(taille*taille)] # créer un échiquier avec uniquement des 0 (0 signifiant sommet non visité)
            somvisite+=1 # correspond au nombre de sommets visités
            liste[dep[0]+(dep[1]*taille)]=somvisite # place le sommet passé en paramètre à "visité" (somvisite)
            if somvisite!=taille**2: # si tous les sommets n'ont pas encore été visités
                voisin=self.nombrepossibilite(liste,dep[0]+dep[1]*taille) # récupère les prochains sommets visitable par ordre de priorité, le premier sommet de la liste est celui qui après aura le moins de sommet suivant
                for mov in voisin: # pour chaque sommet visitable
                    y=mov//taille # calcul des
                    x=mov%taille  # coordonnées
                    somvisite,liste=self.cavalier([x,y],taille,somvisite,liste) #passe au sommet suivant
                    if somvisite==taille**2: # si une solution a été trouvée
                        return somvisite,liste # renvoie la liste et le nombre de sommets visités
                    else:
                        liste[liste.index(somvisite)]=0 #supprimer les valeurs si le chemin n'avait pas d'issue
                        somvisite-=1 # decrémente somvisite
            return somvisite,liste # renvoie la liste et le nombre de sommets visités
    def cavaliercycle(self,suivant,taille,somvisite=0,liste=[],dep=None):
        if suivant[0]>=0 and suivant[0]<taille and suivant[1]>=0 and suivant[1]<taille: # vérification que le sommet passé en paramètre soit bien valide
            if liste==[]: # si c'est la première occurence
                dep=suivant
                liste=[0 for i in range(taille*taille)] # créer un échiquier avec uniquement des 0 (0 signifiant sommet non visité)
            somvisite+=1 # correspond au nombre de sommets visités
            liste[suivant[0]+(suivant[1]*taille)]=somvisite # place le sommet passé en paramètre à "visité" (somvisite)
            if somvisite!=taille**2 and (0 in [liste[i] for i in self._graphe_dict[dep[0]+dep[1]*taille]]): # si tous les sommets n'ont pas encore été visités et qu'il existe au moins un sommet voisin du sommet de départ encore non-visité
                voisin=self.nombrepossibilite(liste,suivant[0]+suivant[1]*taille) # récupère les prochains sommets visitable par ordre de priorité, le premier sommet de la liste est celui qui après aura le moins de sommet suivant
                for mov in voisin: # pour chaque sommet visitable
                    y=mov//taille # calcul des
                    x=mov%taille  # coordonnées
                    somvisite,liste=self.cavaliercycle([x,y],taille,somvisite,liste,dep) #passe au sommet suivant
                    if somvisite==taille**2 and somvisite in [liste[i] for i in self._graphe_dict[dep[0]+dep[1]*taille]]: # si une solution a été trouvée
                        return somvisite,liste # renvoie la liste et le nombre de sommets visités
                    else:
                        liste[liste.index(somvisite)]=0 #supprimer les valeurs si le chemin n'avait pas d'issue
                        somvisite-=1 # decrémente somvisite
            return somvisite,liste # renvoie la liste et le nombre de sommets visités



"""Cette fonction a pour but de créer un graphe avec toutes les sauts possibles entre les points"""
def creation_graphe(taille):
    T=Graphe() #initialisation d'un grapge
    voisin=[(-2,-1),(-2,1),(-1,-2),(-1,2),(2,-1),(2,1),(1,-2),(1,2)] # mouvement de cavalier possible
    for y in range(taille):
        for x in range(taille):
            T.add_sommet(x+y*taille)
            for mov in voisin:
                if mov[0]+x>=0 and mov[0]+x<taille and mov[1]+y>=0 and mov[1]+y<taille:
                    mouvement=(x+mov[0])+(y+mov[1])*taille
                    if mouvement>=0 and mouvement<taille*taille:
                        T.add_arete([x+y*taille,mouvement])
    return T
"""Cette fonction sert a générer un damier avec tkinter"""
def damier(taille,taille_carre,can):
	y = 0
	while y < taille:
		if y % 2 == 0: # Décale une fois sur deux
			x = 0      # la position du premier carré noir
		else:
			x = 1
		carre_noir(x*taille_carre, y*taille_carre,taille,taille_carre,can)
		y += 1
"""Cette fonction sert a afficher le parcours suivi par le programme sur le damier"""
def creation_parcours(can,taille_carre,liste):
    taille=sqrt(len(liste))
    ajout=taille_carre/2
    dep=liste.index(1)
    y=(dep//taille)*taille_carre+ajout
    x=(dep%taille)*taille_carre+ajout
    r=taille_carre/2
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    can.create_oval(x0, y0, x1, y1,fill="green") # place un rond vert sur le sommet de départ
    fin=liste.index(len(liste))
    y=(fin//taille)*taille_carre+ajout
    x=(fin%taille)*taille_carre+ajout
    r=taille_carre/2
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    can.create_oval(x0, y0, x1, y1,fill="blue") # place un rond bleu sur le sommet d'arrivée
    for i in range(1,len(liste)):
        point1=liste.index(i)
        point2=liste.index(i+1)
        y1=(point1//taille)*taille_carre+ajout
        x1=(point1%taille)*taille_carre+ajout
        y2=(point2//taille)*taille_carre+ajout
        x2=(point2%taille)*taille_carre+ajout
        can.create_oval(x1-taille_carre/20,y1-taille_carre/20,x1+taille_carre/20,y1+taille_carre/20,fill="red") # crée un petit rond sur chaque sommets
        can.create_line(x1,y1,x2,y2,fill="red") # crée une ligne entre le sommet visité et le prochain sommet

"""Cette fonction sert a créer in carre noir"""
def carre_noir(x, y,taille,taille_carre,can):
    i = 0
    nb=taille//2
    if taille%2!=0:
        nb+=1
    while i < nb:
    	can.create_rectangle(x, y, x+taille_carre, y+taille_carre, fill = "black")
    	i += 1
    	x += taille_carre * 2

"""Cette fonction génère la fenêtre tkinter"""
def affichage(liste,taille):
    taille_carre = 750/taille # permet de définir une taille de damier modifiable
    fen = Tk()
    fen.title("Problème du cavalier")
    can = Canvas(fen, width = taille_carre * taille, height = taille_carre * taille, bg = "white")
    can.pack(side = TOP, padx = 5, pady = 5)
    damier(taille,taille_carre,can)
    creation_parcours(can,taille_carre,liste)
    fen.mainloop()

"""Cette fonction sert a faire un affichage secondaire en ligne de commande"""
def affichage_ligne(liste,n):
    a=0
    for i in range(n):
        for j in range(n):
            if liste[a]<100:
                print("0",end="")
            if liste[a]<10:
                print("0",end="")
            print(liste[a]," ",end="")
            a+=1
        print("")

"""Cette fonction s'occuper de tous les lancements de fonctions nécessaires"""
def probleme(dep,taille):
    T=creation_graphe(taille)
    somvisite,liste=T.cavalier(dep,taille)
    if somvisite==taille**2:
        affichage_ligne(liste,taille)
        affichage(liste,taille)
    else:
        print("Pas de solution")

def probleme_cycle(dep,taille):
    T=creation_graphe(taille)
    somvisite,liste=T.cavaliercycle(dep,taille)
    if somvisite==taille**2:
        affichage_ligne(liste,taille)
        affichage(liste,taille)
    else:
        print("Pas de solution")


n=8 # nombre a changer pour définir la taille de l'échiquier ( de 2 à 30 pour le parcours et de 2 à 10 pour le cycle)
probleme_cycle([0,0],n)
probleme([0,0],n)