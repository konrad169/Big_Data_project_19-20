#!/usr/bin/env python
import sys

#POSIZIONE CAMPI PER OGNI RIGA
SECTOR = 0
TICKER = 1
DATE = 2
CLOSE = 3
VOLUME = 4


#VARIABILI GLOBALI
prevSector = None
prevTicker = None
prevYear = None
prevClose = 0


yearToSectorTrend = {}

yearToSectorDailyClosePrice = {}





#FUNZIONE PER SCRIVERE UN INSIEME DI COPPIE CHIAVE-VALORE
def writeRecord():
    for year in sorted(yearToSectorTrend.keys()):
        sectorTrend = yearToSectorTrend[year]
        sectorDailyClosePrices = yearToSectorDailyClosePrice[year]
        entireVolume = sectorTrend['entireVolume']
        countVolume = sectorTrend['countVolume']
        percentChange = (sectorTrend['closePriceFinalValue'] - sectorTrend['closePriceStartingValue']) / sectorTrend[
            'closePriceStartingValue']
        averageClosePrice = getDailyCloseAverage(sectorDailyClosePrices)
        annualMeanVolume = (entireVolume / countVolume)
        print('{}\t{}\t{}\t{}\t{}'.format(
            prevSector,
            year,
            annualMeanVolume,
            percentChange,
            averageClosePrice))



def getDailyCloseAverage(yearToDailyClosePriceMap):
    count = len(yearToDailyClosePriceMap.keys())
    closeSum = sum(yearToDailyClosePriceMap.values())
    return closeSum / count



def updateDataStructure(dataStructure, year, key, value):
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
    sector = valueList[SECTOR].strip()
    ticker = valueList[TICKER].strip()
    date = valueList[DATE].strip()
    close = float(valueList[CLOSE].strip())
    volume = int(valueList[VOLUME].strip())
    return (sector, ticker, date, close, volume)



for line in sys.stdin:
    valueList = line.strip().split('\t')

    if len(valueList) == 5:
        sector, ticker, date, close, volume = parseValues(valueList)
        year = date[0:4]

        if prevSector and prevSector != sector:

            updateDataStructure(yearToSectorTrend,
                                prevYear,
                                'closePriceFinalValue',
                                prevClose)
            writeRecord()

            # RESET DIZIONARI
            yearToSectorTrend = {}
            yearToSectorDailyClosePrice = {}


            updateDataStructure(yearToSectorTrend,
                                year,
                                'closePriceStartingValue',
                                close)


            updateDataStructure(yearToSectorTrend,
                                year,
                                'entireVolume',
                                volume)

            updateDataStructure(yearToSectorTrend,
                                year,
                                'countVolume',
                                1)

            updateDataStructure(yearToSectorDailyClosePrice,
                                year,
                                date,
                                close)

        else:

            updateDataStructure(yearToSectorTrend,
                                year,
                                'entireVolume',
                                volume)

            updateDataStructure(yearToSectorTrend,
                                year,
                                'countVolume',
                                1)

            updateDataStructure(yearToSectorDailyClosePrice,
                                year,
                                date,
                                close)


            if prevTicker and prevTicker != ticker:
                #TICKER DIFFERENTI

                updateDataStructure(yearToSectorTrend,
                                    prevYear,
                                    'closePriceFinalValue',
                                    prevClose)


                updateDataStructure(yearToSectorTrend,
                                    year,
                                    'closePriceStartingValue',
                                    close)

            else:
                #STESSO TICKER
                if not prevTicker:
                    prevTicker = ticker

                    updateDataStructure(yearToSectorTrend,
                                        year,
                                        'closePriceStartingValue',
                                        close)


                if prevYear and prevYear != year:
                    updateDataStructure(yearToSectorTrend,
                                        prevYear,
                                        'closePriceFinalValue',
                                        prevClose)

                    updateDataStructure(yearToSectorTrend,
                                        year,
                                        'closePriceStartingValue',
                                        close)

        # AGGIORNO I VALORI DELLE VARIABILI GLOBALI
        prevSector = sector
        prevTicker = ticker
        prevYear = year
        prevClose = close

if prevSector:
    updateDataStructure(yearToSectorTrend,
                        prevYear,
                        'closePriceFinalValue',
                        prevClose)
    writeRecord()
