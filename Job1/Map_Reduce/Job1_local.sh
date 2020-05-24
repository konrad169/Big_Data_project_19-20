#!/bin/bash

mapred streaming \
    -D stream.num.map.output.key.fields=2 \
    -D mapreduce.job.reduces=1 \
    -files Mapper.py,Reducer.py \
    -mapper Mapper.py \
    -reducer Reducer.py \
    -input /user/corrado/input/historical_stock_prices.csv \
    -output /user/corrado/output/result_job1
