CREATE VIEW IF NOT EXISTS ticker_min_max_avg AS
SELECT ticker, min(low) AS min_price, max(high) AS max_price, avg(volume) AS avg_volume
FROM historical_stock_prices1
WHERE dates>='2008-01-01' AND dates<='2018-12-31'
GROUP BY ticker;

CREATE VIEW IF NOT EXISTS min2008 AS
SELECT ticker, min(dates) AS min_data
FROM historical_stock_prices1
WHERE dates>='2008-01-01' AND dates<='2018-12-31'
GROUP BY ticker;

CREATE VIEW IF NOT EXISTS max2018 AS
SELECT ticker, max(dates) AS max_data
FROM historical_stock_prices1
WHERE dates>='2008-01-01' AND dates<='2018-12-31'
GROUP BY ticker;

CREATE VIEW IF NOT EXISTS ticker_chiusura_iniziale AS
SELECT hsp.ticker, hsp.dates, hsp.close
FROM min2008 AS min, historical_stock_prices1 AS hsp
WHERE hsp.ticker=min.ticker AND hsp.dates=min.min_data;

CREATE VIEW IF NOT EXISTS ticker_chiusura_finale AS
SELECT hsp.ticker, hsp.dates, hsp.close
FROM max2018 AS max, historical_stock_prices1 AS hsp
WHERE hsp.ticker=max.ticker AND hsp.dates=max.max_data;

CREATE VIEW IF NOT EXISTS variazione_quotazione AS
SELECT ci.ticker, FLOOR(((cf.close-ci.close)/ci.close)*100) AS variazione
FROM ticker_chiusura_finale AS cf join ticker_chiusura_iniziale AS ci on cf.ticker=ci.ticker;

CREATE TABLE IF NOT EXISTS risultati1 AS
SELECT a.ticker, b.variazione, a.min_price, a.max_price, a.avg_volume
FROM ticker_min_max_avg AS a join variazione_quotazione AS b on a.ticker=b.ticker
ORDER BY b.variazione DESC limit 10;
