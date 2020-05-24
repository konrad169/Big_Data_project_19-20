CREATE TABLE historical_stock_prices1 (ticker STRING, open float, close float, adj_close float,low float, high float, volume float, dates date)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n'
TBLPROPERTIES("skip.header.line.count"="1");

LOAD DATA LOCAL INPATH '/home/corrado/Scrivania/bd_project/Datasets/Original/historical_stock_prices.csv'
OVERWRITE INTO TABLE historical_stock_prices1;


CREATE TABLE historical_stock_prices (ticker STRING, open float, close float, adj_close float,low float, high float, volume float, dates STRING)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n'
TBLPROPERTIES("skip.header.line.count"="1");

LOAD DATA LOCAL INPATH '/home/corrado/Scrivania/bd_project/Datasets/Original/historical_stock_prices.csv'
OVERWRITE INTO TABLE historical_stock_prices;

CREATE TABLE historical_stock (ticker STRING,exchanges STRING,name STRING,sector STRING,industry STRING)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES ("separatorChar"=",","quoteChar"="\"")
STORED AS TEXTFILE
TBLPROPERTIES("skip.header.line.count"="1");

LOAD DATA LOCAL INPATH '/home/corrado/Scrivania/bd_project/Datasets/Original/historical_stocks.csv'
OVERWRITE INTO TABLE historical_stock;
