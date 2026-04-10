import random, rich
from datetime import datetime, timedelta, date
from rich.console import Console
from rich.table import Table

AREA=600

PZ_X_KG_SEMINA=800
PZ_X_KG_MEZZANA=180
PZ_X_KG_GROSSA=100

GG_RACC_SEMINA=130
GG_RACC_MEZZANA=420
GG_RACC_GROSSA=600

SEME_4=20000
SEME_6=10000
SEME_8=5000


# Funzione che, fornita in ingresso l'area della concessione in ettari, restituisce un dizionario contenente
# la dimensione delle zone per le tre produzioni richieste in input all'utente
def div_vivaio (concessione):                   
    valido=False
    while not valido:
        p_sem=float(input("Inserire percentuale di vivaio da adibire a contivazione semina (min 10%-max 25%)\t"))
        if 10<=p_sem<=25:
            valido=True
        else:
            print("Area inserita non congrua, inserisci nuovamente")
    dim_sem=(concessione/100)*p_sem
    valido=False
    while not valido:
        p_gros=float(input("Inserire percentuale di vivaio da adibire a produzione Vongola taglia grossa (min 10%-max 30%)\t" ))
        if 10<=p_gros<=30:
            valido=True
        else:
            print("Area inserita non congrua, inserisci nuovamente")     
    dim_gros=(concessione/100)*p_gros
    dim_mezz=concessione-(dim_sem+dim_gros)
    print()
    print("Dimensione area adibita produzione di semina =",dim_sem,"Ha")
    print()
    print("Dimensione area adibita a produzione vongola mezzana =",dim_mezz,"Ha")
    print()
    print("Dimensione area adibita a produzione vongola grossa =",dim_gros,"Ha\n")
    print()
    divisione_vivaio={"Semina":dim_sem, "Mezzana":dim_mezz, "Grossa":dim_gros}
    return divisione_vivaio     


# Funzione che in ingresso viene fornita la coppia chiave (tipologia prodotto), valore (dimenzione vivaio) e
# vengono popolati gli attributi dell'oggetto restituendo la lista relativa al vivaio
def crea_vivaio(chiave, valore, sigla): 
    campi_vivaio=dividi_campo(valore)
    campi_vivaio_arr=[round(valore, 2) for valore in campi_vivaio]  
    print()     
    print("L'area per il prodotto",chiave, "è divisa in:",+len(campi_vivaio_arr),"campi")
    print()
    print("La dimensione in ettari dei",len(campi_vivaio_arr),"campi è",campi_vivaio_arr)
    print()
    vivaio=[]
    cod_campo=[str(n).zfill(3) for n in random.sample(range(1, 600),len(campi_vivaio))]
    for i in range(len(campi_vivaio)):
        in_mq=int(round(campi_vivaio[i]*10000))
        quantita=popola_campo(in_mq)
        imp_data=data_semina(chiave)
        id_campo=sigla+cod_campo[i]
        campo=Campo(imp_data, quantita, in_mq, id_campo)
        vivaio.append(campo)
    return vivaio


# Funzione che crea i vivai e stampa le tabelle relative alla composizione dei vivai
def stampa_tabella_vivaio(console, nome, sigla, area_dati, colore):
    valore = area_dati[nome]
    vivaio = crea_vivaio(nome, valore, sigla)
    table = Table(title=f"[bold underline {colore}]VIVAIO {nome.upper()}[/bold underline {colore}]")
    table.add_column("Id Campo", header_style=f"bold {colore}", style="white", justify="left")
    table.add_column("Data semina", header_style=f"bold {colore}", style="white", justify="center")
    table.add_column("Dimensione campo mq", header_style=f"bold {colore}", style="white", justify="right")
    table.add_column("Quantità numero pezzi seminati", header_style=f"bold {colore}", style="white", justify="right")
    for obj in vivaio:
        table.add_row(str(obj.get_codice_campo()), str(obj.get_data_semina()), str(obj.get_dimensione()), str(obj.get_quantita()))
    console.print(table)
    return(vivaio)
    print("\n")


# Funzione che in ingresso viene data la dimensione in ettari della zona per la produzione di un prodotto, viene restituita 
# una lista con la dimensione in ettari dei campi creati randon (dimensione min Ha 1,5 max Ha5)
def dividi_campo(dim_campo):
    vivaio=list()
    campo=0
    while dim_campo>0:
        campo=random.uniform(1.5, 5)
        vivaio.append(campo)
        dim_campo-=campo
        if dim_campo<5:
            vivaio.append(dim_campo)
            dim_campo=0
    return vivaio


