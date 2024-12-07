from threading import Thread

from json import loads,dumps

from PIL import ImageTk
from tkinter import ttk, Scrollbar, filedialog, messagebox
import tkcalendar
from os import startfile
from logique import *
from time import strftime
from customtkinter import *
bg = "#CAD0B1"

x=0
bg_color="#A4B4C4"

root = CTk("#2b3e50")
font1 = "Bookman Old Style"
#set_appearance_mode("dark")
set_default_color_theme("green")

root.geometry("1330x650+10+5")

root.iconbitmap("logo.ico")
root.title("Logiciel de gestion de dévis")

colonnes_materiel_table = ["Références", "Unité", "Quantité", "Prix Unitaire", "Montant Total"]
list_width_mat_table = [100, 100, 220, 260]
list_colonnes = ["reference", "unite", "qte", "prix_unitaire", "montant_ht"]
facture_table_colonnes = ["Client", "N°Facture", "Date", "Matériels", "Main d'œuvre",
                          "Total", "Reste"]
list_anchor_coloums = ["nw", "n", "n", "center", "center", "center", "center"]
list_colonnes_width = [200, 160, 110, 130, 150, 160, 150]
consulter_facture_colonnes = ["client_name", "facture_number", "Date",
                              "Montant_achat_materiels", "Montant_Main_oeuvre", "Montant_Total", "Reste"]

colonne_bilan = ["Client", "N°Facture", "Date", "Materiel", "Main d'œuvre", "Reste", "Total"]
window = CTkFrame(root, width=1200,height=650,)
window.place(relx=0.138, rely=0.001)
list_string_var=[StringVar() for _ in range(9)]
#list Frames



def retour_resume_last_part():
    show_widget(frame_remplissage_last_part)
class Resume(CTkFrame):
    def __init__(self, master, nom_client, numero_client, adresse_client, nom_facture,
     date,items,total_achat, main_oeuvre,
    main_oeuvre_descript,   total, avance, reste, **kwargs):
        super().__init__(master, **kwargs)
        self.avance=avance
        self.nom_client=nom_client
        self.adresse=adresse_client
        self.numero_client=numero_client
        self.reste=reste
        self.total=total
        self.items=json.loads(items)
        self.total_achat=total_achat
        self.main_oeuvre=main_oeuvre
        self.main_oeuvre_descript=main_oeuvre_descript
        self.date=date
        self.nom_facture=nom_facture
        self.configure(width=1200, height=650)
        self.place(relx=0.001, rely=0.001)

    def show_window(self):
        frame_resume_facture=CTkFrame(self,width=1200,height=750,)
        frame_resume_facture.place(relx=0.001,rely=0.001)
        frame1=CTkFrame(frame_resume_facture,width=1100,height=220)
        frame1.place(relx=0.001,rely=0.07)

        label_date_resume=CTkLabel(frame1,text="Date : "+self.date,font=(font1,23))
        label_date_resume.place(relx=0.05,rely=0.82)
        label_nom_client=CTkLabel(frame1,text="Nom: "+self.nom_client,font=(font1,23))
        label_nom_client.place(relx=0.05,rely=0.04)
        label_client_num=CTkLabel(frame1,text="Tel: "+self.numero_client,font=(font1,23))
        label_client_num.place(relx=0.05,rely=0.22)
        label_client_address=CTkLabel(frame1,text="Adresse :"+self.adresse,font=(font1,23))
        label_client_address.place(relx=0.05,rely=0.4)
        label_nom_facture=CTkLabel(frame1,text=self.nom_facture,font=(font1,23))
        label_nom_facture.place(relx=0.05,rely=0.52)

        label_achat_materiel=CTkLabel(frame1,text="Total achat Matériel: "+set_espace_between_3_numbers(self.total_achat),font=(font1,23))
        label_achat_materiel.place(relx=0.66,rely=0.05)

        label_main_oeuvre=CTkLabel(frame1,text="Main d'œuvre: "+set_espace_between_3_numbers(self.main_oeuvre),font=(font1,23))
        label_main_oeuvre.place(relx=0.66,rely=0.22)

        label_main_oeuvre_des=CTkLabel(frame1,text=self.main_oeuvre_descript,font=(font1,23))
        label_main_oeuvre_des.place(relx=0.05,rely=0.69)

        label_avance_resume=CTkLabel(frame1,text="Avance : "+set_espace_between_3_numbers(self.avance),font=(font1,23))
        label_avance_resume.place(relx=0.66,rely=0.39)

        label_reste_resume=CTkLabel(frame1,text="Reste : "+set_espace_between_3_numbers(self.reste),font=(font1,23))
        label_reste_resume.place(relx=0.66,rely=0.59)

        label_total_resume=CTkLabel(frame1,text="Total : "+set_espace_between_3_numbers(self.total),font=(font1,23,"bold"))
        label_total_resume.place(relx=0.66,rely=0.75)

        CTkLabel(frame_resume_facture, text="Résumé de la Facture"
        , font=(font1, 28, "bold", "italic"), fg_color="#2CC985").place(relx=0.3, rely=0.01)

        button_enregistrer_facture = CTkButton(frame_resume_facture, corner_radius=20, text="Enregistrer Facture",
        font=("Bookman Old Style", 23), height=45,command=test1, width=150, )
        button_enregistrer_facture.place(relx=0.5, rely=0.7)
        button_retour_resume = CTkButton(frame_resume_facture, corner_radius=20, text="Retour",
        font=("Bookman Old Style", 23), height=45, width=150,command=retour_resume_last_part )
        button_retour_resume.place(relx=0.1, rely=0.7)

        

        """"for index,value in enumerate(self.items):

            value=list(value.values())

            j=CTkFrame(scroollable_frame,border_color="green",width=1000,height=150,border_width=2)
            j.pack(pady=15)
            CTkLabel(j, text="Matériel: "+str(index+1), font=(font1, 22,"bold")).place(relx=0.4, rely=0.01)

            CTkLabel(j,text="Référence: "+str(value[0]),font=(font1,20)).place(relx=0.01,rely=0.3)
            CTkLabel(j, text="Unité: "+str(value[1]), font=(font1, 22)).place(relx=0.82, rely=0.3)
            CTkLabel(j, text="Quantité: "+str(value[2]), font=(font1, 20)).place(relx=0.01, rely=0.7)
            CTkLabel(j, text="Prix_unitaire: "+str(value[3]), font=(font1, 20)).place(relx=0.3, rely=0.7)
            CTkLabel(j, text="Prix Total: "+str(value[4]), font=(font1, 20)).place(relx=0.7, rely=0.7)
"""
        frame_resume_treeview = CTkFrame(frame_resume_facture, width=1100, height=240)
        frame_resume_treeview.place(relx=0.001, rely=0.37)

        table_resume = ttk.Treeview(frame_resume_treeview, columns=colonnes_materiel_table, show="headings", height=7)
        scrollbar = Scrollbar(frame_resume_treeview, orient="vertical", command=table_resume.yview)
        #table_resume.bind("<<TreeviewSelect>>", get_selected_element)
        for i,col in enumerate(colonnes_materiel_table):

            table_resume.heading(column=col,text=col,)
        for ind,value in enumerate(self.items):
            tag = "evenrow" if ind % 2 == 0 else "oddrow"
            table_resume.insert("", index=0,tags=(tag,), values=list(value.values()), )
        for ind,colonne in enumerate(colonnes_materiel_table):
            list_width=[400,100,100,250,200]
            list_anchor_coloums = ["nw", "center", "center", "center", "center", ]
            table_resume.column(column=colonne,width=list_width[ind],anchor=list_anchor_coloums[ind])
        table_resume.tag_configure("oddrow", background="lightblue")
        table_resume.tag_configure("evenrow", background="white")

        scrollbar.pack(fill="y", side="right")

        table_resume.pack(fill="both")
        table_resume.configure(yscrollcommand=scrollbar.set)
        
        


