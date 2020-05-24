#!/bin/bash

mapred streaming \
	  -D stream.num.map.output.key.fields=3 \
		-D mapreduce.partition.keypartitioner.options=-k1,1 \
		-D mapreduce.job.reduces=2 \
		-files FirstMapper.py,FirstReducer.py,../../Datasets/Original/historical_stocks.csv \
		-mapper FirstMapper.py \
		-reducer FirstReducer.py \
		-input /user/corrado/input/historical_stock_prices.csv \
		-output /user/corrado/output/job3_hadoop_tmp \
		-partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner \
&& 	\
mapred streaming \
		-D stream.num.map.output.key.fields=3 \
		-D mapreduce.job.reduces=1 \
		-files SecondMapper.py,SecondReducer.py \
		-mapper SecondMapper.py \
		-reducer SecondReducer.py \
		-input /user/corrado/output/job3_hadoop_tmp/part-* \
		-output /user/corrado/output/result_job3 \
