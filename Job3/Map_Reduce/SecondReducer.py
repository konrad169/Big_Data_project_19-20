#!/usr/bin/env python
import sys

#POSIZIONE CAMPI PER OGNI RIGA DA STDIN
PERCENTDIFF2016 = 0
PERCENTDIFF2017 = 1
PERCENTDIFF2018 = 2
NAME = 3


# VARIABILI GLOBALI
prevTriplettaVariazionePercent = None

companyList = []

#FUNZIONE PER SCRIVERE UN INSIEME DI COPPIE CHIAVE-VALORE
def writeRecord():

    if len(companyList) > 1:
        placeholders = '\t'.join(['{},'] * len(companyList) + ['2016: {}%'] + ['2017: {}%'] + ['2018: {}%'])
        arglist = companyList + list(prevTriplettaVariazionePercent)
        out = placeholders.format(*arglist)
        print(out)

#PARSING DEI VALORI IN VALUE LIST
def parseValues(valueList):
    percentChange2016 = valueList[PERCENTDIFF2016].strip()
    percentChange2017 = valueList[PERCENTDIFF2017].strip()
    percentChange2018 = valueList[PERCENTDIFF2018].strip()
    name = valueList[NAME].strip()
    return ((percentChange2016, percentChange2017, percentChange2018),
            name)


for line in sys.stdin:
    valueList = line.strip().split('\t')

    if len(valueList) == 4:
        TriplettaVariazionePercent, name = parseValues(valueList)

        if prevTriplettaVariazionePercent and prevTriplettaVariazionePercent != TriplettaVariazionePercent:
            # TRIPLETTA CAMBIATA
            writeRecord()

            # RESET VARIABILI GLOBALI
            prevTriplettaVariazionePercent = TriplettaVariazionePercent

            # RESET DIZIONARIO
            companyList = []

            #AGGIUNGO UNA NUOVA COMPAGNIA
            companyList.append(name)

        else:
            prevTriplettaVariazionePercent = TriplettaVariazionePercent

            companyList.append(name)

if prevTriplettaVariazionePercent:
    writeRecord()