frame_client_info = CTkFrame(window, width=1130+x,fg_color=bg_color,height=580, border_width=2)
frame_resume_facture = CTkFrame(window, width=1100+x, height=650, border_width=2)

frame_menu_principale = CTkFrame(window, width=1200+x,fg_color="#A4B4C4", height=650)
frame_reste_payer = CTkFrame(window, width=1100+x, height=550, border_width=2)
frame_reste_payer.place(relx=0, rely=0.1)
frame_modifier_reste = CTkFrame(frame_reste_payer,fg_color=bg_color, width=700, height=430, border_width=1)
frame_modifier_reste.place(relx=0.154, rely=0.1)
frame_info_client = CTkFrame(frame_client_info,border_width=1,
fg_color=bg_color, width=1090+x, height=250)
frame_info_client.place(relx=0.005, rely=0.05)
frame_remplissage_materiel = CTkFrame(window, fg_color=bg_color,width=1130+x, height=600, border_width=2)
frame_remplissage = frame_remplissage_materiel
frame_faire_bilan = CTkFrame(window, width=1100+x, height=630,fg_color=bg_color,)
frame_consulter_facture = CTkFrame(window, width=1100+x,fg_color=bg_color, height=550)

frame_remplissage_last_part = CTkFrame(window, width=1130+x,fg_color=bg_color, height=600)
list_frames = [frame_remplissage_last_part, frame_client_info, frame_remplissage_materiel,
frame_faire_bilan,
frame_menu_principale,frame_consulter_facture, frame_reste_payer,frame_resume_facture]



def bouger_menu():

    for frame in list_frames:
        frame.configure(width=1100)
    if frame_menu.cget("width") == 185:
        window.place(relx=0.03, rely=0.001)
        x=100
        frame_menu.configure(width=1)
        button_menu_bar.configure(width=10,text="")
        """for frame in list_frames:
        frame.configure(width=frame.cget("width")+100)"""
    else:
        x=0
        frame_menu.configure(width=185)
        button_menu_bar.configure(width=185, text="Menu")
        window.configure(width=1200)
        window.place(relx=0.138, rely=0.001)
def thread_bouger_menu():
    thread=Thread(target=bouger_menu)
    thread.start()
def change_mode_dark_light():
    if switch_mode.get():
        set_appearance_mode("dark")
    else:
        set_appearance_mode("light")
#images
if 2+2==4:
    img_menu = CTkImage(light_image=ImageTk.Image.open("list.png"), size=(20, 30))
    img_pdf = CTkImage(light_image=ImageTk.Image.open("pdf.png"), size=(50, 50))
    img_suivant = CTkImage(light_image=ImageTk.Image.open("suivant.png"), size=(20, 30))
    img_precedent = CTkImage(light_image=ImageTk.Image.open("arrow.png"), size=(20, 30))
    image_logo = CTkImage(light_image=ImageTk.Image.open("image_logo.jpg"), size=(120, 90))
    image_faire_fact = CTkImage(light_image=ImageTk.Image.open("invoice.png"), size=(250, 250))
    image_consult_fact = CTkImage(light_image=ImageTk.Image.open("consult_fact.png"), size=(250, 250))
    image_faire_bilan = CTkImage(light_image=ImageTk.Image.open("bilan_fact.png"), size=(250, 250))

def get_save_directory():
    path = filedialog.askdirectory()
    directory_to_save_facture.configure(text=str(path))


def refresh_materiel_number():
    materiel_number=len(get_table_values())+1
    materiel_number_label.configure(text="Matériel N° "+str(materiel_number))
    root.after(100,refresh_materiel_number)

def show_frame_faire_facture():
    for item in list_facture_table.selection():
        list_facture_table.selection_remove(item)
    show_widget(frame_client_info)

def thread_show_frame_faire_facture():
    Thread(target=show_frame_faire_facture).start()

def show_frame_last_part():
    show_widget(frame_remplissage_last_part, x=0, y=0.05)
def show_frame_accueil():
    show_widget(frame_menu_principale)


def show_frame_remplissage_materiel():
    if not nom_client.get().strip() or not nom_facture.get().strip():
        client_name_pop_up=messagebox.showerror("Erreurs détectées","Veuillez entrer le nom du client et \n le nom de la facture")
    else:
        show_widget(frame_remplissage_materiel, x=0, y=0.001)

def show_widget(widget: CTkFrame, x=0.001, y=0.001):
    for frame in list_frames:
        frame.place_forget()
    widget.place(relx=x, rely=y)


def consulter_facture():
    show_widget(frame_consulter_facture)


def faire_bilan():
    show_widget(frame_faire_bilan)


def clear_all_entries():
    nom_client.delete(0, END)
    numero_client.delete(0, END)
    nom_facture.delete(0, END)
    avance_entry.delete(0, END)
    reste_payer.delete(0, END)
    montant_total_label.configure(text="")
    main_oeuvre.delete(0, END)
    main_oeuvre_descipt.delete(0, END)
    adresse_client.delete(0, END)
    numero_client.delete(0, END)
    Quantite.delete(0, END)
    prix_Total.delete(0, END)
    prix_unitaire.delete(0, END)
    Unite.delete(0, END)
    nom_materiel.delete(0, END)
    for element in table.get_children():
        table.delete(element)


def retour1():
    show_widget(frame_client_info, x=0.01, y=0.01)


def retour2():
    show_widget(frame_remplissage_materiel, x=0, y=0.001)


def retour3():
    show_widget(frame_consulter_facture)


def retour_modi_consul():
    show_widget(frame_consulter_facture)


def set_montant_total_materiel():
    quantite = Quantite.get()
    prix_unit = prix_unitaire.get()
    try:
        string_var_total.set(set_espace_between_3_numbers(str(int(quantite) * int(prix_unit))))
    except:
        pass
    frame_remplissage.after(100, set_montant_total_materiel)


def afficher_resume_facture():
    avance=avance_entry.get()
    gere_montant = gerer_montant(delete_space_3numbers(main_oeuvre.get()))
    gerer_avance = gerer_montant(delete_space_3numbers(avance))
    total = delete_space_3numbers(montant_total_label.cget("text"))
    state_avance_reste = gerer_montant_total_avance_reste(delete_space_3numbers(avance), total)
    gerer_montant_descript = gerer_montant_oeuvre_and_description(delete_space_3numbers(main_oeuvre.get()), main_oeuvre_descipt.get())
    data = get_all_datas("tableau")[1:-3]
    status_main_oeuvre=True
    if main_oeuvre.get().strip():
        status_main_oeuvre = False
        try:
            float(delete_space_3numbers(main_oeuvre.get()))
            status_main_oeuvre=True
        except:
            pass
    if state_avance_reste[0]:
        if status_main_oeuvre:
            if gerer_montant_descript:
                print(total)
                if delete_space_3numbers(total.strip()) =="0":
                    messagebox.showerror(" Status de la Facture", "vous la facture est vide \n veuillez remplissez la d'abord")
                else:
                    show_widget(frame_resume_facture)
                    resume=Resume(frame_resume_facture,*data)
                    resume.show_window()
            else:
                messagebox.showerror("Description", "Veuillez remplir la description\n dela main d'œuvre et \n Montant de la main d'œuvre")
        else:
            messagebox.showerror("Description", "Montant  de la main d'œuvre \n est invalide")
    else:
        messagebox.showerror("Erreurs détectées", state_avance_reste[1])

def valider(type="enregistrer",id_facture=""):
    data = get_all_datas("facture")
    if type=="enregistrer":
        status1 = messagebox.askyesno("Sauvegarder la facture", "Voulez-vous \n enregistrer cette facture ?")
        if status1:
            insert_facture(data)
            status = messagebox.askyesno("", "Voulez vous exporter en PDF ?")
            if status:
                get_save_directory()
                path=directory_to_save_facture.cget("text")
                facture = Facture(*data[:-3], path)
                numero_facture="Facture Proforma "+(facture.numero_facture).replace("/","_")+".pdf"
                facture.produire_facture()
                clear_all_entries()
                messagebox.showinfo("succès", "enregistré")
                status2=messagebox.askyesno("Ouverture de la Facture","Voulez-vous ouvrir la facture?")
                if status2:
                    startfile(path+"/"+numero_facture,operation="open")

    else:
        status1 = messagebox.askyesno("Sauvegarder la facture", "Confirmez-vous la \nmodification cette facture ?")
        if status1:
            update_facture_data(id_facture,data[1:])
            messagebox.showinfo("Status de la modification","Facture modifier\navec succès")


def test():
    afficher_resume_facture()

def test1():
    if get_selected_facture():
        id_facture = list_facture_table.item(get_selected_facture()[0])["values"][1]

        valider("modification", id_facture=id_facture)
    else:

        valider()


def modifier_completement_facture():
    selection=get_selected_facture()[0]
    button_valider.configure(command=test)
    id_facture=list_facture_table.item(selection)["values"][1]
    values,items=get_value_for_modification(id_facture)
    items=loads(items)
    for index,value in enumerate(values):
        list_string_var[index].set(value)
    for item in items:
        table.insert("",index=0,values=tuple(item.values()))
    show_widget(frame_client_info, x=0.01, y=0.01)
    #button_valider.configure(command=test)
def get_all_datas(type):
    avance = set_espace_between_3_numbers(avance_entry.get())
    reste = set_espace_between_3_numbers(reste_payer.get())
    main_oeuvre_name = main_oeuvre_descipt.get()
    main_oeuvre_montant = set_espace_between_3_numbers(main_oeuvre.get().strip())
    client_name = nom_client.get()
    client_number = numero_client.get()
    client_address = adresse_client.get()
    facture_name = nom_facture.get()
    Date = date.get()
    if type=="facture":
        main_oeuvre_name=cut_string(main_oeuvre_name,57)
        client_address=cut_string(client_address,60)
        facture_name=cut_string(facture_name,100)
    else:
        main_oeuvre_name = cut_string(main_oeuvre_name, 45)
        client_address = cut_string(client_address, 45)
        facture_name = cut_string(facture_name, 45)
    items = dumps(get_table_values())
    numero_facture = generer_numero_facture(*get_mois_jour(Date)[1:], "/")
    total_materiel = set_espace_between_3_numbers(calcul_montant_total_materiels())
    Total = set_espace_between_3_numbers(calcul_montant_total())
    jour, mois, annee = get_mois_jour(Date)
    if not main_oeuvre_montant:
        main_oeuvre_montant="0"
    return (numero_facture, client_name, client_number, client_address,
            facture_name, Date, items, total_materiel, main_oeuvre_montant, main_oeuvre_name,
            Total, avance, reste, jour, mois, annee)


def calcul_montant_total():
    try:
        main_oeuvre_montant = int(main_oeuvre.get())
        return str(main_oeuvre_montant + calcul_montant_total_materiels())
    except:
        return calcul_montant_total_materiels()


def get_materiel_values():
    material_name = nom_materiel.get()
    quantity = Quantite.get()
    prix_unit = prix_unitaire.get()
    unite = Unite.get()
    prix_Tot = prix_Total.get()
    return (material_name, unite, quantity, prix_unit, prix_Tot)


def get_table_values():
    resultat = []
    values = []
    for element in table.get_children():
        values.append(table.item(element)["values"])
    for value in values:
        value[0]=cut_string(value[0],42)
        resultat.append({list_colonnes[index]: value[index] for index in range(5)})
    return resultat


def set_montant_total_facture():
    main_oeuvre_montant = main_oeuvre.get()
    total_montant_materiel = calcul_montant_total_materiels()
    text = set_espace_between_3_numbers(calcul_montant_total_materiels())
    try:
        text = str(set_espace_between_3_numbers(int(total_montant_materiel) + int(main_oeuvre_montant)))
    except:
        pass
    montant_total_label.configure(text=text)
    root.after(100, set_montant_total_facture)


def set_montant_restant():
    montant_total = montant_total_label.cget("text")
    avance = avance_entry.get()
    try:
        text = float(delete_space_3numbers(montant_total)) - float(delete_space_3numbers(avance))
        if int(text) == text:
            text = int(text)
        string_var_rest.set(value=set_espace_between_3_numbers(text))
    except:
        pass
    root.after(100, set_montant_restant)


def calcul_montant_total_materiels():
    values = get_table_values()
    total = 0
    for materiel in values:
        total += float(delete_space_3numbers(materiel["montant_ht"]))
    if int(total) == total:
        total = int(total)
    return total


def supprimer_materiel():
    try:
        table.delete(get_selected_element()[0])
    except:
        messagebox.showerror("Erreur", "Sélectionner un article puis \n" + "cliquez sur Supprimer")


def get_selected_element(*args):
    return table.selection()


def ajouter_materiel(*args):
    status = gerer_materiel_descrip_montant_total(nom_materiel.get(), delete_space_3numbers(prix_Total.get()))
    if not status[0]:
        messagebox.showerror("Erreur", status[1])
    else:
        values = get_materiel_values()
        table.insert(parent="", index=0, values=values)


def show_montant_total_materiel():
    try:
        text = calcul_montant_total_materiels()
        montant_total_materiel_label.configure(text=set_espace_between_3_numbers(text))
        montant_total_materiel_label1.configure(text=set_espace_between_3_numbers(text))
    except:
        pass
    root.after(100, show_montant_total_materiel)


def modifier_materiel():
    get_table_values()
    selected_element = get_selected_element()
    try:
        values = get_materiel_values()
        table.item(selected_element[0], values=values)
        table.delete(selected_element[0])
    except:
        messagebox.showerror("Erreur", "Sélectionner un article puis \n" + "cliquez sur Modifier")


#remplissage materiel


frame_table = CTkFrame(frame_remplissage, width=1055, height=5)
frame_table.place(relx=0.003, rely=0.4)
table = ttk.Treeview(frame_table, columns=colonnes_materiel_table, show="headings", height=8)
scrollbar = Scrollbar(frame_table, orient="vertical", command=table.yview)
table.bind("<<TreeviewSelect>>", get_selected_element)
scrollbar.pack(fill="y",side="right")

table.pack(fill="both")
table.configure(yscrollcommand=scrollbar.set)
style = ttk.Style()
style.configure("Treeview.Heading",background="#2b2b2b", font=("Bookman Old Style", 17, "bold"),
                borderwidth=1,row_border=1)
style.theme_use("default")
style.configure("Treeview",
font=("Helvetica", 15,), borderwidth=2,rowheight=30)
for colonne in colonnes_materiel_table:
    table.heading(colonne, text=colonne)
for i, colonne in enumerate(colonnes_materiel_table[1:]):
    table.column(colonne, width=list_width_mat_table[i], anchor="n")
table.column("Références", width=400)
table.tag_configure("oddrow",background="lightblue")
table.tag_configure("evenrow",background="white")

frame_materiel = CTkFrame(frame_remplissage_materiel,fg_color=bg_color, width=900, height=190)
frame_materiel.place(relx=0.01, rely=0.01)
stringVar_list = [StringVar(frame_materiel) for _ in range(4)]

materiel_number_label=CTkLabel(frame_materiel, font=(font1, 24, "bold", "underline"), text="Matériel N° " + str(1))
materiel_number_label.place(relx=0.38,rely=0)
CTkLabel(frame_materiel, text="Références:", font=(font1, 24,)).place(relx=0, rely=0.2)
nom_materiel = CTkEntry(frame_materiel, placeholder_text="Références du matériel", corner_radius=10, height=35,
                        textvariable=stringVar_list[0], width=500, font=(font1, 20, "italic"))
nom_materiel.place(relx=0.158, rely=0.2)
CTkLabel(frame_materiel, text="Unité:", font=(font1, 24)).place(relx=0.74, rely=0.2)

Unite = CTkEntry(frame_materiel, textvariable=StringVar(frame_materiel, value="U"), placeholder_text="Unité",
                 corner_radius=10, width=120, font=(font1, 25))
Unite.place(relx=0.83, rely=0.2)
CTkLabel(frame_materiel, text="Quantité:", font=(font1, 23)).place(relx=0, rely=0.7)
Quantite = CTkEntry(frame_materiel, textvariable=StringVar(frame_materiel, value="1"), width=100, font=(font1, 24,),
                    corner_radius=15)
Quantite.place(relx=0.118, rely=0.7)
CTkLabel(frame_materiel, text="Prix Unitaire:", font=(font1, 23)).place(relx=0.25, rely=0.7)
prix_unitaire = CTkEntry(frame_materiel, width=180,textvariable=stringVar_list[3], font=(font1, 24,), corner_radius=10)
prix_unitaire.place(relx=0.42, rely=0.7)

string_var_total = StringVar(frame_materiel, value="")
CTkLabel(frame_materiel, text="Prix Total:", font=(font1, 23)).place(relx=0.632, rely=0.7)
prix_Total = CTkEntry(frame_materiel, textvariable=string_var_total, font=(font1, 24,), corner_radius=10, width=200)
prix_Total.place(relx=0.76, rely=0.69)
frame_list_button = CTkFrame(frame_remplissage,fg_color=bg_color, corner_radius=20, width=170, height=190, border_width=2)
frame_list_button.place(relx=0.825, rely=0.01)
button_ajouter_materiel = CTkButton(frame_list_button, font=(font1, 20),
text="Ajouter", command=ajouter_materiel, corner_radius=10, width=150,height=40)
button_ajouter_materiel.place(relx=0.1, rely=0.72)

button_supprimer_materiel = CTkButton(frame_list_button, font=(font1, 20),
text="Supprimer", command=supprimer_materiel, corner_radius=15, width=150,height=40)


button_modifier_materiel = CTkButton(frame_list_button, font=(font1, 20),
text="Modifier", command=modifier_materiel, corner_radius=15, width=150,height=40)

button_suivant2 = CTkButton(frame_remplissage, font=(font1, 20),
text="Suivant", command=show_frame_last_part, corner_radius=15, width=150, height=40)
button_suivant2.place(relx=0.5, rely=0.9)

frame_total_achat_materiel = CTkFrame(frame_remplissage, width=200, height=36)
frame_total_achat_materiel.place(relx=0.8, rely=0.9)

montant_total_materiel_label1 = CTkLabel(frame_total_achat_materiel, text="",
                                         font=("Bookman Old Style", 24, "bold"))
montant_total_materiel_label1.place(relx=0.02, rely=0.18)
CTkLabel(frame_remplissage, text="Total:", font=(font1, 26, "bold", "italic")).place(relx=0.71, rely=0.9)

frame_remplissage.after(100, set_montant_total_materiel)

#############################################"

# information client

CTkLabel(frame_info_client, text="Informations du client", font=(font1, 25, "bold", "underline","italic"),).place(relx=0.3,
                                                                                                        rely=0.01)
nom_client = CTkEntry(frame_info_client,textvariable=list_string_var[0], width=400, height=40, corner_radius=15
        ,font=("Bookman Old Style", 23),fg_color="#D4D4D4",)
nom_client.place(relx=0.2, rely=0.2)
numero_client = CTkEntry(frame_info_client,textvariable=list_string_var[1], width=320, height=40, corner_radius=16
                         , font=("Bookman Old Style", 24))
numero_client.place(relx=0.2, rely=0.5)

adresse_client = CTkEntry(frame_info_client, width=400, height=40, corner_radius=15
,textvariable = list_string_var[2] , font=("Bookman Old Style", 18))
adresse_client.place(relx=0.2, rely=0.8)

CTkLabel(frame_info_client, text="Nom du client:", font=(font1, 25, "italic")).place(relx=0.001, rely=0.2)

CTkLabel(frame_info_client, text="Téléphone du client:", font=(font1, 22, "italic")).place(relx=0.001, rely=0.5)

CTkLabel(frame_info_client, text="Adresse du client:", font=(font1, 25, "italic")).place(relx=0.001, rely=0.8)
frame_nom_fact_date = CTkFrame(frame_client_info, width=700, height=150)

CTkLabel(frame_client_info, text="Nom de la facture:", font=(font1, 25, "italic")).place(relx=0.5, rely=0.7)

nom_facture = CTkEntry(frame_client_info, textvariable=list_string_var[3],width=520, height=40,
                       corner_radius=16, placeholder_text="Nom de la facture", font=("Bookman Old Style", 25))
nom_facture.place(relx=0.5, rely=0.695)

date = tkcalendar.dateentry.DateEntry(frame_client_info,textvariable=list_string_var[4],width=10, font=(font1, 16),
                                      state="readonly", date_pattern="dd/mm/yyyy")
date.place(relx=0.12, rely=0.7)
CTkLabel(frame_client_info, text="Date:", font=(font1, 28, "italic")).place(relx=0.05, rely=0.69)
bg1 = "#352932"
CTkLabel(frame_client_info, text="Nom de la facture:", font=(font1, 25, "italic")).place(relx=0.3, rely=0.7)


frame_menu = CTkFrame(root, width=185, height=600, fg_color=bg1, border_width=2)
frame_menu.place(relx=0, rely=0.08)

button_suivant1 = CTkButton(frame_client_info, font=(font1, 20),image=img_suivant,
text="Suivant",compound="right", command=show_frame_remplissage_materiel, corner_radius=15, width=150,
                            height=40)
button_suivant1.place(relx=0.65, rely=0.88)



#Menu

button_faire_facture = CTkButton(frame_menu, corner_radius=20, text="Etablir Facture",
                                 font=("Bookman Old Style", 18), height=42, width=150,
                                 command=thread_show_frame_faire_facture)
button_faire_facture.place(relx=0.03, rely=0.15)

button_accueil = CTkButton(frame_menu, corner_radius=20, text=" Menu Accueil",
font=("Bookman Old Style", 18), height=42, width=150,
                                 command=show_frame_accueil)
button_accueil.place(relx=0.02, rely=0.01)

button_verifier_facture = CTkButton(frame_menu, corner_radius=16, text="Vérifier Facture",
                                    font=("Bookman Old Style", 18), height=42, width=140, command=consulter_facture)
button_verifier_facture.place(relx=0.02, rely=0.30)

button_faire_bilan = CTkButton(frame_menu, corner_radius=20, text="Faire Bilan",
                               font=("Bookman Old Style", 18), height=42, width=170, command=faire_bilan)
button_faire_bilan.place(relx=0.028, rely=0.45)
button_menu_bar = CTkButton(root, border_width=0, text="Menu", font=("Bookman Old Style", 18),
                            height=47, width=185, command=thread_bouger_menu, image=img_menu)
button_menu_bar.place(relx=0.001, rely=0.008)

#####################################
#frame_last_part




frame_supp = frame_remplissage_last_part
#frame_supp.place(relx=0.15,rely=0.001)
frame_remplissage_info_supplemntaire = CTkFrame(frame_supp,fg_color=bg_color, width=1100+x, height=380, border_width=2)
frame_remplissage_info_supplemntaire.place(rely=0.001, relx=0.001)
string_var_rest = StringVar(frame_remplissage_last_part)

CTkLabel(frame_remplissage_info_supplemntaire, text="Total Achat Matériel:",
         font=(font1, 23, "bold", "italic")).place(relx=0.25, rely=0.04)

frame_total_achat_materiel = CTkFrame(frame_remplissage_info_supplemntaire, border_width=0, width=250, height=40)
frame_total_achat_materiel.place(relx=0.5, rely=0.03)

montant_total_materiel_label = CTkLabel(frame_total_achat_materiel, text="50 000 000",
                                        font=("Bookman Old Style", 22, "bold"))
montant_total_materiel_label.place(relx=0.3, rely=0.2)

main_oeuvre_descipt = CTkEntry(frame_remplissage_info_supplemntaire, width=530, height=40, corner_radius=15,
textvariable=list_string_var[5]
                               , font=("Bookman Old Style", 23))
main_oeuvre_descipt.place(relx=0.38, rely=0.2)

CTkLabel(frame_remplissage_info_supplemntaire, text=" Montant Main d'œuvre:", font=(font1, 26, "italic")).place(relx=0.001,
                                                                                                        rely=0.39)

main_oeuvre = CTkEntry(frame_remplissage_info_supplemntaire, width=270, height=40, corner_radius=15,
textvariable=list_string_var[6]
                       , font=("Bookman Old Style", 25))
main_oeuvre.place(relx=0.268, rely=0.39)

avance_entry = CTkEntry(frame_remplissage_info_supplemntaire, width=280, height=40, corner_radius=16,
textvariable=list_string_var[7]
                        , font=("Bookman Old Style", 24))
avance_entry.place(relx=0.258, rely=0.6)

reste_payer = CTkEntry(frame_remplissage_info_supplemntaire, textvariable=string_var_rest, width=270, height=40,
corner_radius=15, font=("Bookman Old Style", 23))
reste_payer.place(relx=0.72, rely=0.62)

frame_total = CTkFrame(frame_remplissage_info_supplemntaire, border_width=0, width=250, height=40)
frame_total.place(relx=0.69, rely=0.377)
CTkLabel(frame_remplissage_info_supplemntaire, text="Total:", font=(font1, 27, "bold", "italic")).place(relx=0.6,
                                                                                                        rely=0.39)
button_valider = CTkButton(frame_remplissage_info_supplemntaire, font=(font1, 22),
                           text="Suivant", command=afficher_resume_facture, corner_radius=15, width=170, height=40)
button_valider.place(relx=0.7, rely=0.85)

button_retour1 = CTkButton(frame_remplissage_info_supplemntaire, font=(font1, 22),
text="Retour",image=img_precedent, command=retour2, corner_radius=15, width=170, height=40)
button_retour1.place(relx=0.2, rely=0.85)

