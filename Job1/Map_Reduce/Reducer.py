#!/usr/bin/env python

import sys
from datetime import datetime

#POSIZIONE CAMPI PER OGNI RIGA
TICKER = 0
DATE = 1
CLOSE = 2
LOW = 3
HIGH = 4
VOLUME = 5

#NUMERO DI RIGHE DA STAMPARE IN OUTPUT
TOP_N = 10

#VARIABILI GLOBALI
output = []
ticker_precedente = None
closePriceStartingValue = None
anno_inizio = None
closePriceFinalValue = None
lastAnno = None
minLowPrice = sys.maxsize
maxHighPrice = - sys.maxsize
sommaVolume = 0
contatoreVolume = 0


#FUNZIONE PER INSERIRE I DATI IN OUTPUT
def insertItemToLista():
    differenzeClose = closePriceFinalValue - closePriceStartingValue
    percentageChange = differenzeClose / closePriceStartingValue
    avgVolume = sommaVolume / contatoreVolume

    record = {'ticker': ticker_precedente,
              'percentageChange': percentageChange * 100,
              'minLowPrice': minLowPrice,
              'maxHighPrice': maxHighPrice,
              'avgVolume': avgVolume
              }

    output.append(record)


#PARSING DEI VALORI IN VALUE LIST
def parseValues(valueList):
    ticker = valueList[TICKER].strip()
    year = valueList[DATE].strip()[0:4]
    close = float(valueList[CLOSE].strip())
    low = float(valueList[LOW].strip())
    high = float(valueList[HIGH].strip())
    volume = float(valueList[VOLUME].strip())
    return [ticker, year, close, low, high, volume]



for line in sys.stdin:
    valueList = line.strip().split('\t')

    if len(valueList) == 6:
        ticker, year, close, low, high, volume = parseValues(valueList)

        #CASO IN CUI NEL MAPPER CONSIDERO UN TICKER DIVERSO DA QUELLO PRECEDENTE
        if ticker_precedente and ticker_precedente != ticker:
            #SE IL TICKER CAMBIA LO METTO IN valueList

            insertItemToLista()

            #AGGIORNO VARIABILI GLOBALI
            closePriceStartingValue = close
            firstYear = year
            closePriceFinalValue = close
            lastAnno = year
            minLowPrice = low
            maxHighPrice = high
            sommaVolume = volume
            contatoreVolume = 1

        # CASO IN CUI NEL MAPPER CONSIDERO LO STESSO TICKER
        else:

            if not ticker_precedente:
                closePriceStartingValue = close
                firstYear = year

            # AGGIORNO I VALORI PER IL TICKER PRECEDENTE
            closePriceFinalValue = close
            lastAnno = year
            minLowPrice = min(minLowPrice, low)
            maxHighPrice = max(maxHighPrice, high)
            sommaVolume += volume
            contatoreVolume += 1

        ticker_precedente = ticker

#AGGIUNGO L'ULTIMO TICKER ELABORATO IN LISTA
if ticker_precedente:
    insertItemToLista()

listaOrdinata = sorted(output, key=lambda k: k['percentageChange'], reverse=True)

# STAMPO LA LISTA ORDINATA
for i in range(TOP_N):
    item = listaOrdinata[i]
    print('{}\t{}%\t{}\t{}\t{}'.format(item['ticker'],
                                       item['percentageChange'],
                                       item['minLowPrice'],
                                       item['maxHighPrice'],
                                       item['avgVolume']))
