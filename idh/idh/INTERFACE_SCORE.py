import tkinter as tk
from tkinter import ttk
import tkinter.font as font
from tkinter import Canvas
import time
from tkVideoPlayer import TkinterVideo
import rclpy
from rclpy.node import Node
from interfaces.msg import Lid
# VARIBALES GLOBAL
is_blue_clicked = False
is_green_clicked = False

# -------------- DIFFERENTS INTERFACE -------------- #
# INTERFACE CHOIX DU COTE
def show_choix_interface():
    
    # Supprime les élement de l'ancienne interface (face principale)
    logo_RIR_label.place_forget()
    presente_label.place_forget()
    cherry_label.place_forget()
    next_button_intro.place_forget()
    cherry_image_right_label.place_forget()
    cherry_image_left_label.place_forget()
    
    # Variable Globale
    global blue_canvas
    global green_canvas
    global choice_text_label
    global choice_text_label_2
    global  blue_button
    global  green_button
    global  next_button_choice
    global  return_button_choice
    global blue_rectangle
    global green_rectangle
    
    # Modifie la taille des boutons
    style.configure("RoundedButton.TButton", borderwidth=0, relief="flat", background=window.cget("background"), foreground="black", font=custom_font,  padding=(0.2, 2))
    
    # Crée un Canvas pour dessiner le rectangle bleu
    blue_canvas = Canvas(window, width=70, height=screen_height, bg="#ACC8E6")
    blue_canvas.place(relx=0.999, rely=0.5, anchor="e")

    # Dessine le rectangle bleu
    blue_rectangle = blue_canvas.create_rectangle(0, 0, 100, screen_height, fill="#024F78", outline="")
    
    # Crée un Canvas pour dessiner le rectangle vert
    green_canvas = Canvas(window, width=70, height=screen_height, bg="#ACC8E6")
    green_canvas.place(relx=0.155, rely=0.5, anchor="e")

    # Dessine le rectangle vert
    green_rectangle = green_canvas.create_rectangle(0, 0, 100, screen_height, fill="#015F35", outline="")

    # Affiche les éléments de la nouvelle face
    
    # Label pour le texte "Veuillez Choisir"
    choice_text_label = tk.Label(window, text="Veuillez choisir", font=custom_font, bg=window.cget("background"))
    choice_text_label.place(relx=0.5, rely=0.1, anchor="center")
    
    # Label pour le texte "Votre côté"
    choice_text_label_2 = tk.Label(window, text="Votre côté", font=custom_font, bg=window.cget("background"))
    choice_text_label_2.place(relx=0.5, rely=0.2, anchor="center")
    
    # Boutton Bleu
    blue_button = ttk.Button(window, text="Bleu", style="RoundedButton.TButton", command=Blue_Click)
    blue_button.place(relx=0.5, rely=0.35, anchor="center")

    #Boutton Vert
    green_button = ttk.Button(window, text="Vert", style="RoundedButton.TButton", command=Green_Click)
    green_button.place(relx=0.5, rely=0.5, anchor="center")
    
    # Boutton Suivant
    next_button_choice = ttk.Button(window, text="Suivant", style="RoundedButton.TButton", command=show_enter_score_interface, state=tk.DISABLED)
    next_button_choice.place(relx=0.5, rely=0.7, anchor="center")

    # Boutton Retour
    return_button_choice = ttk.Button(window, text="Retour", style="RoundedButton.TButton", command = window.mainloop)
    return_button_choice.place(relx=0.5, rely=0.85, anchor="center")