button_retour2 = CTkButton(frame_remplissage_materiel,image=img_precedent, font=(font1, 22),
text="Retour", command=retour1, corner_radius=15, width=170, height=40)
button_retour2.place(relx=0.2, rely=0.91)

CTkLabel(frame_remplissage_info_supplemntaire, text="Descriptions de la main d'œuvre:",
         font=(font1, 25, "italic")).place(relx=0.001, rely=0.2)

CTkLabel(frame_remplissage_info_supplemntaire, text=" Montant Avance reçu:", font=(font1, 26, "italic")).place(relx=0.005,
                                                                                                      rely=0.59)
CTkLabel(frame_remplissage_info_supplemntaire, text="Reste à payer:", font=(font1, 24, "italic")).place(relx=0.56,
                                                                                                        rely=0.63)
montant_total_label = CTkLabel(frame_total, text="", font=(font1, 26, "bold"))
montant_total_label.place(relx=0.08, rely=0.1)
directory_to_save_facture = CTkLabel(frame_remplissage_info_supplemntaire, text="")





#consulter facture
def set_facture_in_treewiew(*args):
    for element in list_facture_table.get_children():
        list_facture_table.delete(element)
    Date = date_consulter_fac.get()
    list_factures = consulter_facture_with_date(Date)

    for ind,facture in enumerate(list_factures):
        tag = "evenrow" if ind % 2 == 0 else "oddrow"
        list_facture_table.insert("", index=0,tags=(tag,) ,values=facture)


def pack_modifier_supprimer_button():
    pass

date_consulter_fac = tkcalendar.dateentry.DateEntry(frame_consulter_facture, width=10, font=(font1, 20),
                                                    state="readonly", date_pattern="dd/mm/yyyy")
date_consulter_fac.place(relx=0.08, rely=0.1)
CTkLabel(frame_consulter_facture, text="Date:", font=(font1, 28, "italic")).place(relx=0.01, rely=0.1)

date_consulter_fac.bind("<<DateEntrySelected>>", set_facture_in_treewiew)
frame_table_facture = CTkFrame(frame_consulter_facture,width=1100, height=300,)
frame_table_facture.place(relx=0.005, rely=0.405)

tree_frame=CTkFrame(frame_table_facture,width=1100,height=300)
tree_frame.pack()
list_facture_table = ttk.Treeview(tree_frame, height=10, columns=facture_table_colonnes,
show="headings",)
list_facture_table.pack(expand=True,side="left")

scrollbar_treeview_consult=Scrollbar(tree_frame, command=list_facture_table.yview
,orient="vertical")
scrollbar_treeview_consult.pack(side="right",fill="y")


list_facture_table.configure(yscrollcommand=scrollbar_treeview_consult.set)


style = ttk.Style()
style.configure("Treeview.Heading", font=(font1, 16, 'bold'))
style.configure("Treeview", font=(font1, 12))
for indexe, colonne in enumerate(facture_table_colonnes):
    list_facture_table.heading(column=colonne, text=colonne)
    list_facture_table.column(colonne, width=list_colonnes_width[indexe], anchor="center")
list_facture_table.tag_configure("oddrow",background="lightblue")
list_facture_table.tag_configure("evenrow",background="white")
CTkLabel(frame_consulter_facture, text="Entrer N° Facture:", font=(font1, 28, "italic")).place(relx=0.28, rely=0.1)
numero_facture_entry = CTkEntry(frame_consulter_facture, width=270, height=40, corner_radius=15,
textvariable=StringVar(frame_consulter_facture, value="N°FP00"), font=("Bookman Old Style", 25))
numero_facture_entry.place(relx=0.5, rely=0.1)


def get_selected_treeview_element(*args):
    return list_facture_table.selection()


def set_frame_list_button():
    selection = ""
    try:
        selection = get_selected_element()[0]
    except:
        pass
    if selection:
        button_supprimer_materiel.place(relx=0.1, rely=0.4)
        button_modifier_materiel.place(relx=0.1, rely=0.1)
    else:
        button_supprimer_materiel.place(relx=1, rely=0.5)
        button_modifier_materiel.place(relx=1, rely=0.1)

    root.after(100, set_frame_list_button)


def show_all_facture():
    values = get_all_database_facture()
    for children in list_facture_table.get_children():
        list_facture_table.delete(children)
    for indexe, value in enumerate(values):
        tag = "evenrow" if indexe % 2 == 0 else "oddrow"
        list_facture_table.insert("",tags=(tag,), index=indexe, values=value)


def exporter_fichier():
    get_exporter_path()
    path = label_exporter_fichier.cget("text")
    element = get_selected_treeview_element()
    id_facture = list_facture_table.item(element[0])["values"][1]
    data = facture_data(id_facture)
    document = Facture(*data[:-3], path)
    document.produire_facture()
    messagebox.showinfo("", "Exporter avec succès")


def chercher_facture(*args):
    for element in list_facture_table.get_children():
        list_facture_table.delete(element)
    Date = date.get()
    numero_facture = numero_facture_entry.get()
    values = get_facture_with_id(numero_facture)
    if values:
        list_facture_table.insert("", 0, values=values)
    else:
        messagebox.showinfo("Recherche de la facture", "Aucune Facture enregistrée ")


def supprimer_fichier():
    element = get_selected_treeview_element()
    id_facture = list_facture_table.item(element[0])["values"][1]
    resultat_supprimer = messagebox.askokcancel("Supprimer La Facture",
                                                "être vous sûr de vouloir \nsupprimer cette facture ?")
    if resultat_supprimer:
        list_facture_table.delete(element[0])
        supprimer_facture(id_facture)


def get_selected_facture(*args):
    return list_facture_table.selection()


def get_exporter_path():
    path = filedialog.askdirectory()
    label_exporter_fichier.configure(text=path)


def modifier_reste_seul():
    montant_entree=delete_space_3numbers(entry_Regler.get())
    status=gerer_montant(montant_entree)
    if status:
        id_facture = list_facture_table.item(get_selected_facture()[0])["values"][1]
        reste=float(delete_space_3numbers(get_reste(id_facture)))
        if gerer_reglement_reste_payer(reste,float(montant_entree)):
            status1=messagebox.askyesno("status de la modification du reste à payer",
            "Confirmez-vous  cette modification ?")
            if status1:

                update_reste(id_facture,float(montant_entree))
                entry_Regler.delete(0,END)
                messagebox.showinfo("Reste à payer modifier avec succès","Modification éffectuée avec succès ")
        else:
            messagebox.showerror("Montant à regler doit inférieur\n à"+str(reste))
    else:

        messagebox.showerror("modification", "Montant entré est invalide")


