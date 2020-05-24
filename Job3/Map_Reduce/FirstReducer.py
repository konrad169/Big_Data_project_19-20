#!/usr/bin/env python
import sys
import csv

#POSIZIONE CAMPI PER OGNI RIGA
NAME = 0
TICKER = 1
DATE = 2
CLOSE = 3

ANNO_START = 2016
ANNO_END = 2018

LUNGHEZZA_RECORD = 4

rangeValues = list(range(ANNO_START, ANNO_END + 1))

#VARIABILI GLOBALI
prevName = None
prevTicker = None
prevYear = None
prevClose = None

yearToCompanyTrend = {}





#FUNZIONE PER SCRIVERE UN INSIEME DI COPPIE CHIAVE-VALORE
def writeRecord():
    if all(str(year) in yearToCompanyTrend for year in rangeValues):
        yearToCompanyTrendKeys = yearToCompanyTrend.keys()
        listOfSquareBrackets = ['{}'] * len(yearToCompanyTrendKeys) + ['{}']

        formattedString = '\t'.join(listOfSquareBrackets)


        percentChangeMap = {year: None for year in yearToCompanyTrendKeys}

        for year in sorted(yearToCompanyTrend.keys()):
            companyTrendYear = yearToCompanyTrend[year]
            closePriceFinalValue = companyTrendYear['closePriceFinalValue']
            closePriceStartingValue = companyTrendYear['closePriceStartingValue']
            closeDifference = closePriceFinalValue - closePriceStartingValue
            percentChange = closeDifference / closePriceStartingValue
            percentChangeMap[year] = int(round(percentChange * 100))

        sortedPercentChangeMapKeys = sorted(percentChangeMap)
        sortedPercentChangeMapValues = [percentChangeMap[year] for year
                                        in sortedPercentChangeMapKeys]


        sortedPercentChangeMapValues.append(prevName)
        print(formattedString.format(*(sortedPercentChangeMapValues)))



def updateCompanyTrend(dataStructure, year, key, value):
    if year in dataStructure:
        if key in dataStructure[year]:
            dataStructure[year][key] += value
        else:
            dataStructure[year][key] = value
    else:
        dataStructure[year] = {}
        dataStructure[year][key] = value


#PARSING DEI VALORI IN VALUE LIST
def parseValues(valueList):
    name = valueList[NAME].strip()
    ticker = valueList[TICKER].strip()
    year = valueList[DATE].strip()[0:4]
    close = float(valueList[CLOSE].strip())
    return (name, ticker, year, close)






for line in sys.stdin:
    valueList = line.strip().split('\t')

    if len(valueList) == LUNGHEZZA_RECORD:
        name, ticker, year, close = parseValues(valueList)

        if prevName and prevName != name:

            updateCompanyTrend(yearToCompanyTrend,
                               prevYear,
                               'closePriceFinalValue',
                               prevClose)
            writeRecord()

            # RESET DIZIONARI
            yearToCompanyTrend = {}


            updateCompanyTrend(yearToCompanyTrend,
                               year,
                               'closePriceStartingValue',
                               close)

        else:

            if prevTicker and prevTicker != ticker:
                    #TICKER DIFFERENTI
                updateCompanyTrend(yearToCompanyTrend,
                                   prevYear,
                                   'closePriceFinalValue',
                                   prevClose)

                # this also means that the current close value is the first
                # close value for this ticker in this year
                updateCompanyTrend(yearToCompanyTrend,
                                   year,
                                   'closePriceStartingValue',
                                   close)

            else:
                #STESSO TICKER
                if prevYear and prevYear != year:
                    #ANNI DIVERSI
                    updateCompanyTrend(yearToCompanyTrend,
                                       prevYear,
                                       'closePriceFinalValue',
                                       prevClose)


                    updateCompanyTrend(yearToCompanyTrend,
                                       year,
                                       'closePriceStartingValue',
                                       close)
                else:
                    #ANNI UGUALI
                    if not prevYear:
                        updateCompanyTrend(yearToCompanyTrend,
                                           year,
                                           'closePriceStartingValue',
                                           close)

        # RESET VARIABILI GLOBALI
        prevName = name
        prevTicker = ticker
        prevYear = year
        prevClose = close


if prevName:
    updateCompanyTrend(yearToCompanyTrend,
                       prevYear,
                       'closePriceFinalValue',
                       prevClose)
    writeRecord()