# INTERFACE SAISIE DU SCORE
def show_enter_score_interface():
    
    # Supprime les éléments de l'ancienne face (face choix du côté)
    blue_canvas.place_forget()
    green_canvas.place_forget()
    choice_text_label.place_forget()
    choice_text_label_2.place_forget()
    blue_button.place_forget()
    green_button.place_forget()
    next_button_choice.place_forget()
    return_button_choice.place_forget()
    
    # Variable Global
    global score_label
    global score_entry
    global increase_button
    global decrease_button
    global submit_button
    global return_button_score
    
    # Changer la taille des boutons increase_button et decrease_button
    style.configure("SmallButton.TButton", borderwidth=0, relief="flat", background=window.cget("background"), foreground="black", font=(custom_font['family'], 14), padding=(2, 7))
    
    # Affiche les éléments de la nouvelle face
    # Label "Saisissez le score"
    score_label = tk.Label(window, text="Saisissez le score :", font=custom_font,bg=window.cget("background"),fg="white")
    score_label.place(relx=0.5, rely=0.1, anchor="center")
    
    # Cadre pour entrer le score
    score_entry = ttk.Entry(window,font=custom_font)
    score_entry.place(relx=0.5, rely=0.3, anchor="center")
    score_entry.insert(0, "0")
    
    # Boutton Plus
    increase_button = ttk.Button(window, text="↑", style="SmallButton.TButton",command=increase_score)
    increase_button.place(relx=0.32, rely=0.5, anchor="center")
    
    # Boutton Moins
    decrease_button = ttk.Button(window, text="↓", style="SmallButton.TButton", command=decrease_score)
    decrease_button.place(relx=0.67, rely=0.5, anchor="center")
    
    # Boutton Lancé
    submit_button = ttk.Button(window, text="Lancé", style="RoundedButton.TButton", command=display_score)
    submit_button.place(relx=0.5, rely=0.7, anchor="center")
    
    # Boutton Retour
    return_button_score = ttk.Button(window, text="Retour", style="RoundedButton.TButton",command=return_to_choice)
    return_button_score.place(relx=0.5, rely=0.85, anchor="center")

# INTERFACE AFFICHAGE SCORE       
def display_score():
    
    # Supprime les éléments de l'ancienne face (face saisir le score)
    score_label.place_forget() 
    score_entry.place_forget()
    increase_button.place_forget() 
    decrease_button.place_forget()  
    submit_button.place_forget()  
    return_button_score.place_forget() 
    
    # Variable Global
    global score_show_label
    global return_button_score_affiche
    
    # Test pour savoir si le score entrer est supérieur à 0
    score = int(score_entry.get())
    if score >= 0:
        # Afficher le score dans une étiquette dans l'interface principale
        score_show_label = tk.Label(window, text="Score Saisi: {}".format(score), font=(custom_font['family'], 35),bg=window.cget("background"),fg="white")
        score_show_label.place(relx=0.5, rely=0.35, anchor="center")
    else:
        # Afficher une erreur de score négatif
        print("Erreur: Le score doit être positif")

    # Bouton Retour
    return_button_score_affiche = ttk.Button(window, text="Retour", style="RoundedButton.TButton", command=return_to_enter_score_interface)
    return_button_score_affiche.place(relx=0.5, rely=0.55, anchor="center")
    
    window.update()  # Mettre à jour la fenêtre pour afficher immédiatement le score
    
    time.sleep(95)  # Attendre 95 secondes avant de lancer video de Rick Roll
    
    Rick_Roll()    
  
#-------- DEFINITION DES FONCTION POUR LES DIFFERENTS BOUTON ET AUTRE INTERFACE--------#

# Bouton Suivant "Main Face" avec coins arrondis
def next_button_click_interface_1():
    show_choix_interface() # On passe à l'interface choix
    
#-------- INTERFACE CHOIX DU CÔTE --------#    
# Boutton Bleu 
def Blue_Click(): # Si bouton blue cliqué
    
    # On change la couleur de fond
    global current_background_color
    current_background_color = "#024F78"
    window.configure(background=current_background_color)
    
    # Configuration des bouttons
    style.configure("RoundedButton.TButton", borderwidth=0, relief="flat", background=window.cget("background"), foreground="black", font=custom_font,  padding=(0.2, 2)) 
    
    global is_green_clicked
    global is_blue_clicked
    is_blue_clicked = True
    global couleur_choisie
    couleur_choisie = "B" # Si le bouton blue est cliqué la varible couleur choisis prend la valeur "B"
    idh_node.callback('Bleu')
    is_green_clicked = False
    next_button_choice.config(state=tk.NORMAL) # Le bouton "SUIVANT" devient accessible
    
    green_canvas.itemconfigure(green_rectangle,fill="#024F78") # le rectangle vert devient bleu
    blue_canvas.itemconfigure(blue_rectangle,fill="#024F78") # le rectangle blue reste blue
    
    # On change le fond des texte et leur couleur de police
    choice_text_label.configure(bg="#024F78")
    choice_text_label_2.configure(bg="#024F78")
    choice_text_label.configure(fg="white")
    choice_text_label_2.configure(fg="white")
    
    print (couleur_choisie)
    