# Funzione che in ingresso entra la dimensione di un campo in mq, viene restituito un intreo relativo al numero 
# di pezzi di prodotto seminati (random min 500 max 600 x mq)
def popola_campo(dim_campo_mq):        
     n_pezzi=random.randint(500, 600)*dim_campo_mq
     return n_pezzi


# Funzione che imposta la data random di semina di un campo con in ingresso la tipologa del campo.Per i tre prodotti
# il l'intervallo massimo non può superare il periodo di raccolta differente per tipologia di prodotto
def data_semina(tipo_vivaio):
    if tipo_vivaio=="Semina":
        limite_min=60
        limite_max=180
    elif tipo_vivaio=="Mezzana":
        limite_min=200
        limite_max=548
    elif tipo_vivaio=="Grossa":
        limite_min=365
        limite_max=780
    giorni_random=random.randint(limite_min, limite_max)
    oggi=datetime.now()
    data_semina_campo=oggi-timedelta(days=giorni_random) 
    data_semina_campo=data_semina_campo.strftime("%d-%m-%Y")
    return data_semina_campo


# Oggetto relativo ad un campo per produzione di vongola verace
class Campo:

    def __init__(self, data_semina, quantita, dimensione,codice_campo):
        self.data_semina=data_semina
        self.quantita=quantita
        self.dimensione=dimensione
        self.codice_campo=codice_campo

    def get_data_semina(self):
        return self.data_semina
    
    def get_quantita(self):
        return self.quantita
    
    def get_dimensione(self):
        return self.dimensione
    
    def get_codice_campo(self):
        return self.codice_campo
          
    def __str__(self):
        return f"Id Campo: {self.codice_campo}\t Data semina: {self.data_semina}\t Dimensione campo mq: {self.dimensione}\t Quantità numero pezzi seminati: {self.quantita}"   
        
    
# Funzione che calcola la resa in kg. di un vivaio considerando una resa random pari al 70-80% su quanto seminato    
def resa_vivaio(vivaio, pz_kg):
    tot_kg=0
    for obj in vivaio:
        resa_campo_p=(obj.quantita/100)*random.randint(70, 80)
        resa_kg=resa_campo_p/pz_kg
        tot_kg+=resa_kg
    return tot_kg    


# Funzione che calcola la resa media per ettaro di vivaio per ogni prodotto contivato
def stima_resa_media(viv_1, viv_2, viv_3, area_div):
    pezzi_x_kg=[PZ_X_KG_SEMINA, PZ_X_KG_MEZZANA, PZ_X_KG_GROSSA]
    vivai = [viv_1, viv_2, viv_3]
    for (chiave, ettari), viv, c in zip(area_div.items(), vivai, pezzi_x_kg):
        totale_kg = sum(obj.quantita for obj in viv) / c
        resa_media = round(totale_kg / ettari, 2)
        resa_media = round((resa_media / 100)*75, 2)
        print(f"La stima di produzione media per ettaro del vivaio {chiave} di dimensione {ettari} ettari è di Kg.: {resa_media}")        
        print()


# Funzione che calcola la quantità in pezzi di prodotto disponibile in base alla data di semina        
def calcola_disponibilità_prodotto(vivaio, gg):
    oggi=datetime.now().date()
    disp_quantita=0
    for obj in vivaio:
        data_semina_obj=datetime.strptime(obj.data_semina, "%d-%m-%Y").date()
        if (oggi-data_semina_obj).days>=gg:
            disp_quantita+=obj.quantita
    disp_quantita = round((disp_quantita / 100)*75, 2)        
    return disp_quantita
         

# Funzione che restituisce il codice identificativo di un campo nel quanle è possibile pescare, alla data odierna, prodotto disponibile in base alla data di semina
def estrai_campi_disponibilità(viv, gg, pz):
    oggi = datetime.now().date()
    risultati = [] 
    for obj in viv:
        data_semina_obj = datetime.strptime(obj.data_semina, "%d-%m-%Y").date()
        if (oggi - data_semina_obj).days >= gg:
            disp_kg = round((obj.quantita / pz), 2)
            disp_kg = round((disp_kg / 100)*75, 2) 
            campo_dati = {"codice_campo": obj.codice_campo, "quantita": disp_kg}
            risultati.append(campo_dati)  
    return risultati


# Funzione che calcola la semina necessaria in base alla dimensione del campo
def calcola_semina(viv_1, viv_2, viv_3, seme):
    semina_nec={} 
    semi={"4": SEME_4, "6": SEME_6, "8": SEME_8}
    if seme in semi:
        semina=semi[seme]
        vivai=[viv_1, viv_2, viv_3]
        for vivaio in vivai:
            for obj in vivaio:
                semina_nec[obj.codice_campo]=round((obj.quantita/semina), 2)
    return semina_nec


# Funzione che, inserito un codice campo, restituisce i kg. di semina necessari per diversa tipologia
def calcola_semina_campo(vivaio_semina, vivaio_mezzana, vivaio_grossa, cod):
    cod = cod.strip().upper()
    sigla = cod[0]
    if sigla == "S":
        vivaio_target = vivaio_semina
    elif sigla == "M":
        vivaio_target = vivaio_mezzana
    elif sigla == "G":
        vivaio_target = vivaio_grossa
    else:
        print(f"Errore: Il codice {cod} non inizia con S, M o G.")
        return
    trovato = False
    for obj in vivaio_target:
        if obj.codice_campo.strip().upper() == cod:
            print(f"\n--- Risultati per il campo {cod} ---")
            print()
            print(f"Seme 4 mm. = KG. {round(obj.quantita / SEME_4, 2)}")
            print()
            print(f"Seme 6 mm. = KG. {round(obj.quantita / SEME_6, 2)}")
            print()
            print(f"Seme 8 mm. = KG: {round(obj.quantita / SEME_8, 2)}")
            print()
            trovato = True
            break
    if not trovato:
        print(f"Attenzione: Il codice {cod} non è stato trovato nel vivaio {sigla}.")


#Funzione che, inserendo quantità di prodotto da pescare, aggiorna i dati del vivaio      
def raccolta_prodotto(vivaio, pz, gg):
    try:
        kg_da_raccogliere = float(input("Inserisci quantità in kg da raccogliere: "))
        print()
    except ValueError:
        print("Errore: Inserisci un numero valido!")
        return
    disponibilita = estrai_campi_disponibilità(vivaio, pz, gg)
    if not disponibilita:
        print("Nessun campo disponibile.")
        return
    rimanenza = 0
    quota_per_campo = round(kg_da_raccogliere / len(disponibilita), 2)
    risultato_finale = {} 
    for obj in disponibilita:
        nome = obj["codice_campo"]
        valore = obj["quantita"]
        if valore >= quota_per_campo:
            nuova_disp = round(valore - quota_per_campo, 2)
        else:
            nuova_disp = 0
            rimanenza += round(quota_per_campo - valore, 2)
        risultato_finale[nome] = {"iniziale": valore, "attuale": nuova_disp}
    return risultato_finale, rimanenza


# Funzione che gestisce la rimanenza di prodotto pescato in presenza di campi disponibilità inferiore alla quota attribuita
def gestisci_rimanenza(risultato_finale, rimanenza):
    while rimanenza > 0.001:
        campi_con_disponibilita = [nome for nome, dati in risultato_finale.items() if dati["attuale"] > 0]
        if not campi_con_disponibilita:
            print()
            print(f"Attenzione: Rimanenza di {rimanenza:.2f} kg non prelevabile (prodotto esaurito).")
            print()
            break
        quota_extra = round(rimanenza / len(campi_con_disponibilita), 2)
        if quota_extra == 0:
            quota_extra = rimanenza
        for nome in campi_con_disponibilita:
            disponibile = risultato_finale[nome]["attuale"]
            prelievo = min(disponibile, quota_extra)
            risultato_finale[nome]["attuale"] = round(disponibile - prelievo, 2)
            rimanenza -= prelievo
            rimanenza = round(rimanenza, 2)
            if rimanenza <= 0:
                break
    return risultato_finale, round(rimanenza, 2)
     