def set_modifier_reste(*args):
    selection=get_selected_facture()
    if selection:
        reste = (get_reste(list_facture_table.item(selection[0])["values"][1]))
        database_reste.configure(text=set_espace_between_3_numbers(reste))
        try:
            montant_entree = gerer_float_numbre(delete_space_3numbers(entry_Regler.get()))

            reste1=float(delete_space_3numbers(reste.strip()))
            Resultat_reste.configure(text=set_espace_between_3_numbers(calcul_difference(reste1,float(montant_entree))).strip())
        except:

            Resultat_reste.configure(text=set_espace_between_3_numbers(reste))
    root.after(100,set_modifier_reste)
def modifier_reste():
    show_widget(frame_reste_payer)




def pack_list_consulter_button_mod_supp_exp():
    if get_selected_facture():
        frame_list_button_consult.place(relx=0.76, y=0.01)
    else:
        frame_list_button_consult.place(relx=1.2, y=0.01)

    root.after(100,pack_list_consulter_button_mod_supp_exp)
def fill_entry_regler():
    id_facture = list_facture_table.item(get_selected_facture()[0])["values"][1]
    reste = (delete_space_3numbers(get_reste(id_facture)))
    if checkbox.get():
        modifier_reste_stringvar.set(reste)
    else:
        modifier_reste_stringvar.set("")



frame_label_reste1 = CTkFrame(frame_modifier_reste, width=200, height=40, border_width=0)
frame_label_reste1.place(relx=0.58, rely=0.2)
database_reste = CTkLabel(frame_label_reste1, text="", font=(font1, 27, "bold"))
database_reste.place(relx=0.1, rely=0.1)

frame_label_reste = CTkFrame(frame_modifier_reste, width=200, height=40, border_width=0)
frame_label_reste.place(relx=0.58, rely=0.68)
Resultat_reste = CTkLabel(frame_label_reste, text="", font=(font1, 27, "bold"))
Resultat_reste.place(relx=0.1, rely=0.1)

modifier_reste_stringvar = StringVar(frame_modifier_reste)
entry_Regler = CTkEntry(frame_modifier_reste,textvariable=modifier_reste_stringvar,
                        height=40, width=200, font=(font1, 26), corner_radius=16)
entry_Regler.place(relx=0.54, rely=0.44)

entry_Regler.bind("<Key>", set_modifier_reste)
CTkLabel(frame_modifier_reste, text="Enter le montant à régler:",
         font=(font1, 23, "italic")).place(relx=0.1, rely=0.44)

CTkLabel(frame_modifier_reste, text="Régler le Reste à Payer",
         font=(font1, 27, "italic", 'bold')).place(relx=0.3, rely=0.01)
checkbox=CTkCheckBox(frame_modifier_reste,
    onvalue=1,offvalue=0,command=fill_entry_regler,text="")
CTkLabel(frame_modifier_reste,text="Tout",font=(font1, 26,"italic")).place(relx=0.61,rely=0.352)
checkbox.place(relx=0.7,rely=0.36)
CTkLabel(frame_modifier_reste, text="Voici ce qui reste à payer:",
         font=(font1, 26, "italic")).place(relx=0.1, rely=0.68)
CTkLabel(frame_modifier_reste, text="Voici ce qui restait à payer:",
         font=(font1, 26, "italic")).place(relx=0.1, rely=0.2)

valider_reste_payer = CTkButton(frame_modifier_reste, font=(font1, 20),
text="Valider", command=modifier_reste_seul, corner_radius=15, width=150,height=40)
valider_reste_payer.place(relx=0.5, rely=0.83)

button_retour3 = CTkButton(frame_modifier_reste, image=img_precedent,font=(font1, 20),
text="Retour", command=retour3, corner_radius=15, width=150,height=40)
button_retour3.place(relx=0.1, rely=0.83)




frame_list_button_consult = CTkFrame(frame_consulter_facture,fg_color=bg_color, corner_radius=20, width=250, height=220, border_width=2)


label_exporter_fichier = CTkLabel(frame_consulter_facture, text="")

button_rechercher = CTkButton(frame_consulter_facture, font=(font1, 20), text=" Chercher Facture",
                              command=chercher_facture, corner_radius=15, width=150, height=45)
button_rechercher.place(relx=0.42, rely=0.22)

button_show_all_facture = CTkButton(frame_consulter_facture, font=(font1, 20),
                                    text=" Voir toutes les factures", command=show_all_facture, corner_radius=15,
                                    width=150,height=45)
button_show_all_facture.place(relx=0.1, rely=0.22)

list_facture_table.bind("<<TreeviewSelect>>", get_selected_facture)

button_supprimer_consult = CTkButton(frame_list_button_consult, font=(font1, 21),
text="Supprimer Facture", command=supprimer_fichier, corner_radius=15,width=160,height=40)

numero_facture_entry.bind("<Return>", chercher_facture)

button_modifier_consulter = CTkButton(frame_list_button_consult, font=(font1, 23), height=40,
text="Modifier Facture", command=modifier_completement_facture, corner_radius=15,width=190)

button_modifier_reste_consulter = CTkButton(frame_list_button_consult, font=(font1, 20), height=40,
text="Régler reste à payer", command=modifier_reste, corner_radius=15,width=150)
img_pdf_exporter=CTkImage(ImageTk.Image.open("pdf.png"),size=(28,28))
button_exporter_fact = CTkButton(frame_list_button_consult, font=(font1, 20), height=40,
text="Exporter Facture", image=img_pdf_exporter,command=exporter_fichier, corner_radius=15, width=160, )


button_exporter_fact.place(relx=0.02, rely=0.79)
button_supprimer_consult.place(relx=0.05, rely=0.525)
button_modifier_consulter.place(relx=0.05, rely=0.28)
button_modifier_reste_consulter.place(relx=0.02,rely=0.05)

#frame_bilan


def exporter_bilan():
    Date1, Date2 = date1.get(), date2.get()
    all_data=[]
    if checkbox_bilan.get():
        all_data=get_all_database_data()
        Date1,Date2="",""
    else:
        all_data=get_bilan(Date1,Date2)

    list_factures, totaux = calcul_totaux_bilan(all_data,Date1, Date2)
    print(Date1,Date2)
    if not list_factures:
        messagebox.showinfo("Status du Bilan", "desolé aucune facture enregistrée au cours\n de " +
                            str(Date1) + "  au  " + str(Date2))
    else:
        get_exporter_bilan_path()
        save_directory_path = exporter_bilan_path.cget("text")
        if save_directory_path:
            document = Bilan(list_factures, Date1, Date2, save_directory_path, *totaux)
            document.faire_PDF()
            messagebox.showinfo("Status du Bilan", "Bilan Sauvegardé\n avec succès")


def get_exporter_bilan_path():
    path = filedialog.askdirectory()
    exporter_bilan_path.configure(text=path)