# Boutton Vert
def Green_Click(): # Si bouton vert cliqué
    
    # On change la couleur de fond
    global current_background_color
    current_background_color = "#015F35"
    window.configure(background=current_background_color)
    
    # Configuration des bouttons
    style.configure("RoundedButton.TButton", borderwidth=0, relief="flat", background=window.cget("background"), foreground="black", font=custom_font,  padding=(0.2, 2))
    
    global is_green_clicked
    global is_blue_clicked
    is_blue_clicked = False
    
    is_green_clicked = True
    global couleur_choisie
    couleur_choisie = "V" # Si le bouton vert est cliqué la varible couleur choisis prend la valeur "V"
    idh_node.callback('Vert')
    next_button_choice.configure(state=tk.NORMAL)
    
    blue_canvas.itemconfigure(blue_rectangle,fill="#015F35") # le rectangle bleu devient vert
    green_canvas.itemconfigure(green_rectangle,fill="#015F35") # le rectangle vert devient  vert
    
    # On change le fond des texte et leur couleur de police
    choice_text_label.configure(bg="#015F35")
    choice_text_label_2.configure(bg="#015F35")
    choice_text_label.configure(fg="white")
    choice_text_label_2.configure(fg="white")
    
#-------- INTERFACE SAISIR SCORE --------#
# Bouton plus    
def increase_score(): 
    current_score = int(score_entry.get())
    new_score = current_score + 1
    score_entry.delete(0, tk.END)
    score_entry.insert(0, str(new_score))

# Bouton moins
def decrease_score():
    current_score = int(score_entry.get())
    if current_score > 0:
        new_score = current_score - 1
        score_entry.delete(0, tk.END)
        score_entry.insert(0, str(new_score))

# Bouton Retour 
def return_to_choice():
    show_choix_interface()
    score_label.place_forget() 
    score_entry.place_forget()
    increase_button.place_forget() 
    decrease_button.place_forget()  
    submit_button.place_forget()  
    return_button_score.place_forget() 
    
    window.configure(background="#ACC8E6")
    style.configure("RoundedButton.TButton", borderwidth=0, relief="flat", background=window.cget("background"), foreground="black", font=custom_font,  padding=(0.2, 2))
    
    choice_text_label.configure(bg="#ACC8E6",fg="black")
    choice_text_label_2.configure(bg="#ACC8E6",fg="black")
    
    blue_canvas.itemconfigure(blue_rectangle,fill="#024F78")
    green_canvas.itemconfigure(green_rectangle,fill="#015F35")
   
#-------- INTERFACE AFFICHAGE SCORE --------#
# Boutton retour
def return_to_enter_score_interface():
    show_enter_score_interface()
    score_show_label.place_forget() 
    return_button_score_affiche.place_forget()
    
    
#-------- INTERFACE QUI PERMET D'AFFICHER LE RICK ROLL --------#
def Rick_Roll():
    
    #Dimensions de l'écran LCD (480x320 pixels)
    screen_width = 480
    screen_height = 320
    
    #Création de la fenêtre principale
    window_rick_roll = tk.Toplevel()
    window_rick_roll.title("RICK ROLL")
    window_rick_roll.geometry(f"{screen_width}x{screen_height}")

    RickRoll = tk.PhotoImage(file="~/Documents/font/RickRoll.png")

    # Calcul des nouvelles dimensions de l'image
    image_width = RickRoll.width()
    image_height = RickRoll.height()
    print(image_width)
    print(image_height)
    max_width = screen_width - 200 # Largeur maximale de l'image (avec une marge de 100 pixels)
    max_height = screen_height - 200 # Hauteur maximale de l'image (avec une marge de 200 pixels)
    print(max_width)
    print(max_height)
    if image_width < max_width or image_height < max_height:
    # Réduction proportionnelle de la taille de l'image
        print("salut")
        scale_factor = min(max_width / image_width, max_height / image_height)
        new_width = int(image_width * scale_factor)
        new_height = int(image_height * scale_factor)
        RickRoll = RickRoll.subsample(int(image_width / new_width), int(image_height / new_height))
    #videoplayer = TkinterVideo(master=window_rick_roll, scaled=True)
    #videoplayer.load(r"~/Documents/font/rick-astly-rick-rolled.gif")
    #videoplayer.pack(expand=True, fill="both")

    #videoplayer.play() # play the video
    RickRoll_label = tk.Label(window_rick_roll, image=RickRoll,)
    RickRoll_label.place(relx=0.5, rely=0.5, anchor="center")

    window_rick_roll.after(6000, window_rick_roll.destroy)
    
    window_rick_roll.mainloop()

# ----------------------------------------------------------------------------------------------------------------------------------------------- #
# ----------------------------------------------------------------------------------------------------------------------------------------------- #  
# ----------------------------------------------------------------------------------------------------------------------------------------------- #  
# ----------------------------------------------------------------------------------------------------------------------------------------------- #  
# node

