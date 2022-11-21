import pandas as pd

df_dejavnosti = pd.read_csv("data/podatki_po_dejavnostih.csv", delimiter=",", encoding="windows-1250")
df_odjemalci = pd.read_csv("data/podatki_vrsta_odjemalca.csv", delimiter=",", encoding="windows-1250")


def izrisi_odjemalci_Slovenija(odjemalci, leto):
    df_odjemalci = odjemalci.copy()
    #Tukaj vzamemo samo podatke za VSE SKUPAJ porabo (brez gospodinjstva in poslovnih objektov)
    df = df_odjemalci[::+3]
    #Tukaj izbrišem podatke za SLOVENIJO in Neznano vrstice
    df = df[1:-1]
    #Priprava podatkov za uporabo
    df = df.drop("VRSTA ODJEMALCA", axis=1)
    obcine = {df["OBČINE"][i]:i for i in df.index}

    dict_porab = dict()
    if leto == 2020:
        vse_2020 = dict(df[df.columns[1:13]].sum(axis=1))
        dict_porab = dict([(k,[vse_2020[k]]) for k in vse_2020])
    elif leto == 2021:
        vse_2021 = dict(df[df.columns[13:25]].sum(axis=1))
        dict_porab = dict([(k,[vse_2021[k]]) for k in vse_2021]) 
    elif leto == 2022:
        vse_2022 = dict(df[df.columns[25:34]].sum(axis=1))
        dict_porab = dict([(k,[vse_2022[k]]) for k in vse_2022]) 

    #V koncem dictu so shranjene OBČINE (ključ) z vrednostmi, ki so LISTI, 
    # ki prikazujejo porabo za vsako občino za vsako leto posebaj
    koncni_dict = dict()
    for k,v in obcine.items():
        koncni_dict[k] = dict_porab[v]

    return pd.DataFrame.from_dict(koncni_dict)
