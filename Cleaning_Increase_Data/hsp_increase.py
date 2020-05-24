import pandas as pd
import os
import sys

workdir_path = os.path.join("../Datasets/Original")
workdir_path1=os.path.join("./Dataset/Increased")
input_filename = "historical_stock_prices.csv"
input_file_path = os.path.join(workdir_path, input_filename)
iterations = 3

if len(sys.argv) > 1:
    iterations = int(sys.argv[1])

output_filename = input_filename.split(".")[0]+"_"+str(iterations)+"x."+input_filename.split(".")[1]

output_file_path = os.path.join(workdir_path1, output_filename)


""" Augment File """
hsp = pd.read_csv(input_file_path)
dataframes = [hsp]
i = 1
while i <= iterations:
    pd2 = pd.DataFrame.copy(hsp)
    #pd2["ticker"] += i*len(hs)
    dataframes.append(pd2)
    i += 1

conc = pd.concat(dataframes, ignore_index=True)
conc.to_csv(output_file_path, index=False, sep=",", line_terminator="\n")