def set_bilan_treeview(*args):
    values = get_bilan(date1.get(), date2.get())

    for children in bilan_treewiew.get_children():
        bilan_treewiew.delete(children)
    for i,value in enumerate(values):
        tag = "evenrow" if i % 2 == 0 else "oddrow"
        bilan_treewiew.insert("", index=0, tags=(tag,),values=list(value.values())[:-1])



def refresh_bilan_treeview(*args):
    set_bilan_treeview()
def call_checbox_bilan_fonction():
    if checkbox_bilan.get():
        set_all_facture_treeview()
    else:
        for children in bilan_treewiew.get_children():
            bilan_treewiew.delete(children)
def set_all_facture_treeview():
    for children in bilan_treewiew.get_children():
        bilan_treewiew.delete(children)
    values=get_all_database_facture()
    for i,value in enumerate(values):
        tag = "evenrow" if i % 2 == 0 else "oddrow"
        bilan_treewiew.insert("", index=0, values=value,tags=(tag,))
    # root.after(500, set_bilan_treeview)



# date1
frame_bilan = CTkFrame(frame_faire_bilan,fg_color=bg_color, width=1100+x, height=630)
frame_bilan.place(relx=0.001, rely=0.001)
frame_treeview_bilan=CTkFrame(frame_faire_bilan,width=1070,height=300)
frame_treeview_bilan.place(relx=0.005,rely=0.27)
date1 = tkcalendar.dateentry.DateEntry(frame_bilan, width=10, font=(font1, 18),
                                       state="readonly", date_pattern="dd/mm/yyyy")
date1.place(relx=0.18, rely=0.1)
CTkLabel(frame_bilan, text="Date Début:", font=(font1, 28, "italic")).place(relx=0.02, rely=0.1)
date1.bind("<<DateEntrySelected>>", refresh_bilan_treeview)

# date1
date2 = tkcalendar.dateentry.DateEntry(frame_bilan, width=10, font=(font1, 18),
                                       state="readonly", date_pattern="dd/mm/yyyy")
date2.place(relx=0.55, rely=0.1)
CTkLabel(frame_bilan, text="Date Fin:", font=(font1, 28, "italic")).place(relx=0.43, rely=0.1)
date2.bind("<<DateEntrySelected>>", set_bilan_treeview)
exporter_bilan_path = CTkLabel(frame_bilan, text='')
CTkLabel(frame_bilan,font=(font1,23),text="Selectionnez toutes les Factures").place(relx=0.15,rely=0.2)
checkbox_bilan=CTkCheckBox(frame_bilan,text="",checkbox_height=25,command=call_checbox_bilan_fonction)
checkbox_bilan.place(relx=0.49,rely=0.208)

faire_bilan_button = CTkButton(frame_bilan, font=(font1, 20),
text="Exporter le bilan en fichier PDF", command=exporter_bilan, corner_radius=15,
    width=150,height=30,image=img_pdf)
faire_bilan_button.place(relx=0.32, rely=0.8)

bilan_treewiew = ttk.Treeview(frame_treeview_bilan, height=10, columns=colonne_bilan,
show="headings",)

bilan_treewiew.tag_configure("oddrow",background="lightblue")
bilan_treewiew.tag_configure("evenrow",background="white")
scrollbar_treeview_bilan=Scrollbar(frame_treeview_bilan,command=bilan_treewiew.yview
,orient="vertical")
scrollbar_treeview_bilan.pack(fill="y",side="right")
bilan_treewiew.pack(fill="x")
bilan_treewiew.configure(yscrollcommand=scrollbar_treeview_bilan.set)

list_witdh_bilan_treview = [200, 170, 120, 140, 145, 150, 150]
for index, colonne in enumerate(colonne_bilan):
    bilan_treewiew.heading(column=colonne, text=colonne)
    bilan_treewiew.column(colonne, width=list_witdh_bilan_treview[index],
                          anchor=list_anchor_coloums[index])

CTkLabel(frame_bilan, text="Faire le bilan d'une période donnée!",
         font=(font1, 27, "bold", "italic", "underline")).place(
    relx=0.2, rely=0.01)

###################################
#frame_menu_principale

def set_time():
    Time = strftime("%H:%M:%S").strip()
    date=strftime("%d/%m/%Y")
    label_heure.configure(text=Time+"\n"+date)
    root.after(1000, set_time)



CTkLabel(frame_menu_principale, text="", image=image_faire_fact).place(relx=0.05, rely=0.28)
CTkLabel(frame_menu_principale, text="", image=image_consult_fact).place(relx=0.4, rely=0.28)
CTkLabel(frame_menu_principale, text="", image=image_faire_bilan).place(relx=0.7, rely=0.28)


CTkLabel(frame_menu_principale, text="Bienvenue sur le logiciel de gestion de dévis de MANTECH"
, font=(font1, 28, "bold", "underline","italic","roman"), fg_color="#2CC985").place(relx=0.02, rely=0.01)

button_faire_facture = CTkButton(frame_menu_principale, corner_radius=20, text="Etablir Facture",
                                 font=("Bookman Old Style", 18), height=42, width=150,
                                 command=thread_show_frame_faire_facture)
button_faire_facture.place(relx=0.08, rely=0.7)

button_verifier_facture = CTkButton(frame_menu_principale, corner_radius=16, text="Vérifier Facture",
                                    font=("Bookman Old Style", 18), height=42, width=140, command=consulter_facture)
button_verifier_facture.place(relx=0.44, rely=0.7)

button_faire_bilan = CTkButton(frame_menu_principale, corner_radius=20, text="Faire Bilan",
                               font=("Bookman Old Style", 18), height=42, width=170, command=faire_bilan)
button_faire_bilan.place(relx=0.72, rely=0.7)

label_heure = CTkLabel(frame_menu_principale, text="", font=(font1, 32),
                    fg_color="#7DA1C6")
label_heure.place(relx=0.77, rely=0.008)
root.after(1000, set_time)

switch_mode=CTkSwitch(frame_menu,text="",onvalue=1,
        command=change_mode_dark_light,switch_height=22,switch_width=48)
switch_mode.place(relx=0.67,rely=0.905)
CTkLabel(frame_menu,text="Mode Sombre",font=(font1,17)).place(relx=0.01,rely=0.9)



#show frames

show_widget(frame_remplissage_last_part, x=0.001, y=0.001)
root.after(100, set_montant_total_facture)
root.after(100, set_montant_restant)
root.after(100, show_montant_total_materiel)
root.after(100, set_frame_list_button)
root.after(100, pack_modifier_supprimer_button)
root.after(100, set_modifier_reste)
root.after(100,refresh_materiel_number)

root.after(100, pack_list_consulter_button_mod_supp_exp)


change_mode_dark_light()
root.mainloop()

