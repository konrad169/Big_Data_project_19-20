#!/usr/bin/env python

import sys

ANNO_START = 2008
ANNO_END = 2018

rangeValues = range(ANNO_START, ANNO_END + 1)

# VARIABILE PER SALTARE LA PRIMA RIGA
firstLine = True

for line in sys.stdin:

    # RIMUOVO LE RIGHE VUOTE
    if line == "":
        continue

    # SALTO LA PRIMA RIGA
    if firstLine:
        firstLine = False
        continue

    #CONVERTO OGNI RIGA IN UNA LISTA DI STRING
    input = line.strip().split(',')
    if len(input) == 8:
        ticker, _, close, _, low, high, volume, date = input


        if ticker != 'ticker':
            anno = int(date[0:4])
            #CONTROLLO CHE L'ANNO SIA TRA START & END
            if anno in rangeValues:
                print('{}\t{}\t{}\t{}\t{}\t{}'.format(ticker,
                                                      date,
                                                      close,
                                                      low,
                                                      high,
                                                      volume))
