from csv import DictReader
import pandas as pd

def poraba_to_list(record):
    poraba_po_mesecih = []
    for key, value in record.items():
        if key != 'OBČINE' and key != 'SKD DEJAVNOST':
            poraba_po_mesecih.append(value)
    return poraba_po_mesecih[:24]

def izrisi_dejavnosti_obcine():

    data = list(DictReader(open('data/podatki_po_dejavnostih.csv', 'rt', encoding='windows-1250')))
    obcine = set()
    dejavnosti = set()
    for record in data:
        obcine.add(record['OBČINE'])
        dejavnosti.add(record['SKD DEJAVNOST'])

    dt_dejavnosti_obcine = dict()
    dt_obcine_poraba = dict()
    # 24 polj zacne se z januar 2020 konca z december 2021
    poraba_po_mesecih = []

    for dejavnost in dejavnosti:
        for obcina in obcine:
            for record in data:
                if record['OBČINE'] == obcina and record['SKD DEJAVNOST'] == dejavnost:
                    dt_obcine_poraba[obcina] = poraba_to_list(record)
        dt_dejavnosti_obcine[dejavnost] = dt_obcine_poraba
        dt_obcine_poraba = dict()

    # print(len(dt_dejavnosti_obcine.keys()))

    return pd.DataFrame.from_dict(dt_dejavnosti_obcine).transpose()