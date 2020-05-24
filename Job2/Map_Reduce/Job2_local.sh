#!/bin/bash

# try with -D mapreduce.job.reduces=1

mapred streaming \
   -D stream.num.map.output.key.fields=3 \
   -D mapreduce.partition.keypartitioner.options=-k1,1 \
   -D mapreduce.job.reduces=1 \
   -files Mapper.py,Reducer.py,../../Datasets/Original/historical_stocks.csv \
   -mapper Mapper.py \
   -reducer Reducer.py \
   -input /user/corrado/input/historical_stock_prices.csv \
   -output /user/corrado/output/result_job2 \
   -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner
