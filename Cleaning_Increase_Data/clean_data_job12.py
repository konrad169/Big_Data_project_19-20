import pandas as pd

col_list = ["ticker", "open", "close", "low", "high", "volume", "date"]
output = open('../Datasets/Clean/historical_stock_prices_job12.csv', 'w')

tile_df = pd.read_csv("../Datasets/Original/historical_stock_prices.csv", usecols=col_list)
indexNames_2008 = tile_df[tile_df['date'] < '2008'].index
indexNames_2018 = tile_df[tile_df['date'] > '2018-12-31'].index

tile_df.drop(indexNames_2008, inplace=True, axis=0)
tile_df.drop(indexNames_2018, inplace=True, axis=0)
tile_df.to_csv(r'../Datasets/Clean/historical_stock_prices_job12.csv', index=False, header=True)
