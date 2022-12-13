from csv import DictReader
import pandas as pd


def skupna_poraba_obcine(record):
    poraba = 0
    for key, value in record.items():
        if key != 'OBČINE' and key != 'SKD DEJAVNOST' and value != 'z' and value != 'N':
            if value == 'N':
                print("neki")
            poraba += int(value)
    return poraba

data = list(DictReader(open('data/podatki_po_dejavnostih.csv', 'rt', encoding='windows-1250')))
obcine = set()
dejavnosti = set()
for record in data:
    #if record['OBČINE'] != 'Slovenija' and record['OBČINE'] != 'Neznano':

    if "/" in record["OBČINE"]:
        obcine.add(record['OBČINE'].split("/")[0])
    else:
        obcine.add(record['OBČINE'])
    dejavnosti.add(record['SKD DEJAVNOST'])

dejavnosti_obcine = dict()
# 24 polj zacne se z januar 2020 konca z december 2021
poraba_po_mesecih = []
obcine = sorted(list(obcine))
dejavnosti = sorted(list(dejavnosti))

dejavnosti_obcine["OBČINE"] = obcine
for dejavnost in dejavnosti:
    poraba_po_obcinah = []
    for obcina in obcine:
        dejavnost_je_v_obcini = False
        for record in data:
            if record['OBČINE'] == obcina and record['SKD DEJAVNOST'] == dejavnost:
                dejavnost_je_v_obcini = True
                poraba_po_obcinah.append(skupna_poraba_obcine(record))
        if not dejavnost_je_v_obcini:
            poraba_po_obcinah.append(0)
    dejavnosti_obcine[dejavnost] = pd.DataFrame(list(zip(obcine, poraba_po_obcinah)), columns =['Občina', 'Poraba'])
    poraba_po_obcinah = []

    print(dejavnost)
    print("---------------------")

    print(dejavnosti_obcine[dejavnost])
    print("---------------------")
    print()
    print()

