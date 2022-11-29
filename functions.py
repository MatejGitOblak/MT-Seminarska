import pandas as pd

def izrisi_odjemalci_Slovenija(odjemalci, leto):
    df_odjemalci = odjemalci.copy()
    df=df_odjemalci[::+3]
    df = df[1:-1]
    df = df.drop("VRSTA ODJEMALCA", axis=1)
    obcine = {df["OBČINE"][i]:i for i in df.index}

    dict_porab = dict()
    if leto == 2020:
        vse_2020 = dict(df[df.columns[1:13]].sum(axis=1))
        dict_porab = dict([(k,[vse_2020[k]]) for k in vse_2020])
    elif leto == 2021:
        vse_2021 = dict(df[df.columns[13:25]].sum(axis=1))
        dict_porab = dict([(k,[vse_2021[k]]) for k in vse_2021])

    koncni_dict = dict()
    for k,v in obcine.items():
        koncni_dict[k] = dict_porab[v]
    
    return pd.DataFrame.from_dict(koncni_dict).transpose()


def izrisi_odjemalci_gospodinjstva(odjemalci, leto):
    df_odjemalci = odjemalci.copy()
    df=df_odjemalci[1::+3]
    df = df[1:-1]
    df = df.drop("VRSTA ODJEMALCA", axis=1)
    obcine = {df["OBČINE"][i]:i for i in df.index}

    dict_porab = dict()
    if leto == 2020:
        vse_2020 = dict(df[df.columns[1:13]].sum(axis=1))
        dict_porab = dict([(k,[vse_2020[k]]) for k in vse_2020])
    elif leto == 2021:
        vse_2021 = dict(df[df.columns[13:25]].sum(axis=1))
        dict_porab = dict([(k,[vse_2021[k]]) for k in vse_2021])

    koncni_dict = dict()
    for k,v in obcine.items():
        koncni_dict[k] = dict_porab[v]

    return pd.DataFrame.from_dict(koncni_dict).transpose()

def izrisi_odjemalci_poslovni_objekti(odjemalci, leto):
    df_odjemalci = odjemalci.copy()
    df=df_odjemalci[2::+3]
    df = df[1:-1]
    df = df.drop("VRSTA ODJEMALCA", axis=1)
    obcine = {df["OBČINE"][i]:i for i in df.index}

    dict_porab = dict()
    if leto == 2020:
        vse_2020 = dict(df[df.columns[1:13]].sum(axis=1))
        dict_porab = dict([(k,[vse_2020[k]]) for k in vse_2020])
    elif leto == 2021:
        vse_2021 = dict(df[df.columns[13:25]].sum(axis=1))
        dict_porab = dict([(k,[vse_2021[k]]) for k in vse_2021])

    koncni_dict = dict()
    for k,v in obcine.items():
        koncni_dict[k] = dict_porab[v]

    return pd.DataFrame.from_dict(koncni_dict).transpose()


def uredi_data_prebivalci(prebivalci_data, mapdf):
    df = prebivalci_data.copy()
    df = df.rename({'OBČINE': 'District'}, axis = 'columns')
    df = df.drop(df.index[0])

    df.index = mapdf.index
    df["District"] = mapdf["District"]

    df["2020_skupaj"] = ((df["2020H1 Starost - SKUPAJ"] + df["2020H2 Starost - SKUPAJ"]) / 2).astype(int)
    df["2021_skupaj"] = ((df["2021H1 Starost - SKUPAJ"] + df["2021H2 Starost - SKUPAJ"]) / 2).astype(int)
    df = df.drop(columns = ["2021H1 Starost - SKUPAJ",  '2021H2 Starost - SKUPAJ', '2020H1 Starost - SKUPAJ', '2020H2 Starost - SKUPAJ'])

    return df

def izracun_normalizacije_Slovenija(df, urejeni, mapdf):
    df.index = mapdf.index
    df.insert(0,'District', mapdf["District"])
    df["Normalizacija_2020"] = round(df[0] / urejeni["2020_skupaj"],2)
    df["Normalizacija_2021"] = round(df[0] / urejeni["2021_skupaj"],2)
    return df

def izracun_normalizacije_gospodinjstva(df, urejeni, mapdf):
    df.index = mapdf.index
    df.insert(0,'District', mapdf["District"])
    df["Normalizacija_2020"] = round(df[0] / urejeni["2020_skupaj"],2)
    df["Normalizacija_2021"] = round(df[0] / urejeni["2021_skupaj"],2)
    return df

def izracun_normalizacije_poslovni_objekti(df, urejeni, mapdf):
    df.index = mapdf.index
    df.insert(0,'District', mapdf["District"])
    df["Normalizacija_2020"] = round(df[0] / urejeni["2020_skupaj"],2)
    df["Normalizacija_2021"] = round(df[0] / urejeni["2021_skupaj"],2)
    return df