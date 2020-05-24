#!/usr/bin/env python

import sys
import csv

annoStart = 2008
annoEnd = 2018

rangeValues = range(annoStart, annoEnd + 1)

tickerToSectorMap = {}

with open('historical_stocks.csv') as csv_file:

    csv_reader = csv.reader(csv_file, delimiter=',')
    firstLine = True

    for row in csv_reader:
        if not firstLine:
            ticker, _, _, sector, _ = row
            if sector != 'N/A':
                tickerToSectorMap[ticker] = sector
        else:
            firstLine = False

for line in sys.stdin:
    #CONVERTO OGNI RIGA IN UNA LISTA DI STRING
    input = line.strip().split(',')
    if len(input) == 8:
        ticker, _, close, _, _, _, volume, date = input
        if ticker != 'ticker':
            year = int(date[0:4])

            #CONTROLLO CHE L'ANNO SIA TRA START & END
            if year in rangeValues and ticker in tickerToSectorMap:
                sector = tickerToSectorMap[ticker]
                print('{}\t{}\t{}\t{}\t{}'.format(sector, ticker, date, close, volume))
