from tkinter import *
from tkinter import font as tkfont
from random import randint
from PIL import Image, ImageTk 


tk = Tk()

#on met en place les prérequis pour le poison
pommes_mangees = 0
murs_fatals = False
controles_inverses = False

#on associe les images aux objects ( il se pourrait que ça ne marche pas sur tous les ordinateurs car ça marche seulement si les images sont dans le meme fichier que le programme)
im_teteN = Image.open("teteN.png") 
teteN = ImageTk.PhotoImage(im_teteN) 
im_teteS = Image.open("teteS.png") 
teteS = ImageTk.PhotoImage(im_teteS) 
im_teteE = Image.open("teteE.png") 
teteE = ImageTk.PhotoImage(im_teteE) 
im_teteW = Image.open("teteW.png") 
teteW = ImageTk.PhotoImage(im_teteW) 
im_noeud1 = Image.open("noeud1.png") 
noeud1 = ImageTk.PhotoImage(im_noeud1) 
im_noeud2 = Image.open("noeud2.png") 
noeud2 = ImageTk.PhotoImage(im_noeud2)
pomme = Image.open("pomme.png") 
pomme = ImageTk.PhotoImage(pomme)
im_poison = Image.open("poison.png")
poison_img = ImageTk.PhotoImage(im_poison)

#on met en place des fonctions pour déterminer la direction du joueur
def right(event):
    global direction, controles_inverses
    if controles_inverses == True:
        direction = 'left'
    else:
        direction = 'right'
    
def left(event):
    global direction, controles_inverses
    if controles_inverses == True:
        direction = 'right'
    else:
        direction = 'left'
    
def down(event):
    global direction, controles_inverses
    if controles_inverses == True:
        direction = 'up'
    else:
        direction = 'down'
    
def up(event):
    global direction, controles_inverses
    if controles_inverses == True:
        direction = 'down'
    else:
        direction = 'up'
    
def reset_effets():
    global murs_fatals, controles_inverses
    murs_fatals = False
    controles_inverses = False

#on calcule la frame actuelle 
def computeNextFrame(numFrame,coordonnee, objet):
    global direction, murs_fatals, controles_inverses, pommes_mangees
    numFrame+= 1
    can.delete('all')
    game_over = False
    #on calcule le déplacement de la queue
    for n in range (len(coordonnee)-1,0,-1):
        coordonnee[n][0] = coordonnee[n-1][0]
        coordonnee[n][1] = coordonnee[n-1][1]
    
    #on définit le déplacement/les coordonnées du joueur et on change le sprit de la tete en fonction de sa direction
    if direction == 'right':
        coordonnee[0][0] += 20
        if coordonnee[0][0] > 480:
            if murs_fatals == True:
                game_over = True
            else:
                coordonnee[0][0] = 0
        can.create_image(coordonnee[0][0], coordonnee[0][1], anchor=NW, image=teteE)
    if direction == 'left':
        coordonnee[0][0] += -20
        if coordonnee[0][0] < 0:
            if murs_fatals == True:
                game_over = True
            else:
                coordonnee[0][0] = 480
        can.create_image(coordonnee[0][0], coordonnee[0][1], anchor=NW, image=teteW)
    if direction == 'up':
        coordonnee[0][1] += -20
        if coordonnee[0][1] < 0:
            if murs_fatals == True:
                game_over = True
            else:
                coordonnee[0][1] = 480
        can.create_image(coordonnee[0][0], coordonnee[0][1], anchor=NW, image=teteN)
    if direction == 'down':
        coordonnee[0][1] += 20
        if coordonnee[0][1] > 480:
            if murs_fatals == True:
                game_over = True
            else:
                coordonnee[0][1] = 0
        can.create_image(coordonnee[0][0], coordonnee[0][1], anchor=NW, image=teteS)
            
    for n in range(1,len(coordonnee)):
        if n%2 == 0: 
            can.create_image(coordonnee[n][0], coordonnee[n][1], anchor = NW, image = noeud1)
        else:
            can.create_image(coordonnee[n][0], coordonnee[n][1], anchor = NW, image = noeud2)
    #on associe un identifiant à chaque objet: pomme = 0 et poison = 1
    for p in range(len(objet)):
        if objet[p][2] == 0:  
            can.create_image(objet[p][0], objet[p][1], anchor=NW, image=pomme)
        elif objet[p][2] == 1:  
            can.create_image(objet[p][0], objet[p][1], anchor=NW, image=poison_img)

    # on verifie si la tete est en contact avec un objet
    for p in range(len(objet)):
        if coordonnee[0][0] == objet[p][0] and coordonnee[0][1] == objet[p][1]:
            if objet[p][2] == 0:  # si c'est une pomme
                pommes_mangees += 1
                objet[p][0] = randint(1, 24) * 20
                objet[p][1] = randint(1, 24) * 20
                coordonnee.append([-20, -20])
                if pommes_mangees % 2 == 0:  # toutes les 2 pommes mangées, un nouveau poison apparait
                    objet.append([randint(1, 24) * 20, randint(1, 24) * 20, 1])
            elif objet[p][2] == 1:  # si c'est un poison
                murs_fatals = True
                controles_inverses = True
                objet[:] = [o for o in objet if o[2] != 1]  
                tk.after(5000, reset_effets)  # les effets du poison durent 5 secondes 
    
    #on regarde si le serpent se mord la queue, si oui game over= True, on va définir le game over juste après
    for n in range(1,len(coordonnee)): # L'indice 0 est exclu, c'est la tête
        if coordonnee[0][0] == coordonnee [n][0] and coordonnee[0][1] == coordonnee [n][1]:
            game_over = True
    #on définit le game over
    if game_over : 
        TEXTE = "GAME OVER"
        normal_font = tkfont.Font(family="Helvetica", size=12, weight="bold")
        can.create_text(100,200,text = TEXTE, fill='red',  font=normal_font)
    else:
        #on définit le 'rythme' du jeu (1 frame = 100ms) et donc on rafraîchit la posision du joueur toutes les 100ms si game over =false
        tk.after(100, lambda:computeNextFrame(numFrame,coordonnee, objet))
            
        

    #on recrée la toile
if __name__ == "__main__":
    can = Canvas(tk, width=500, height=500, bg='black')
#on affiche la toile
    can.pack()

#on définit la position et la direction initiale du joueur
    direction = 'up'
    coordonnee = [ [200, 200], [200, 220], [200, 240], [220, 240] ]
    objet = []
#rend la position de la pomme aléatoire
    x = randint(1,24)
    y = randint(1,24)
    objet.append([x*20, y*20, 0])
    
    computeNextFrame(0,coordonnee, objet)

#on associe chaque directon à une touche, autrement dit on définit les controles
    if controles_inverses==False:
        tk.bind('<Right>', right) 
        tk.bind('<Left>', left) 
        tk.bind('<Down>', down) 
        tk.bind('<Up>', up)
    else:
        tk.bind('<Left>', right) 
        tk.bind('<Right>', left) 
        tk.bind('<Up>', down) 
        tk.bind('<Down>', up)
    tk.mainloop()