class idhPub(Node):
    def __init__(self):
        super().__init__('idh_pub')
        self.publisher_=self.create_publisher(Lid,'screen',10)
    
    def callback(self,couleur):
        msg=Lid()
        msg.etat=couleur
        self.publisher_.publish(msg)
        self.get_logger().info('pub : %s'%msg.etat)


#------------------------------ FENETRE PRINCIPALE ------------------------------ #
def main():

    rclpy.init()
    global idh_node
    idh_node=idhPub()

    # Dimensions de l'écran LCD (480x320 pixels)
    global screen_height
    global screen_width
    screen_width = 480
    screen_height = 320
    global window
    # Création de la fenêtre principale
    window = tk.Tk()
    window.title("CHEERY ON THE CAKE")
    window.geometry(f"{screen_width}x{screen_height}")

    # Ajout du fond #ACC8E6
    window.configure(background="#ACC8E6")

    # Chargement de la police personnalisée
    global custom_font
    custom_font = font.Font(family="Heavitas", size=20)
    # Chargement de l'image du logo RIR
    global logo_RIR
    logo_RIR = tk.PhotoImage(file="~/Documents/font/LOGO RIR.png")  # Chemin complet de l'image du logo RIR

    # Calcul des nouvelles dimensions de l'image
    image_width = logo_RIR.width()
    image_height = logo_RIR.height()
    max_width = screen_width - 100  # Largeur maximale de l'image (avec une marge de 100 pixels)
    max_height = screen_height - 200  # Hauteur maximale de l'image (avec une marge de 200 pixels)
    if image_width > max_width or image_height > max_height:
    # Réduction proportionnelle de la taille de l'image
        scale_factor = min(max_width / image_width, max_height / image_height)
        new_width = int(image_width * scale_factor)
        new_height = int(image_height * scale_factor)
        logo_RIR = logo_RIR.subsample(int(image_width / new_width), int(image_height / new_height))

    #Affichage de l'image du logo RIR
    global logo_RIR_label
    logo_RIR_label = tk.Label(window, image=logo_RIR, bg="#ACC8E6")
    logo_RIR_label.place(relx=0.5, rely=0.2, anchor="center")

    #Chargement du Cherry Image
    global cherry_image
    cherry_image = tk.PhotoImage(file="~/Documents/font/The Cherry.png")

    #Calcul des nouvelles dimensions du Cherry Image
    other_width = cherry_image.width()
    other_height = cherry_image.height()
    max_width = new_width - 100
    max_height = new_height - 10
    if other_width > max_width or other_height > max_height:
    # Réduction proportionnelle de la taille de l'image
        scale_factor = min(max_width / other_width, max_height / other_height)
        new_width = int(other_width * scale_factor)
        new_height = int(other_height * scale_factor)
        cherry_image = cherry_image.subsample(int(other_width / new_width), int(other_height / new_height))

    #Affichage du Cherry Image
    global cherry_image_right_label
    cherry_image_right_label = tk.Label(window, image=cherry_image, bg="#ACC8E6")
    cherry_image_right_label.place(relx=0.75, rely=0.12)
    global cherry_image_left_label
    cherry_image_left_label = tk.Label(window, image=cherry_image, bg="#ACC8E6")
    cherry_image_left_label.place(relx=0.04, rely=0.12)

    #Texte "Présente" avec la police personnalisée
    global presente_label
    presente_label = tk.Label(window, text="Présente", font=custom_font, bg="#ACC8E6")
    presente_label.place(relx=0.5, rely=0.5, anchor="center")

    #Texte "Cherry on the cake" avec la police personnalisée
    global cherry_label
    cherry_label = tk.Label(window, text="The Cherry on the Cake", font=custom_font, bg="#ACC8E6")
    cherry_label.place(relx=0.5, rely=0.6, anchor="center")
    global next_button_intro
    next_button_intro = ttk.Button(window, text="Suivant", style="RoundedButton.TButton", command=next_button_click_interface_1)

    #Configuration du style du bouton
    global style
    style = ttk.Style()
    style.configure("RoundedButton.TButton", borderwidth=0, relief="flat", background=window.cget("background"), foreground="black", font=custom_font, padding=10)
    style.map("RoundedButton.TButton", background=[("active", "#4CAF50")])
    next_button_intro.place(relx=0.5, rely=0.8, anchor="center")

    #Exécution de la boucle principale
    window.mainloop()
    rclpy.spin(idh_node)
    idh_node.destroy_node()
    rclpy.shutdown()

if __name__=='__main__':
    main()