# Funzione che restituisce la stampa ordinata della tabella successiva al raccolto
def mostra_tabella_raccolta(dati_raccolta):
    console = Console()
    table = Table(title="[bold underline yellow]DISPONIBILITA' CAMPI RIMASTA DOPO RACCOLTA[/bold underline yellow]")
    table.add_column("ID CAMPO", header_style="bold yellow", style="white")
    table.add_column("DISPONIBILITA' INIZIALE KG.", header_style="bold yellow", justify="right")
    table.add_column("DISPONIBILITA' FINALE KG.", header_style="bold yellow", justify="right")
    for id_campo, dati in dati_raccolta.items():
        table.add_row(str(id_campo), f"{dati['iniziale']:.2f}", f"{dati['attuale']:.2f}")
    console.print(table)


def main():

    console=Console()
    print("La concessione a disposizione per la produzione è pari a 600 ettari")
    print()

    area_divisa=div_vivaio(AREA)

    categorie = [{"nome": "Semina", "sigla": "S", "colore": "cyan"}, {"nome": "Mezzana", "sigla": "M", "colore": "green"}, {"nome": "Grossa", "sigla": "G", "colore": "red"}]
    #risultati_vivaio = {}
    #for obj in categorie:
       # risultati_vivaio[obj["nome"]] = stampa_tabella_vivaio(console, obj["nome"], obj["sigla"], area_divisa, obj["colore"]) 
    vivaio_semina = stampa_tabella_vivaio(console, "Semina", "S", area_divisa, "green")
    vivaio_mezzana = stampa_tabella_vivaio(console, "Mezzana", "M", area_divisa, "yellow")
    vivaio_grossa = stampa_tabella_vivaio(console, "Grossa", "G", area_divisa, "red")
    print() 

    while True:
        print("--- SCELTA OUTPUT ---")
        print("1.   Stima resa totale vivaio")
        print("2.   Stima resa media per ettaro")
        print("3.   Calcolo quantità di prodotto disponibile per tipologia")
        print("4.   Estrai campi con disponibilità prodotto")
        print("5.   Calcola semina vivai")
        print("6.   Calcola semina campo")
        print("7.   Esegui raccolta prodotto")
        print("8.   Esci")
        scelta_input = input("\n Inserire la scelta: ")
        try:
            scelta = int(scelta_input)
        except ValueError:
            print("\nERRORE: Devi inserire un numero da 1 a 8, non caratteri differenti!")
            print()
            continue  
        if 1<=scelta<=8:    
            if scelta==1:
                    vivaio_map = {"s": (vivaio_semina, PZ_X_KG_SEMINA, "per semina"), "m": (vivaio_mezzana, PZ_X_KG_MEZZANA, "mezzana"), "g": (vivaio_grossa, PZ_X_KG_GROSSA, "grossa")}
                    while True:
                        viv = input("\nInserisci il vivaio di cui vuoi conoscere la stima della resa. Digita S (Semina), M (Mezzana), G (Grossa) o X per uscire: ").lower()
                        if viv == "x":
                            break
                        if viv in vivaio_map:
                            vivaio, pz_kg, etichetta = vivaio_map[viv]
                            resa = resa_vivaio(vivaio, pz_kg)
                            print(f"La resa stimata del vivaio di produzione vongola {etichetta} è Kg. {resa:.2f}")
                            if input("\nVuoi inserire una nuova scelta? (s/n): ").lower() != "s":
                                break
                        else:
                            print("Scelta errata, riprova!")

            elif scelta==2:
                stima_resa=stima_resa_media(vivaio_semina, vivaio_mezzana, vivaio_grossa, area_divisa)
                print()
            elif scelta==3:
                categorie_vongole = [{"tipo": "semina", "vivaio": vivaio_semina, "gg": GG_RACC_SEMINA, "pz_kg": PZ_X_KG_SEMINA}, 
                                     {"tipo": "vongola mezzana", "vivaio": vivaio_mezzana, "gg": GG_RACC_MEZZANA, "pz_kg": PZ_X_KG_MEZZANA}, 
                                     {"tipo": "vongola grossa", "vivaio": vivaio_grossa, "gg": GG_RACC_GROSSA, "pz_kg": PZ_X_KG_GROSSA}]
                for cat in categorie_vongole:
                    disp = calcola_disponibilità_prodotto(cat["vivaio"], cat["gg"])
                    kg = round(disp / cat["pz_kg"], 2)
                    print()
                    print(f"Alla data odierna la disponibilità di prodotto {cat['tipo']} è per kg {kg}")
                    print()

            elif scelta==4:
                categorie = [{"vivaio": vivaio_semina, "gg": GG_RACC_SEMINA, "pz": PZ_X_KG_SEMINA, "nome": "SEMINA", "colore": "yellow"},
                             {"vivaio": vivaio_mezzana, "gg": GG_RACC_MEZZANA, "pz": PZ_X_KG_MEZZANA, "nome": "VONGOLA MEZZANA", "colore": "cyan"},
                             {"vivaio": vivaio_grossa, "gg": GG_RACC_GROSSA, "pz": PZ_X_KG_GROSSA, "nome": "VONGOLA GROSSA", "colore": "medium_orchid"}]

                for cat in categorie:
                    disponibilita = estrai_campi_disponibilità(cat["vivaio"], cat["gg"], cat["pz"])
                    print(f"\nL'elenco dei campi con disponibilità di prodotto {cat['nome'].lower()} alla data odierna è:\n")
                    table = Table(title=f"[bold underline {cat['colore']}]PRODOTTO DI {cat['nome']} DISPONIBILE PER CAMPO[/bold underline {cat['colore']}]")
                    table.add_column("ID CAMPO", header_style=f"bold {cat['colore']}", style="white", justify="left")
                    table.add_column("KG. PRODOTTO DISPONIBILE", header_style=f"bold {cat['colore']}", style="white", justify="right")
                    visti = set()
                    for obj in disponibilita:
                        codice = obj["codice_campo"]
                        if codice not in visti:
                            table.add_row(str(codice), str(obj["quantita"]))
                            visti.add(codice)
                    console.print(table)
                print()
                
            elif scelta==5:
                while True:
                    print("\n--- OPZIONI SEME ---")
                    print("Indicare la taglia di seme da utilizzare 4 mm., 6 mm. o 8 mm. (digita  '0' per uscire)")
                    tipo_seme = input("Tipo di seme: ")
                    print()
                    if tipo_seme == "0":
                        break
                    if tipo_seme in ["4", "6", "8"]:
                        semina_necessaria = calcola_semina(vivaio_semina, vivaio_mezzana, vivaio_grossa, tipo_seme)
                        table = Table(show_header=True, header_style="bold white on blue")
                        table.add_column("CODICE CAMPO", justify="left", width=10)
                        table.add_column("KG SEMINA", justify="right", width=10)
                        for codice, valore in semina_necessaria.items():
                            table.add_row(codice, f"{valore:.2f}")
                        console.print(table)
                        if input("\nVuoi ricalcolare con un nuovo seme? (s/n): ").lower() != "s":
                            break
                    else:
                        print("Opzione non valida! Riprova.")  

            elif scelta==6:
                    cod = input("Inserisci il campo di cui vuoi conoscere la quantità di semina necessaria:\t")
                    calcola_semina_campo(vivaio_semina, vivaio_mezzana, vivaio_grossa, cod)
                      
            elif scelta==7:
                while True:
                    scegli=input("Inserisci il prodotto da pescare S / M / G: (X pr uscire)  ") 
                    print()
                    opzioni = {"S":(vivaio_semina,GG_RACC_SEMINA, PZ_X_KG_SEMINA), "M":(vivaio_mezzana, GG_RACC_MEZZANA, PZ_X_KG_MEZZANA), "G":(vivaio_grossa, GG_RACC_GROSSA, PZ_X_KG_GROSSA)}
                    tasto = scegli.upper()
                    if scegli == "X" or scegli == "x":
                        break
                    if tasto in opzioni:
                        vivaio, gg, pz =opzioni[tasto]
                        raccolta, rimanenza=raccolta_prodotto(vivaio, gg, pz)
                        mostra_tabella_raccolta(raccolta)
                        if rimanenza==0:
                            break
                        else:
                            print()
                            print("Non è stata raggiunta la quota da raccogliere, è necessario suddividere la rimanenza da raccogliere su campi che hanno ancora disponibiltà di prodotto")
                            print()
                            risultato, rimanenza = gestisci_rimanenza(raccolta, rimanenza)
                            mostra_tabella_raccolta(risultato)
                    else:
                        print("Opzione non valida! Riprova.")
                
            elif scelta==8:
                print("Uscita dalla procedura, saluti")
                break
        else:
                print()
                print("Opzione non valida, inserisci nuovamente scelta")
main()