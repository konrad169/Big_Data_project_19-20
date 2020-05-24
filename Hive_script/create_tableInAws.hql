CREATE EXTERNAL TABLE historical_stock_prices1 (ticker STRING, open double, close double, adj_close double, low double, high double, volume int, dates date)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
LOCATION 'dataset/historical_stock_prices.csv'
TBLPROPERTIES("skip.header.line.count"="1");

CREATE EXTERNAL TABLE historical_stock_prices (ticker STRING, open double, close double, adj_close double, low double, high double, volume int, dates STRING)
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
LOCATION 'dataset/historical_stock_prices.csv'
TBLPROPERTIES("skip.header.line.count"="1");

CREATE EXTERNAL TABLE historical_stock (
	ticker STRING,
	exchanges STRING,
	name STRING,
	sector STRING,
	industry STRING)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
       "separatorChar" = ",",
       "quoteChar"     = "\""
)
LOCATION 'dataset/historical_stocks.csv'
TBLPROPERTIES("skip.header.line.count"="1");
