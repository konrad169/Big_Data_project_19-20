#!/usr/bin/env python

import sys
import csv

ANNO_START = 2016
ANNO_END = 2018

rangeValues = range(ANNO_START, ANNO_END + 1)

tickerToCompanyNameMap = {}


with open('historical_stocks.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
# VARIABILE PER SALTARE LA PRIMA RIGA
    firstLine = True

    for row in csv_reader:
        if not firstLine:
            ticker, _, name, sector, _ = row
            if sector != 'N/A':
                tickerToCompanyNameMap[ticker] = name
        else:
            firstLine = False

for line in sys.stdin:
    #CONVERTO OGNI RIGA IN UNA LISTA DI STRING
    input = line.strip().split(',')
    if len(input) == 8:
        ticker, _, close, _, _, _, _, date = input
        if ticker != 'ticker':
            year = int(date[0:4])

            #CONTROLLO CHE L'ANNO SIA TRA START & END
            if year in rangeValues and ticker in tickerToCompanyNameMap:
                name = tickerToCompanyNameMap[ticker]
                print('{}\t{}\t{}\t{}'.format(name,
                                              ticker,
                                              date,
                                              close))
