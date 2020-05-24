CREATE TABLE IF NOT EXISTS join_csv3 AS
SELECT hs.name, hs.sector, hsp.dates, hsp.close, hsp.ticker
FROM historical_stock AS hs JOIN historical_stock_prices AS hsp on hsp.ticker=hs.ticker
WHERE YEAR(dates)>=2016 AND YEAR(dates)<=2018 AND hs.sector!='N/A';

CREATE VIEW IF NOT EXISTS name_dates_min_max AS
SELECT name, ticker, sector, YEAR(dates) AS anno, min(TO_DATE(dates)) AS min_data, max(TO_DATE(dates)) AS max_data
FROM join_csv3
GROUP BY name, ticker, sector, YEAR(dates);

CREATE VIEW IF NOT EXISTS quotazione_inizio_anno3 AS
SELECT b.name, a.ticker, YEAR(b.min_data) AS anno, SUM(a.close) AS min_close
FROM join_csv3 AS a, name_dates_min_max AS b
WHERE a.ticker=b.ticker AND a.dates=b.min_data
GROUP BY b.name, a.ticker, YEAR(b.min_data);

CREATE VIEW IF NOT EXISTS quotazione_fine_anno3 AS
SELECT b.name, a.ticker, YEAR(b.max_data) AS anno, SUM(a.close) AS max_close
FROM join_csv3 AS a, name_dates_min_max AS b
WHERE a.dates=b.max_data AND a.ticker=b.ticker
GROUP BY b.name, a.ticker, YEAR(b.max_data);

CREATE TABLE IF NOT EXISTS variazione_settore3 AS
SELECT qi.name, qi.ticker,qi.anno, ROUND((qf.max_close - qi.min_close) / qi.min_close *100, 0) AS differenza_percentuale
FROM quotazione_inizio_anno3 AS qi, quotazione_fine_anno3 AS qf
WHERE qi.name=qf.name AND qi.anno=qf.anno AND qi.ticker=qf.ticker
ORDER BY  ticker, anno;

CREATE TABLE IF NOT EXISTS groups AS
SELECT name, concat_ws(',', collect_list(cast (differenza_percentuale AS STRING))) AS quotazione, anno
FROM variazione_settore3
GROUP BY name, anno;

CREATE TABLE IF NOT EXISTS risultati3 AS
SELECT collect_set(g1.name), g1.quotazione AS variazione16, g2.quotazione AS variazione17, g3.quotazione AS variazione18
FROM groups g1, groups g2, groups g3
WHERE g1.name = g2.name AND g1.anno != g2.anno != g3.anno AND g1.name = g3.name AND g1.anno = '2016' AND g2.anno = '2017' AND g3.anno = '2018'
GROUP BY g1.quotazione, g2.quotazione, g3.quotazione
HAVING count(*)>1;
