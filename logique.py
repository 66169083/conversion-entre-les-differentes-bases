import json
from sqlite3 import connect
from pandas import date_range
from fpdf import FPDF




list_colonnes = ["client", "Num_Facture", "Date", "Materiel", "Main_oeuvre", "montant_ht", "Reste","Montant_avance"]
font1 = "Bookman Old Style"
def set_espace_between_3_numbers(numbers):
    if " " in str(numbers).strip():
        return numbers
    else:
        numbers =str(numbers)[::-1].strip()
        number = ""
        for caractere in str(numbers):
            if caractere == " ":
                pass
            else:
                number += caractere
        a = len(number)
        resultat = ""
        for i in range(0, a, 3):
            resultat += number[i:i + 3] + " "
        return resultat[::-1]


class Facture(FPDF):

    def __init__(self, numero_facture, client, tel, addresse, facture_name,
                 date, items, total_achat, montant_main_oeuvre, main_oeuvre_nom, total, avance, reste,
                 directory_path):
        self.total = total
        self.reste = set_espace_between_3_numbers(reste)
        self.avance = set_espace_between_3_numbers(avance)
        self.main_oeuvre_nom = main_oeuvre_nom
        self.montant_main_oeuvre = set_espace_between_3_numbers(montant_main_oeuvre)
        self.total_achat = set_espace_between_3_numbers(total_achat)
        self.tel = tel
        self.addresse = addresse
        self.items = json.loads(items)
        self.client = client
        self.facture_name = facture_name
        self.numero_facture = numero_facture
        self.date = date
        self.directory_path = directory_path
        self.logo = "logo.jpg"
        self.numero=""
        self.nom_entreprise="M.A.N.T.E.C.H"


        super().__init__()
        self.add_font("myfont", "B", "Bookman_Bold.ttf")
        self.add_font("myfont", "BI", "Bookman_Bold_Italic.ttf")
        self.add_font("myfont", "", "Bookman_font.ttf")
        self.add_font("myfont", "I", "Bookman_Italic.ttf")
        self.alias_nb_pages()



    def footer(self, ):
        text1 = "........................................................................................................................................................................................................."
        text2 = "MANTECH SOLUTIONS & SERVICES - IFU:00224067E - RCCM: BF-OUA-01-2024-B12-01614-09BP01490 Ouagadougou 09"
        text3 = "Tél.:78217611 / 74861180 / 70340909"

        self.set_y(-22)
        self.set_font('myfont', 'I', 9)
        self.cell(190, 10, text1, border=0, align="C", )
        self.set_y(-18)
        self.cell(190, 10, text2, border=0, align="C", )
        self.set_y(-14)
        self.cell(190, 10, text3, border=0, align="C", )
        self.set_font('myfont', 'B', 12)
        self.set_y(-8)
        total_pages="{nb}"

        self.cell(190,5, f"{self.page_no()}/{total_pages}", border=0, align="R", )
        self.total_page = self.pages_count

    def ajouter_filigrane(self):
        self.set_font("Helvetica", "", 30)
        self.set_text_color(200, 200, 200)
        with self.rotation(55, self.w / 1.1, self.h / 2):
            self.text((self.w) / 20000, self.h / 3.2, self.nom_entreprise)

        self.set_text_color(0,0,0)
    def set_header(self, ):
        self.image(self.logo, w=194, h=18, x=8, y=10)
        self.set_font('myfont', '', 10)
        self.ajouter_filigrane()
        # set facture numero
        self.set_line_width(0.2)
        self.set_font("myfont", "BI", 13, )
        self.set_fill_color(174, 174, 174)
        self.set_xy(10, 35)
        self.cell(190, 6, "Facture Proforma " + str(self.numero_facture), 0, align="C", fill=True)
        self.ln()

        # client info
        self.set_font('myfont', 'BI', 12, )
        self.ln()
        self.set_line_width(0.3)
        self.multi_cell(150, 8, self.merge_client_info(), 1, )
        self.set_line_width(1)

        # set date
        self.set_font("myfont", "", 14)
        self.set_line_width(0.3)
        self.set_xy(162, y=60)
        self.cell(35, 6, self.date, border=1, align="L")
        # set_facture_name
        self.ln()
        self.set_font("myfont", "B", 12)
        self.set_line_width(0.4)
        self.ln()

        self.multi_cell(188, 8,self.facture_name,  align="C", border=1)
        self.ln()
    def produire_facture(self):
        if str(self.total_achat)=="0":
            self.produire_facture_main_oeuvre_unique()
        elif str(self.montant_main_oeuvre)=="0":
            self.produire_facture_achat_materiel_unique()
        else:
            self.produire_facture_complete()


    def set_add_materiel_header(self,numero="I. "):
        self.set_line_width(0.5)
        self.set_font('myfont', 'B', 12)

        self.cell(188, 7, str(numero) + "Achat de matériel", align="L", border=1)
        self.ln()
        #self.set_xy(10, 100)
        self.set_font('myfont', 'B', 10)
        self.cell(98, 8, 'Références', 1, align="C")
        self.cell(15, 8, 'Unité', 1, align="C")
        self.cell(15, 8, 'Qté', 1, align="C")
        self.cell(30, 8, 'Prix unitaire', 1, align="C")
        self.cell(30, 8, 'Montant HT', 1, align="C")
        self.ln()
        # set partie materiel
        self.set_font("myfont", "B", 12)
        self.set_line_width(0.3)


    def merge_client_info(self):
        resultat = ""
        list_test = [f'DOIT: {self.client}', f'Numéro Tel: {self.tel}', f'Adresse: {self.addresse}']
        for text in list_test:
            resultat += text + "\n"
        return resultat


    def add_materiels(self):
        self.set_font('myfont', '', 10)
        #self.set_xy(10, 126)
        self.set_line_width(0.3)
        for item in self.items:
            if self.get_y() < 260:
                self.cell(98, 6, str(item['reference']), 1)
                self.cell(15, 6, str(item['unite']), 1, align="C")
                self.cell(15, 6, str(item['qte']), 1, align="C")
                self.cell(30, 6, f"{set_espace_between_3_numbers(item['prix_unitaire'])}", 1, align="C")
                self.cell(30, 6, f"{set_espace_between_3_numbers(item['montant_ht'])}", 1, align="C")
                self.ln()

            else:
                self.set_new_page_materiel()
                self.set_font('myfont', '', 10)
                #self.set_xy(10, 127)
                self.set_line_width(0.3)
                self.cell(90, 8, str(item['reference']), 1)
                self.cell(15, 8, str(item['qte']), 1, align="C")
                self.cell(15, 8, str(item['unite']), 1, align="C")
                self.cell(30, 8, f"{set_espace_between_3_numbers(item['prix_unitaire'])}", 1, align="C")
                self.cell(38, 8, f"{set_espace_between_3_numbers(item['montant_ht'])}", 1, align="C")
                self.ln()
        if self.get_y() > 256:
            self.set_add_materiel_header()
        else:
            pass
        # self.ln()
        self.set_font("myfont", "BI", 12)
        self.cell(158, 6, "Total achat de matériel", 1)
        self.set_font("myfont", "B", 12)

        self.cell(30, 6, str(self.total_achat), 1, align="C")
    def set_new_page_materiel(self):
        self.add_page()
        self.set_add_materiel_header()

    def set_main_oeuvre_header(self,numero=""):
        self.set_font('myfont', 'BI', 12)
        self.set_xy(10, self.get_y() + 15)
        self.cell(188, 6, numero+" Main d'œuvre", border=1, align="L")

        if self.get_y() + 8 > 256:
            self.add_new_page()
        else:
            pass
        self.set_font('myfont', '', 10)
        self.set_xy(10, self.get_y() + 8)
        self.cell(150, 6, self.main_oeuvre_nom, border=1)
        self.cell(38, 6, self.montant_main_oeuvre, border=1, align="C")


    def set_last_part(self):
        self.set_y(self.get_y()+10)
        self.set_line_width(0.22)
        self.set_font('myfont', 'BI', 12)
        self.cell(150, 6, "Montant Total HT", border=1)
        self.set_font('myfont', 'B', 10)

        self.cell(38, 6, set_espace_between_3_numbers(self.total), border=1, align="C")
        if self.get_y() + 8 > 256:
            self.add_new_page()
        else:
            pass

        self.set_xy(10, self.get_y() + 20)
        self.set_font('myfont', 'I', 12)
        self.cell(150, 6, "Avance reçu pour démarrage des travaux (HT)", border=1, align="L")
        self.set_font('myfont', 'BI', 12)

        self.cell(38, 6, self.avance, border=1, align="C")

        if self.get_y() + 8 > 256:
            self.add_new_page()
        else:
            pass
        self.set_xy(10, self.get_y() + 8)
        self.set_font('myfont', 'I', 12)
        self.cell(150, 6, "Reste à payer (HT)", border=1, align="L")
        self.set_font('myfont', 'BI', 12)
        self.cell(38, 6, self.reste, border=1, align="C")

        # La Direction
        if (self.get_y() + 20) > 250:
            self.add_new_page()
        else:
            pass
        self.set_xy(150, self.get_y() + 22)
        self.cell(38, 8, "La Direction", border=0, align="C")
        number=self.pages_count

    def add_new_page(self):
        self.add_page()
        self.set_header()

    def remplir_fichier(self):
        self.set_add_materiel_header()
        self.add_materiels()
    def produire_facture_achat_materiel_unique(self):
        self.add_new_page()
        self.set_add_materiel_header("")
        self.add_materiels()
        self.set_last_part()
        #self.ajouter_filigrane()
        self.produire_pdf()

    def produire_facture_main_oeuvre_unique(self):
        self.add_new_page()
        self.set_main_oeuvre_header()
        self.set_last_part()
        #self.ajouter_filigrane()
        self.produire_pdf()

    def produire_facture_complete(self):
        self.add_new_page()
        self.set_add_materiel_header("I. ")
        self.add_materiels()
        self.set_main_oeuvre_header("II.")
        self.set_last_part()
        self.produire_pdf()

    def produire_pdf(self):
        self.ajouter_filigrane()
        self.output(f"{self.directory_path}/Facture Proforma {path_numero_facture(self.numero_facture,'file')}.pdf")

    # Données de la facture


def change_date_format(date:str):
    resultat=""
    result=date.split("/",3)[::-1]
    for element in result:
        resultat+=element+"/"
    return resultat[:-1]
def delete_space_3numbers(number):
    resultat = ""
    for caractere in str(number):
        if caractere == " ":
            pass
        else:
            resultat += caractere
    return resultat
def get_mois_jour(date: str):
    jour, mois, annee = date.split("/", 3)
    return jour, mois, annee
def gerer_materiel_descrip_montant_total(reference, montant):
    resultant_error = ""
    if reference.strip() == "":
        resultant_error += "Description vide" + "\n"
    else:
        pass
    try:
        montant = float(montant)
        if montant < 0:
            raise ValueError
    except:
        resultant_error += "montant_invalide"
    if resultant_error:
        return False, resultant_error
    return True, resultant_error


def gerer_montant(montant):
    montant=str(montant)
    status = False
    try:
        montant = float(montant.strip())
        if not montant >= 0:
            raise ValueError
        status = True
    except:
        pass
    return status
def gerer_montant_total_avance_reste(avance, Total):
    list_errors = "Avance invalide"
    status = False
    total_errors = ""
    try:
        if not gerer_montant(avance):
            total_errors += list_errors + "\n"
            pass
        if (float(Total) - float(avance)) < 0:
            total_errors+="Avance ne doit pas être plus grand que total"
            raise ValueError
        status=True
    except:
        pass
    return status, total_errors
#print(gerer_montant_total_avance_reste(20000,50000))

def generer_numero_facture(mois, anne, format):
    sql = f"""SELECT Numero_facture from DATA where Mois="{mois}" and Annee='{anne}' """
    connexion = connect("database.db")
    data = connexion.execute(sql)
    data = data.fetchall()

    Numero_facture = f"N°FP001{format}{mois}{format}{anne}"
    if data:
        rang=get_rang_facture(data[-1][0])

        Numero_facture = f"N°FP{rang + 1:03d}{format}{mois}{format}{anne}"
    return Numero_facture
def get_rang_facture(numero_facture:str):
    resultat=numero_facture.split("/",3)[0][4:]
    return int(resultat)


#print(generer_numero_facture("11","2024","/"))
def path_numero_facture(numero_facture, nature):
    if nature == "file":
        return numero_facture.replace("/", "_")
    return numero_facture


def insert_facture(data):
    connexion = connect("database.db")
    squery = """INSERT INTO DATA VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
    connexion.execute(squery, data)
    connexion.commit()
    connexion.close()

def get_database_data(id_facture):
    connexion = connect("database.db")
    sql = f"""SELECT * from DATA where Numero_facture="{id_facture}" """
    data = connexion.execute(sql).fetchone()[:-3]
    return data



def consulter_facture_with_date(date):
    datas = []
    connexion = connect("database.db")
    data = connexion.execute(f"""SELECT Nom_client,Numero_facture,Date,Montant_achat_materiel,
    Montant_main_oeuvre,Montant_Total,Montant_reste from DATA where Date="{date}" """)
    return data.fetchall()
def get_list_bilan_facture(date):
    datas = []
    connexion = connect("database.db")
    data = connexion.execute(f"""SELECT Nom_client,Numero_facture,Date,Montant_achat_materiel,
    Montant_main_oeuvre,Montant_Total,Montant_reste,Montant_avance from DATA where Date="{date}" """)
    data = data.fetchall()
    for facture in data:
        datas.append({list_colonnes[i]: facture[i] for i in range(8)})
    return datas
def get_all_database_facture():
    connexion = connect("database.db")
    data = connexion.execute(f"""SELECT Nom_client,Numero_facture,Date,Montant_achat_materiel,
        Montant_main_oeuvre,Montant_Total,Montant_reste,Montant_avance from DATA """)
    return  data.fetchall()


def get_facture_with_id(id_facture):
    connexion = connect("database.db")
    data = connexion.execute(f"""SELECT Nom_client,Numero_facture,Date,Montant_achat_materiel,
    Montant_Main_oeuvre,Montant_Total,Montant_Reste from DATA where Numero_facture='{id_facture}' """)
    return data.fetchone()
def get_all_database_data():
    connexion = connect("database.db")
    totaux_colonnes = ["client","Num_Facture","Date","Materiel", "Main_oeuvre", "montant_ht", "Reste","Montant_avance"]
    resultat=[]
    data = connexion.execute(f"""SELECT Nom_client,Numero_facture,Date,Montant_achat_materiel,
    Montant_Main_oeuvre,Montant_Total,Montant_Reste,Montant_avance from DATA """)
    for value in data.fetchall():

        resultat.append({totaux_colonnes[index]:value[index] for index,colonne in enumerate(totaux_colonnes)})
    return resultat
#print(get_all_database_data())

#print(get_facture_with_id("N°FP001/11/2024"))
def calcul_difference(nombre1,nombre2):
    resultat=nombre1-nombre2
    if int(resultat)==resultat:
        return int(resultat)
    return resultat

def facture_data(id_facture):
    connexion = connect("database.db")
    request = connexion.execute(f"""SELECT * FROM DATA WHERE Numero_facture="{id_facture}" """)
    return request.fetchone()

#print(facture_data("N°FP004/11/2024"))

def supprimer_facture(id_facture):
    connexion = connect("database.db")
    connexion.execute(f"""DELETE FROM DATA WHERE Numero_facture='{id_facture}' """)
    connexion.commit()
    connexion.close()
def generer_dates_bilan(date1, date2):
    resultat = []
    list_date = date_range(start=change_date_format(date1), end=change_date_format(date2),freq="D")
    for date in list_date:
        result = ""
        value = (str(date)[:10].strip().replace("-", "/")).split("/", 3)
        result += value[2] + "/" + value[1] + "/" + value[0]
        resultat.append(result)
    return resultat


#print(generer_dates_bilan("2024/11/21","2024/11/12"))
def get_bilan(date1, date2):
    list_dates = generer_dates_bilan(date1, date2)
    resultat = []
    for date in list_dates:
        resultat+=(get_list_bilan_facture(date))
    return resultat


def calcul_totaux_bilan(list_values,date1, date2):
    if not date1 and date2 :
        list_values = get_bilan(date1=date1, date2=date2)
    total_achat_materiel, total_main_oeuvre_bilan, total_reste, Total ,Montant_avance= 0, 0,0, 0, 0
    list_resultat = [total_achat_materiel, total_main_oeuvre_bilan, total_reste, Total,Montant_avance]
    totaux_colonnes = ["Materiel", "Main_oeuvre", "montant_ht", "Reste","Montant_avance"]
    if list_resultat:
        for value in list_values:
            for index, colonne in enumerate(totaux_colonnes):
                if value[colonne] == "":
                    pass
                else:
                    list_resultat[index] += int(delete_space_3numbers(value[colonne].strip()))
    return list_values, list_resultat
#print(calcul_totaux_bilan([],"2024/11/10","2024/11/28"))

# print(calcul_totaux_bilan("20/11/2024","21/11/2024"))
def Modifier_facture(id_facture):
    connexion = connect("database.db")
    connexion.commit()
    connexion.close()

def get_reste(id_facture):
    connexion=connect("database.db")
    data=connexion.execute(f"""select Montant_reste from data where numero_facture='{id_facture}' """)
    return data.fetchone()[0]
def update_reste(id_facture,montant_regle):
    connexion = connect("database.db")
    avance=connexion.execute(f"""select Montant_avance,Montant_reste from data where Numero_facture='{id_facture}' """)
    avance,reste=avance.fetchone()
    avance,reste=(gerer_float_numbre(float(delete_space_3numbers(avance))+(float(montant_regle))),
    gerer_float_numbre(float(delete_space_3numbers(reste))-float(montant_regle)))
    data = connexion.execute(f"""Update data set Montant_reste='{set_espace_between_3_numbers(gerer_float_numbre(reste))}',
    Montant_avance='{set_espace_between_3_numbers(gerer_float_numbre(avance))}' where numero_facture='{id_facture}' """)
    connexion.commit()
    connexion.close()

#update_reste("N°FP005/11/2024",10000)
class Bilan(FPDF):

    def __init__(self, items, date1, date2, save_directory, montant_materiel,
                 montant_main_oeuvre,  Total,reste, avance):
        self.items = items
        self.logo = "logo.jpg"
        self.save_directory = save_directory
        self.montant_materiel = set_espace_between_3_numbers(montant_materiel)
        self.montant_main_oeuvre = set_espace_between_3_numbers(montant_main_oeuvre)
        self.reste = set_espace_between_3_numbers(reste)
        self.Total = set_espace_between_3_numbers(Total)
        self.avance = set_espace_between_3_numbers(avance)
        self.date1=date1
        self.date2=date2

        super().__init__()
        self.add_font("myfont","","Bookman_font.ttf")
        self.add_font("myfont","B","Bookman_Bold.ttf")
        self.add_font("myfont","I","Bookman_Italic.ttf")
        self.add_font("myfont","BI","Bookman_Bold_Italic.ttf")


    def footer(self, ):
        text1 = "........................................................................................................................................................................................................."
        text2 = "MANTECH SOLUTIONS & SERVICES - IFU:00224067E - RCCM: BF-OUA-01-2024-B12-01614-09BP01490 Ouagadougou 09"
        text3 = "Tél.:78217611/74861180/70340909"
        self.set_y(-20)
        self.set_font('myfont', 'I', 8)
        self.cell(190, 10, text1, border=0, align="C", )
        self.set_y(-16)
        self.cell(190, 10, text2, border=0, align="C", )
        self.set_y(-13)
        self.cell(190, 10, text3, border=0, align="C", )

    def set_header(self, ):

        self.image(self.logo, w=200, h=18, x=8, y=10)
        self.set_font('myfont', '', 10)

        # set facture numero
        self.set_font("myfont", "BI", 16, )
        self.set_fill_color(174, 174, 174)
        self.set_xy(10, 40)
        if not (self.date2 and self.date1):
            self.periode="Bilan général"
        else:
            self.periode=f"Bilan du {self.date1} Au {self.date2} "

        self.cell(196, 6, str(self.periode), 0, align="C", fill=True)

    def add_facture_header(self):
        self.set_line_width(0.5)
        self.set_xy(10, 60)
        self.set_font('myfont', 'B', 10)
        self.cell(35, 8, 'Client', 1, align="C")
        self.cell(27, 8, 'N° Facture', 1, align="C")
        self.cell(25, 8, 'Materiel', 1, align="C")
        self.cell(25, 8, "Main d'œuvre", 1, align="C")
        self.cell(25, 8, 'Avance', 1, align="C")
        self.cell(25, 8, 'Reste', 1, align="C")
        self.cell(25, 8, 'Total', 1, align="C")
        self.ln()

    def placer_dernieres_cellules(self):
        self.set_xy(6, self.get_y() + 10)
        self.set_font("myfont", "B", 10)

        self.cell(40, 8, 'Total Achat Matériel', 1, align="C")
        self.cell(40, 8, "Total Main d'oeuvre", 1, align="C")
        self.cell(40, 8, 'Total Avance Réçu', 1, align="C")
        self.cell(40, 8, 'Total Reste à Payer', 1, align="C")
        self.cell(40, 8, 'Montant Total', 1, align="C")
        self.ln()
        self.set_xy(6, self.get_y())
        self.set_font("myfont", "B", 12)
        self.cell(40, 8, str(self.montant_materiel), 1, align="C")
        self.cell(40, 8, str(self.montant_main_oeuvre), 1, align="C")
        self.cell(40, 8, str(self.avance), 1, align="C")
        self.cell(40, 8, str(self.reste), 1, align="C")
        self.cell(40, 8, str(self.Total), 1, align="C")

    def add_facture(self):
        self.set_font('myfont', '', 8, )
        self.set_xy(10, 68)
        self.set_line_width(0.3)
        for item in self.items:
            self.cell(35, 6, str(cut_string(item['client'],15)), 1)
            self.cell(27, 6, str(item['Num_Facture']), 1, align="C")
            self.cell(25, 6, item['Materiel'], 1, align="C")
            self.cell(25, 6, f"{item['Main_oeuvre']}", 1, align="C")

            self.cell(25, 6, f"{item['Montant_avance']}", 1, align="C")
            print(str(item['Reste'].strip()) =="0")
            if str(item['Reste'].strip()) =="0":
                print("entrer")
                self.set_text_color(106, 250, 24)
            else:
                self.set_text_color(255, 0, 0)
            self.cell(25, 6, f"{item['Reste']}", 1, align="C")
            self.set_text_color(0, 0, 0)
            self.cell(25, 6, f"{item['montant_ht']}", 1, align="C")

            self.ln()
        self.set_xy(100, self.get_y() + 5)
        self.set_font("myfont", "BI", 15)
        self.cell(180, 8, 'Résumé', 0, )

    def faire_PDF(self):
        self.add_page()
        self.set_header()
        self.add_facture_header()
        self.add_facture()
        if self.get_y() > 250:
            self.add_page()
            self.placer_dernieres_cellules()
        self.placer_dernieres_cellules()
        self.output(f"{self.save_directory}/{self.periode.replace('/', '_')}.pdf")

def gerer_float_numbre(number):
    number=float(number)
    if int(number)==number:
        return int(number)
    return number
def gerer_reglement_reste_payer(reste_payer,reglement):
    status=False
    try:
        if reste_payer-reglement <0:
            raise ValueError
        status=True
    except:
        pass
    return status


tem={"client":"Zongoœü,ê,ôûâèèàç","Num_Facture":"N°FP001/11/2024","Materiel":"1 500 000 000",
"Main_oeuvre":"150 000 000","Avance":"150 000 000","Reste":"150 000 000","montant_ht":"150 000 000"}

item1={"client":"Zongoœü,ê,ôûâèèàç","Num_Facture":"N°FP001/11/2024","Materiel":"1 500 000 000",
"Main_oeuvre":"150 000 000","Avance":"150 000 000","Reste":"0","montant_ht":"150 000 000"}


items=[]
for i in range(50):
    items.append(item1)
items=json.dumps(items)

"""bilan=Facture("FPN°001/12/2024","12/10/2024", "+226 6619083","ouagdougou",
            "frais de formation","50 000",items,
            "75 000","75 000","Frais de formation scolaire",
              "150 000","","","E:\pycharmProjects\gestion_devis")
bilan.produire_facture()"""



def gerer_montant_oeuvre_and_description(montant,description):
    status=False
    try:
        montant=float(montant)
    except:
        pass

    if status:
        if montant==0:
            pass
        if description:
            return True
        return False
    else:
        if description:
            return False
        return True

def get_value_for_modification(id_facture):
    connexion=connect("database.db")
    resultat=[]
    data=connexion.execute(f"""select Nom_client,
    Numero_telephone,
    Adresse_client,
    Nom_facture,
    Date,
    Nom_main_oeuvre ,
    Montant_main_oeuvre ,
    Montant_avance from data where Numero_facture='{id_facture}' """)
    item=connexion.execute(f"""select List_Materiels_achetes from data where Numero_facture='{id_facture}' """)
    data = data.fetchone()
    items=item.fetchone()[0]
    return data,items
# print(get_value_for_modification("N°FP006/11/2024"))
def update_facture_data(id_facture,data):
    connexion=connect("database.db")
    sql=f"""update data set Nom_client =?,
    Numero_telephone  =? ,
    Adresse_client =?,
    Nom_facture =?,
    Date =?,
    List_Materiels_achetes =?,
    Montant_achat_materiel =?,
    Montant_main_oeuvre =?,
    Nom_main_oeuvre =?,
    Montant_total =?,
    Montant_avance =?,
    Montant_reste  =?,
    Jour =?,
    Mois=?,
    Annee=? where Numero_facture='{id_facture}' """
    connexion.execute(sql,data)
    connexion.commit()
def cut_string(string:str,maxlen):
    if len(string.strip())<=maxlen:
        return string
    else:
        return string[:maxlen-len(string.strip())]+"..."

def ralentir_placement(width,step):
    resultat=[]
    for i in range(1,width,step):
        resultat.append(i)
    return resultat,resultat[::-1]
#print(cut_string("bonjour",4))
if 0 == 0:
    numero = "N° FP002_10_2024"
    client = "Ouedraogo"
    tel = "+226 25 30 75 30"
    adresse = "Bobo Dioulasso"

    # Liste des articles
    item = [
        {"reference": "convertisseur", 'qte': "1", 'unite': 'U', 'prix_unitaire': "16000", 'montant_ht': "1600000"}]
    items = []
    for i in range(5):
        for value in item:
            items.append(value)
    items = json.dumps(items)
    # Totaux
    total_achat = "630000"
    total_avance = "185000"
    reste_a_payer = "489000"
    total_ht = "815000"
    main_oeuvre = "45000"
    main_oeuvre_nom = "Main oeuvre pour la mise en reseau"

    facture_name = "Fourniture et installation d'un système de vidéosurveillance IP dans les locaux de SOGEPER"
    # Création du PDF
    pdf = Facture(total=total_ht, total_achat=total_achat, reste=reste_a_payer,
                  avance=total_avance, montant_main_oeuvre=main_oeuvre,
                  main_oeuvre_nom=main_oeuvre_nom,
                  client=client, tel=tel, facture_name=facture_name,
                  items=items, numero_facture=numero, date="10/11/2024",
                  addresse=adresse, directory_path="E:/pycharmProjects/gestion_devis")
    pdf.produire_facture()
