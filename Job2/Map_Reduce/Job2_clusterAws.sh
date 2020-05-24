#!/bin/bash

hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming.jar \
				-D stream.num.map.output.key.fields=3 \
				-D mapreduce.partition.keypartitioner.options=-k1,1 \
				-D mapreduce.job.reduces=1 \
				-files Mapper.py,Reducer.py,historical_stocks.csv \
				-mapper Mapper.py \
				-reducer Reducer.py \
				-input /input/s3/historical_stock_prices.csv \
				-output /output/result_job2 \
				-partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner
