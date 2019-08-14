#!/usr/bin/env python3
# coding: utf8
###SETUP###
 
#IMPORTING
import os, sys
with open(os.devnull, 'w') as f:
    oldstdout = sys.stdout
    sys.stdout = f
    import pygame
    import pygame.freetype
    sys.stdout = oldstdout
import tkinter as tk
import tkinter.ttk

#PYGAME INITIALISATION
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)
GAME_FONT = pygame.freetype.Font("assets/cutepunk_regular.ttf", 50)
height = pygame.display.Info().current_h
width = int((height/0.625))
#SCREEN SETUP
time_max_before_losing = 3600*1000#3600*1000 miliseconds = 3600 seconds = 60 minutes = 1 hour
time_before_ask_indice2 = 900*1000#900*1000 miliseconds = 900 seconds = 15 minutes
last_no_repeat = 0
indicate_click = 0
height = int((width*0.625))
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Belzee")

 #LOADING ASSETS
tender = pygame.mixer.Sound("assets/tender.wav")
intro1_image = {"x" : 0, 
                "y" : 0, 
                "image" : pygame.image.load("assets/intro1.jpg")}
intro1_image["image"] = pygame.transform.scale(intro1_image["image"], (width,int((width*2198)/3907)))

#VARIOUS VARIABLES
answer_ask_indice2 = ""
intro_playing = True
eningma_playing = False
outro1_playing = False
outro2_playing = False
running = True
time_start_enigma = 0
time_passed_on_enigma = 0
#mouse_verbose = 0
frameRate = 30
grave_click_combo = 0
max_nbr_click_to_repeat = 3
arrow_key = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]
bg_sprites = {}
bg_sprites_names = [
    "mapp", 
    "portal", 
    "grave01",
    "grave03", 
    "grave04", 
    "grave05", 
    "grave06", 
    "grave07", 
    "grave08", 
    "grave09", 
    "grave10", 
    "grave11", 
    "grave12", 
    "grave13", 
    "grave14",
    "chapel",
    "tree",
    "grave02",
    "hangedrope", 
    "shovelwateringcan", 
    "swing"]



#BELZEE'S SPEECHES STRINGS
indice1 = ("Oh ! Tu as trouvé un portail, à ce que je vois. Et si on regarde d'un peu plus près, on apercoit les mots 'Memento Mori'. "
        "Ça veut dire 'souviens-toi que tu vas mourir' en latin. Mais ça ne s'applique qu'aux humains ! "
        "J'imagine qe tu ne connais pas le latin... C'est pourtant très utile, on l'utilise beaucoup en science, et notamment en "
        "biologie où toutes les espèces sont nommés par un couple latin : c'est la nomenclature binomiale latine, inventée par "
        "Linné et cité dans son célèbre livre 'Systema Naturae en 1735. Tu ne savais pas ?"
        "\n"
        "\n")

"""indice2 = ("Je me doutais bien que tu ne pouvais pas y arriver. Bon, écoutes bien : les éléphants ont des cornes en ivoire et les cornes de "
        "narval sont le plus souvent dextrogyres, bien qu'il arrive qu'elles soient lévrogyres, "
        "c'est-à-dire qu'elles s'enroulent vers la gauche. Tu vois ce que je veux dire ?"
        "\n"
        "\n")"""
indice2 = ("Je me doutais bien que tu ne pouvais pas y arriver. Bon, écoutes bien :  tu te rappelles de la nomenclature binomiale, inventée "
        "par Linné, n'est-ce pas ? Alors sache que le premier terme désigne le genre de l'animal tandis que le second terme évoque l'espèce à "
        "l'intérieur du genre pour identifier précisement l'animal. Prenons plusieurs exemples : le phoque barbu (Erignathus barbatus) est une espèce du genre"
        " Erignathus. Le Scleromystax (Scleromystax barbatus) est désigné dans en français vernaculaire par son seul genre. Le Bulbul des jardins (Pycnonotus "
        "barbatus), comporte plusieurs sous-espèces comme 'Pycnonotus barbatus barbatus' ou 'Pycnonotus barbatus inornatus'. Enfin,tu dois connaitre le Gypaète"
        " Barbu (Gypaetus barbatus), un oiseau de la famile des gypaètes (Gypaetus). Ce n'est pas compliqué..."
        "\n"
        "\n")

#According to binomial nomenclature, the first part of an animal’s name is its genus and the second part is its species. 

indice3 = ("Tiens, une corde de pendu ! Je les connais bien, j'étudie la thanatologie. "
        "C'est un domaine qui regroupe plusieurs sciences universitaires pour étudier la mort et ses aspetcs psychologiques, biologiques et culturels."
        " Malheureusement, c'est une science trop peu connue, comme la cryptozoologie, qui étudie les animaux fantastiques. "
        "C'est fascinant ! Ça permet de mieux connaitre des créatures comme les centaures, les phoenix, les sirènes, les dragons, les hydres, les chimères..."
        "Et ainsi de mieux les acceuillir en Enfer !"
        "\n"
        "\n")

indice4 = ("Waw, une pelle et un arrosoir ! Bravo ! C'est tellement banal, même moi en ai, vu que je jardine souvent. "
        "C'est moi qui entretient les jardins du Purgatoire. Et quand je m'ennuie en Enfer, c'est aussi moi qui tisse les tapisseries "
        "qu'on retrouve un peu partout. Qu'est-ce qu'ils feraient sans moi ? Je me suis beaucoup inspiré des tapisseries médiévales, notamment celle "
        "de Bayeux et surtout celles conservées au musée de Cluny, formant une allégorie des cinq sens. Tu vois desquelles je parle ?"
        "\n"
        "\n")

discut_swing = ("Pfou ! Tu ne penses quand même pas trouver quelque chose près d'une balancoire ? Ce serait si enfantin de ma part..."
        "\n"
        "\n")

discut_tree = ("Un arbre ? Tu n'imagines pas découvrir quoi que ce soit près d'un banal arbre !"
        "\n"
        "\n")

discut_chapel = ("Tu essaie de chercher dans la chapelle, alors qu'on ne voit qu'elle ? Je ne suis pas si naïve..."
        "\n"
        "\n")

answer_grave = ("Oh oh ! Tu as découvert mon mécanisme secret, à ce que je vois... Tu veux peut-être me donner la réponse ?"
        "\n"
        "\n")

ask_indice2 = ("Alors, tu galères ? Je peux t'aider si tu veux... Je peux te fournir un indice supplémentaire, mais tu auras 20 minutes en moins "
        "pour résoudre l'énigme. Ou je te aisse te débrouiller, mais je doutes que tu y parviennes..."
        "\n"
        "\n")

player_refuse_indice2 = ("Ah bon ? Très bien, débrouilles-toi... Mais ne viens pas pleurnicher si tu te retrouves en Enfer..."
        "\n"
        "\n")

intro_talk_pt1 = ("Belzee est une démone, soeur de Belzebuth. Elle vit aux Enfers et est d'un caractère pour le moins taquin. "
        "Elle a tout pour être heureuse, mais... elle est jalouse de son frère. Ce dernier, aussi puissant qu'elle mais plus connu, "
        "reçoit toutes les offrandes satanistes de ces satanés humains sexistes, ainsi que toutes les requêtes croustillantes. "
        "Alors Belzee s'ennuie. Et que fait une démone quand elle s'ennuie ? Elle descend sur terre, aux frontières de son royaume, "
        "pour torturer la première âme venue. Belzee est donc dans un cimetière."
        "\n"
        "\n")

intro_talk_pt2 = ("Une silhouette sombre creuse le sol. Profanation ! Le devoir de Belzee serait d'envoyer la silhouette aux Enfers. "
        "Seulement, la démone aime s'amuser : elle propose donc un marché au mystérieux profanateur : soit vous résolvez son énigme dans le temps imparti et Belzee "
        "oubliera tout, soit vous échouez et elle ne fermera pas les yeux : en un battement de paupières, vous vous retrouverez aux Enfers..."
        "\n"
        "\n")

outro1_talk = "Très bien, tu peux partir... Mais je sens qu'on se retrouvera !"

outro2_talk = "Temps écoulé. Rendez-vous en Enfer..."

popup_content = []

def populate(frame, text_to_display, row):
    tk.Label(frame, text=text_to_display, borderwidth="4", relief="raised", wraplength=500).grid(row=row, column=0)


def onFrameConfigure(canvas):
    canvas.configure(scrollregion=canvas.bbox("all"))
def createPopupThing():
    global root, canvas, frame, vsb, rmbr_button
    root = tk.Tk()
    canvas = tk.Canvas(root, borderwidth=0, background="#2EF2A2", width=550)
    frame = tk.Frame(canvas, background="#2EF2A2")
    vsb = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=vsb.set)

    vsb.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window((5,5), window=frame, anchor="nw")
    frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))

    root.wm_title("Belzee a dit")

    rmbr_button = tk.Button(frame, text="Fermer et se souvenir...", command =(root.destroy))
    rmbr_button.grid(row=11, column=0)
##########



#SPRITES SETUP      
all_sprites_list = pygame.sprite.OrderedUpdates()
mouse_holder = pygame.sprite.Group()
belzee_holder = pygame.sprite.Group()
class BgSprites(pygame.sprite.Sprite):
    def __init__(self,name):
        #CALL OF THE PARENT CLASS CONSTRCUTOR (BECAUSE THIS CLASS DERIVES FROM THE SPRITE PYGAME CLASS)
        super().__init__()
        #INITIALISING THE NAME OF THE SPRITE
        self.name = name
        #CREATING nbr_of_click ARGUMENT
        self.nbr_of_click = 0
        #LOADING ANS SCALING THE SPRITE'S PICTURE
        self.image = pygame.image.load("assets/"+self.name+".png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height)) 
        #FETCHING THE RECTANGLE OBJECT ASSOCIATED WITH THE IMAGE AND POSITIONING IT
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        #SETTING UP THE MASK OF THE SPRITE
        self.mask = pygame.mask.from_surface(self.image)
        #ADDING THE SPRITE TO THE GROUP OF ALL SPRITES
        all_sprites_list.add(self)

#CREATE ALL BG SPRITES
for x in bg_sprites_names: #FOR EACH BG SPRITE THAT'S TO CREATE
   bg_sprites[x] = BgSprites(x) #CREATE THE SPRITE OBJECT UISING THE BgSprites CLASS

#CREATE THE MOUSE SPRITE
mouse_sprite = pygame.sprite.Sprite()
mouse_sprite.image = pygame.image.load("assets/l46.png").convert_alpha()
mouse_sprite.image = pygame.transform.scale(mouse_sprite.image,(int(((width*40)/1500)), int(((width*40)/1500))))
mouse_sprite.mask = pygame.mask.from_surface(mouse_sprite.image)
mouse_sprite.rect = mouse_sprite.image.get_rect()
mouse_sprite.rect.x = 0
mouse_sprite.rect.y = 0
all_sprites_list.add(mouse_sprite)
mouse_holder.add(mouse_sprite)

#CREATE BELZEE'S PLACEHOLDER SPRITE
belzee_plhd = pygame.sprite.Sprite()
belzee_plhd.image = pygame.image.load("assets/belzee_placeholder.png").convert_alpha()
belzee_plhd.image = pygame.transform.scale(belzee_plhd.image,(int((width/10.7)),int((height/4.95))))
belzee_plhd.mask = pygame.mask.from_surface(belzee_plhd.image)
belzee_plhd.rect = belzee_plhd.image.get_rect()
belzee_plhd.rect.x = (width/2.57)
belzee_plhd.rect.y = (height/20.45)
all_sprites_list.add(belzee_plhd)
belzee_holder.add(belzee_plhd)


#VARIOUS FUNCTIONS
def getAnswer():
    enigma_answer = input("Donnes-moi la réponse, alors...").lower()
    if enigma_answer == "monoceros barbatus":
        outro1()
    else:
        print("Euh... non ! Réesaie !")

def askIndice2():
    print(ask_indice2)
    global answer_ask_indice2
    ask_indice2_looping = True
    while ask_indice2_looping:
        answer_ask_indice2 = input("Tu veux de l'aide, oui ou non ?"+"\n")
        if answer_ask_indice2.lower() == "oui":
            time_max_before_losing -= (1200*1000)
            print(indice2)
            ask_indice2_looping = False
        elif answer_ask_indice2.lower() == "non":
            print(player_refuse_indice2)
            ask_indice2_looping = False
        else:
            print("Quoi ?")

#INTRO/OUTRO/MAIN FUNCTIONS
def intro():
    global intro_playing
    global eningma_playing
    #INTRO CODE
    GAME_FONT.render_to(screen, (900, 100), intro_talk_pt1, (251, 242, 252))
    print(intro_talk_pt1)
    print(intro_talk_pt2)
    print("COMMENT JOUER : Explorez l'image et interrogez Belzee pour qu'elle vous en dise plus..."+"\n")
    input("Entrée pour continuer..."+"\n"+"\n")
    #END INTRO CODE
    intro_playing = False
    eningma_playing = True
    time_start_enigma = pygame.time.get_ticks()
    tender.play(-1)

def outro1():
    eningma_playing = False
    outro1_playing = True
    print(outro1_talk+"\n")
    input("Entrée pour quitter")
    sys.exit()

def outro2():
    print(outro2_talk)
    input("Enter to quit")
    sys.exit()

#MOUSE/SPRITE COLLISION FUNCTIONS
def mouseMappCollision():
    print("mapp")

def mouseGrave01Collision():
    #print("grave01")
    global grave_click_combo
    grave_click_combo += 1

def mouseGrave02Collision():
    #print("grave02")
    global grave_click_combo
    grave_click_combo += 1

def mouseGrave03Collision():
    #print("grave03")
    global grave_click_combo
    grave_click_combo += 1

def mouseGrave04Collision():
    #print("grave04")
    global grave_click_combo
    grave_click_combo += 1

def mouseGrave05Collision():
    #print("grave05")
    global grave_click_combo
    grave_click_combo += 1

def mouseGrave06Collision():
    #print("grave06")
    global grave_click_combo
    grave_click_combo += 1

def mouseGrave07Collision():
    #print("grave07")
    global grave_click_combo
    grave_click_combo += 1

def mouseGrave08Collision():
    #print("grave08")
    global grave_click_combo
    grave_click_combo += 1

def mouseGrave09Collision():
    #print("grave09")
    global grave_click_combo
    grave_click_combo += 1

def mouseGrave10Collision():
    #print("grave10")
    global grave_click_combo
    grave_click_combo += 1

def mouseGrave11Collision():
    #print("grave11")
    global grave_click_combo
    grave_click_combo += 1

def mouseGrave12Collision():
    #print("grave12") 
    global grave_click_combo
    grave_click_combo += 1

def mouseGrave13Collision():
    #print("grave13")
    global grave_click_combo
    grave_click_combo += 1

def mouseGrave14Collision():
    #print("grave14")
    global grave_click_combo
    grave_click_combo += 1

def mousePortalCollision():
    global last_no_repeat, grave_click_combo, indicate_click
    bg_sprites["portal"].nbr_of_click += 1
    if bg_sprites["portal"].nbr_of_click<= max_nbr_click_to_repeat:
        popup_content.append(indice1)
        indicate_click = pygame.time.get_ticks()
    else:
        last_no_repeat = pygame.time.get_ticks()
    #print("portal")
    grave_click_combo = 0

def mouseChapelCollision():
    global last_no_repeat, grave_click_combo, indicate_click
    bg_sprites["chapel"].nbr_of_click += 1
    if bg_sprites["chapel"].nbr_of_click<= max_nbr_click_to_repeat:
        popup_content.append(discut_chapel)
        indicate_click = pygame.time.get_ticks()
    else:
        last_no_repeat = pygame.time.get_ticks()
    #print("chapel")
    grave_click_combo = 0

def mouseHangedropeCollision():
    global last_no_repeat, grave_click_combo, indicate_click
    bg_sprites["hangedrope"].nbr_of_click += 1
    if bg_sprites["hangedrope"].nbr_of_click<= max_nbr_click_to_repeat:
        popup_content.append(indice3)
        indicate_click = pygame.time.get_ticks()
    else:
        last_no_repeat = pygame.time.get_ticks()
    #print("hangedrope")
    grave_click_combo = 0

def mouseShovelwateringcanCollision():
    global last_no_repeat, grave_click_combo, indicate_click
    bg_sprites["shovelwateringcan"].nbr_of_click += 1
    if bg_sprites["shovelwateringcan"].nbr_of_click<= max_nbr_click_to_repeat:
        popup_content.append(indice4)
        indicate_click = pygame.time.get_ticks()
    else:
        last_no_repeat = pygame.time.get_ticks()
    ##print("shovelwateringcan")
    grave_click_combo = 0

def mouseSwingCollision():
    global last_no_repeat, grave_click_combo, indicate_click
    bg_sprites["swing"].nbr_of_click += 1
    if bg_sprites["swing"].nbr_of_click<= max_nbr_click_to_repeat:
        popup_content.append(discut_swing)
        indicate_click = pygame.time.get_ticks()
    else:
        last_no_repeat = pygame.time.get_ticks()
    #print("swing")
    grave_click_combo = 0

def mouseTreeCollision(): 
    global last_no_repeat, grave_click_combo, indicate_click
    bg_sprites["tree"].nbr_of_click += 1
    if bg_sprites["tree"].nbr_of_click<= max_nbr_click_to_repeat:
        popup_content.append(discut_tree)
        indicate_click = pygame.time.get_ticks()
    else:
        last_no_repeat = pygame.time.get_ticks()
    #print("tree")
    grave_click_combo = 0

#ALL LETTER PRESSED FUNCTIONS
def apressed():
    #print("a pressed")
    pass

def bpressed():
    #print("b pressed")
    pass

def cpressed():
    #print("c pressed")
    pass

def dpressed():
    #print("d pressed")
    pass

def epressed():
    #print("e pressed")
    pass

def fpressed():
    #print("f pressed")
    pass

def gpressed():
    #print("g pressed")
    pass

def hpressed():
    #print("h pressed")
    pass

def ipressed():
    #print("j pressed")
    pass

def jpressed():
    #print("j pressed")
    pass

def kpressed():
    #print("k pressed")
    pass

def lpressed():
    #print("l pressed")
    pass

def mpressed():
    #print("m pressed")
    pass

def npressed():
    #print("n pressed")
    pass

def opressed():
    #print("o pressed")
    pass

def ppressed():
    #print("p pressed")
    pass

def qpressed(): #QUITTNG FUNCTION
    #print("q pressed")
    """want_to_quit = input("Exiting system... Enter to confirm, c to cancel")
    if want_to_quit == "c":
        print("Cancelling system exit...")
        print("Done !")
    else:"""        
    sys.exit()

def rpressed():
    #print("r pressed")
    pass

def spressed():
    #print("s pressed")
    pass

def tpressed():
    #print("t pressed")
    pass

def upressed():
    #print("u pressed")
    pass

def vpressed(): #MOUSE VERBOSE
    #print("v pressed")
    """global mouse_verbose
    if mouse_verbose:
        mouse_verbose = False
        print("Mouse movements verbose is now off !")
    elif not mouse_verbose:
        print("Mouse movements verbose is now on !")
        mouse_verbose = True"""
    pass

def wpressed():
    #print("w pressed")
    pass

def xpressed():
    #print("x pressed")
    pass

def ypressed():
    #print("y pressed")
    pass

def zpressed():
    #print("z pressed")
    pass

#SWITCHERS
key_switcher = { 
    pygame.K_a : apressed,
    pygame.K_b : bpressed, 
    pygame.K_c : cpressed,
    pygame.K_d : dpressed,
    pygame.K_e : epressed, 
    pygame.K_f : fpressed,
    pygame.K_g : gpressed, 
    pygame.K_h : hpressed,
    pygame.K_i : ipressed, 
    pygame.K_j : jpressed,
    pygame.K_k : kpressed, 
    pygame.K_l : lpressed,
    pygame.K_m : mpressed, 
    pygame.K_n : npressed,
    pygame.K_o : opressed, 
    pygame.K_p : ppressed,
    pygame.K_q : qpressed, 
    pygame.K_r : rpressed,
    pygame.K_s : spressed,
    pygame.K_t : tpressed,
    pygame.K_u : upressed,
    pygame.K_v : vpressed, 
    pygame.K_w : wpressed,
    pygame.K_x : xpressed,
    pygame.K_y : ypressed, 
    pygame.K_z : zpressed}

bg_switcher = { 
    "mapp" : mouseMappCollision,
    "grave01" : mouseGrave01Collision,
    "grave02" : mouseGrave02Collision, 
    "grave03" : mouseGrave03Collision,
    "grave04" : mouseGrave04Collision, 
    "grave05" : mouseGrave05Collision,
    "grave06" : mouseGrave06Collision, 
    "grave07" : mouseGrave07Collision,
    "grave08" : mouseGrave08Collision, 
    "grave09" : mouseGrave09Collision,
    "grave10" : mouseGrave10Collision, 
    "grave11" : mouseGrave11Collision,
    "grave12" : mouseGrave12Collision,
    "grave13" : mouseGrave13Collision,
    "grave14" : mouseGrave14Collision,
    "portal" : mousePortalCollision, 
    "chapel" : mouseChapelCollision, 
    "hangedrope" : mouseHangedropeCollision,
    "shovelwateringcan" : mouseShovelwateringcanCollision, 
    "swing" : mouseSwingCollision,
    "tree" : mouseTreeCollision}

###END SETUP###
    
#MAIN LOOP
while running:
    clock.tick(frameRate)
    time_passed_on_enigma = pygame.time.get_ticks() - time_start_enigma
    if time_passed_on_enigma > time_before_ask_indice2 and answer_ask_indice2 == "":
        askIndice2()
    elif time_passed_on_enigma > time_max_before_losing:
        print("Temps écoulé ! Perdu !...")
        outro2_playing = True
    if intro_playing:
        intro()
    elif outro2_playing:
        outro2()
    #EVENT CHECKER
    for e in pygame.event.get():
        #RED CROSS IS PRESSED ?
        if e.type == pygame.QUIT:
            sys.exit() #EXIT WINDOW
        #KEYBOARD EVENTS    
        elif e.type == pygame.KEYDOWN:
            #ARROW KEY IS PRESSED ?
            if e.key in arrow_key:
                if e.key == pygame.K_UP:
                    pass
                    #print("Key up pressed")
                elif e.key == pygame.K_DOWN:
                    pass
                    #print("Key down pressed")
                elif e.key == pygame.K_LEFT:
                    pass
                    #print("Key left pressed")
                elif e.key == pygame.K_RIGHT:
                    pass
                    #print("Key right pressed")
            #LETTER KEY IS PRESSED ?
            elif e.key in key_switcher:
                key_switcher[e.key]() #SEE DEFINED FUNCTIONS
        #MOUSE MOVED EVENTS
        elif e.type == pygame.MOUSEMOTION:
            #UPDATE MOUSE'S POSITION
            mouse_sprite.rect.x = e.pos[0]
            mouse_sprite.rect.y = e.pos[1]
            """if mouse_verbose: #MOUSE VERBOSE
                print("Mouse moved at x:"+str(e.pos[0])+" and y:"+str(e.pos[1]))
                print("Mouse moved "+str(e.rel[0])+" px x and "+str(e.rel[1])+" px y")"""
        #MOUSE BUTTONS PRESSED EVENTS
        elif e.type == pygame.MOUSEBUTTONDOWN:
            if e.button== 1:
                a=1#print("Mouse left button pressed")
            elif e.button == 2:
                a=1#print("Mouse center button pressed")
            elif e.button == 3:
                a=1#print("Mouse right button pressed")
        #MOUSE BUTTONS RELEASED EVENTS
        elif e.type == pygame.MOUSEBUTTONUP:
            if e.button== 1:
                a=1#print("Mouse left button released")
            elif e.button == 2:
                a=1#print("Mouse center button released")
            elif e.button == 3:
                a=1#print("Mouse right button released")
            if eningma_playing:
                #CHECK FOR COLLISION BETWEEN ANY OF BgSprites'S MASK AND THE MOUSE'S MASK
                if pygame.sprite.collide_mask(mouse_sprite, belzee_plhd):
                    createPopupThing() 
                    """for row in range(10):
                        populate(frame, str(row), row)"""
                    for x in range(len(popup_content)):
                        populate(frame, popup_content[x], x)
                    root.mainloop()

                for x in bg_sprites: #FOR EACH BG SPRITE THAT'S TO CREATE
                    if pygame.sprite.collide_mask(mouse_sprite, bg_sprites[x]) != None and x!= "mapp":
                        bg_switcher[x]()
                        if grave_click_combo == 14:
                            print(answer_grave)
                            keep_asking_for_answer = True
                            while grave_click_combo == 14:
                                confirm_enter_answer = input("Oui ou non?")
                                if confirm_enter_answer.lower() == "oui":
                                    getAnswer()
                                    grave_click_combo = 0
                                elif confirm_enter_answer.lower() == "non":
                                    print("Continue à chercher, alors...")
                                    grave_click_combo = 0
                                else:
                                    print("Quoi ?")
                        #print("Collision with "+x+str(pygame.sprite.collide_mask(mouse_sprite,bg_sprites[x])))
    #END OF EVENTS CHECKER

    #OTHER CODE FROM HERE
    #TO HERE
    #FINALLY, DISPLAY EVERYTHING
    if intro_playing:
        #Code intro
        screen.blit(intro1_image["image"], (intro1_image["x"], intro1_image["y"]))
        pass
    elif eningma_playing:
        all_sprites_list.draw(screen)
    else:
        pass
    #HERE GOES DRAWING CODE (ON TOP OF bgSprites BUT UNDER THE MOUSE AND BELZEE, UPDATE EACH FRAME)
    if (last_no_repeat + 3000) > pygame.time.get_ticks() and last_no_repeat != 0:
        GAME_FONT.render_to(screen, (900, 100), "Je ne vais pas", (251, 242, 252))
        GAME_FONT.render_to(screen, (900, 145), "me répéter !", (251, 242, 252))
    else:
        pass
    if (indicate_click + 700) > pygame.time.get_ticks() and indicate_click != 0:
        GAME_FONT.render_to(screen, (900, 100), "!", (251, 242, 252))
    else:
        pass
    #THEN DRAW MOUSE AND BELZEE ON TOP OF EVERYTHING
    belzee_holder.draw(screen)
    mouse_holder.draw(screen)#DRAWN MOUSE APART TO MAKE SURE ITHE MOUSE IS ALWAYS ON TOP
    pygame.display.flip()
    #WITH A 10 MS DELAY
    pygame.time.delay(10)