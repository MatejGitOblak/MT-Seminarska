import pandas as pd
import dash
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import plotly.express as px
import json
import geojson
import math

def load_and_preprocess_odjemalci():
    df_odjemalci = pd.read_csv("data/podatki_vrsta_odjemalca.csv", delimiter=",", encoding="windows-1250")
    df_starost_prebivalcev = pd.read_csv("data/podatki_starost_prebivalcev.csv", delimiter=",", encoding="windows-1250")

    df_map_slovenija = gpd.read_file('slovenija_map/obcine/obcine.shp')
    df_map_slovenija = df_map_slovenija.to_crs("WGS84")
    df_map_slovenija = df_map_slovenija.rename({'NAZIV': 'District'}, axis = 'columns')
    df_map_slovenija = df_map_slovenija.drop(columns = ['EID_OBCINA',  'SIFRA', 'NAZIV_DJ', 'OZNAKA_MES', 'DATUM_SYS'])
    df_map_slovenija = df_map_slovenija.sort_values('District')
    df_map_slovenija = df_map_slovenija.reset_index(drop=True)

    df_odjemalci = df_odjemalci.drop(df_odjemalci.columns[[2,3,4,5,6,7,8,9,10,11,12,13,26,27,28,29,30,31,32,33,34]], axis=1)
    df_odjemalci["Poraba"] = df_odjemalci.iloc[:,2:14].sum(axis=1)
    df_odjemalci = df_odjemalci.drop(df_odjemalci.columns[[1,2,3,4,5,6,7,8,9,10,11,12,13]], axis=1)

    df_odjemalci_skupaj = df_odjemalci[3:-3:+3]
    df_odjemalci_gospodinjstva = df_odjemalci[4:-3:+3]
    df_odjemalci_industrija = df_odjemalci[5:-3:+3]
    df_starost_prebivalcev = df_starost_prebivalcev[1::]

    df_odjemalci_skupaj = df_odjemalci_skupaj.sort_values('OBČINE')
    df_odjemalci_gospodinjstva = df_odjemalci_gospodinjstva.sort_values('OBČINE')
    df_odjemalci_industrija = df_odjemalci_industrija.sort_values('OBČINE')
    df_starost_prebivalcev = df_starost_prebivalcev.sort_values('OBČINE')

    obcine = []
    for obcina in list(df_odjemalci_skupaj["OBČINE"]):
        if "/" in obcina:
            obcina = obcina.split("/")[0]
        obcine.append(obcina)

    df_odjemalci_skupaj["OBČINE"] = obcine
    df_odjemalci_gospodinjstva["OBČINE"] = obcine
    df_odjemalci_industrija["OBČINE"] = obcine
    df_starost_prebivalcev["OBČINE"] = obcine
    df_map_slovenija["District"] = obcine

    df_odjemalci_skupaj = df_odjemalci_skupaj.reset_index(drop=True)
    df_odjemalci_gospodinjstva = df_odjemalci_gospodinjstva.reset_index(drop=True)
    df_odjemalci_industrija = df_odjemalci_industrija.reset_index(drop=True)
    df_starost_prebivalcev = df_starost_prebivalcev.reset_index(drop=True)

    df_starost_prebivalcev.drop(['2020H1 Starost - SKUPAJ', '2020H2 Starost - SKUPAJ', '2021H1 Starost - SKUPAJ'], axis=1, inplace=True)
    df_starost_prebivalcev.rename(columns={'2021H2 Starost - SKUPAJ':'POPULACIJA'}, inplace=True)

    df_odjemalci_gospodinjstva_norm = pd.DataFrame({
                                                    'OBČINE': df_odjemalci_gospodinjstva['OBČINE'],
                                                    'Poraba': df_odjemalci_gospodinjstva["Poraba"]/df_starost_prebivalcev["POPULACIJA"]
                                                    })

    odjemalci_dict = {
        'skupaj': df_odjemalci_skupaj,
        'gospodinjstvo': df_odjemalci_gospodinjstva,
        'industrija': df_odjemalci_industrija,
        'gospodinjstvo_norm': df_odjemalci_gospodinjstva_norm,
        'df_map': df_map_slovenija
    }

    return odjemalci_dict

def load_and_preprocess_dejavnosti():
    df = pd.read_csv("data/podatki_dejavnosti.csv", delimiter=",", encoding="windows-1250")
    df = df.loc[(df["OBČINE"] != "SLOVENIJA") & (df["OBČINE"] != "Neznano") & (df['SKD DEJAVNOST'] != 'SKD Dejavnost - SKUPAJ') & (df['SKD DEJAVNOST'] != 'X Neznano')]
    dejavnosti = list(df["SKD DEJAVNOST"].unique())
    obcine = list(df['OBČINE'].unique())
    df = df.rename(columns={'2021 (začasni podatki)': 'Poraba'})
    dejavnosti_dict = {}
    
    for dejavnost in dejavnosti:
        df1 = df.loc[df["SKD DEJAVNOST"] == dejavnost].drop(columns=("SKD DEJAVNOST"))
        obcine = []
        for obcina in list(df1["OBČINE"]):
            if "/" in obcina:
                obcina = obcina.split("/")[0]
            obcine.append(obcina)
        df1["OBČINE"] = obcine
        if df1["Poraba"].sum() != 0:
            dejavnosti_dict[" ".join(dejavnost.split(" ")[1:])] = df1
    return dejavnosti_dict

def calculate_sums_dejavnosti(list_dejavnosti, dejavnosti_d):
    seznami = []
    for dejavnost in list_dejavnosti:
        seznami.append(list(dejavnosti_d[dejavnost]["Poraba"].values))
    return list(sum(map(np.array, np.array(seznami))))