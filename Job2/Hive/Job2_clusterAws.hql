CREATE TABLE IF NOT EXISTS join_csv2 AS
SELECT hs.sector, hsp.ticker, hsp.dates, hsp.close, hsp.volume
FROM historical_stock AS hs JOIN historical_stock_prices AS hsp ON hsp.ticker=hs.ticker
WHERE YEAR(hsp.dates)>=2008 AND YEAR(hsp.dates)<=2018 AND hs.sector!='N/A';

CREATE VIEW IF NOT EXISTS volume_settore AS
SELECT sector, YEAR(dates) AS anno, SUM(volume) AS somma_volume, COUNT(ticker) AS contatore
FROM join_csv2
GROUP BY sector, YEAR(dates);

CREATE VIEW IF NOT EXISTS volume_medio_settore AS
SELECT sector, anno, ROUND(somma_volume/contatore) AS avg_volume
FROM volume_settore;

CREATE VIEW IF NOT EXISTS dates_min_max AS
SELECT sector, ticker, min(TO_DATE(dates)) AS min_data, max(TO_DATE(dates)) AS max_data
FROM join_csv2
GROUP BY sector, ticker, YEAR(dates);

CREATE VIEW IF NOT EXISTS quotazione_inizio_anno2 AS
SELECT d.sector, YEAR(d.min_data) AS anno, SUM(j.close) AS min_close
FROM join_csv2 AS j, dates_min_max AS d
WHERE j.sector=d.sector AND j.dates=d.min_data AND d.ticker=j.ticker
GROUP BY d.sector, YEAR(d.min_data);

CREATE VIEW IF NOT EXISTS quotazione_fine_anno2 AS
SELECT d.sector, YEAR(d.max_data) AS anno, SUM(j.close) AS max_close
FROM join_csv2 AS j, dates_min_max AS d
WHERE j.sector=d.sector AND j.dates=d.max_data AND d.ticker=j.ticker
GROUP BY d.sector, YEAR(d.max_data);

CREATE TABLE IF NOT EXISTS variazione_settore2 AS
SELECT mi.sector, mi.anno, ROUND(AVG(((ma.max_close - mi.min_close) / mi.min_close) * 100), 2) AS differenza_percentuale
FROM quotazione_inizio_anno2 AS mi, quotazione_fine_anno2 AS ma
WHERE mi.sector=ma.sector AND mi.anno=ma.anno
GROUP BY mi.sector, mi.anno;

CREATE VIEW IF NOT EXISTS prezzo_chiusura AS
SELECT sector, dates, SUM(close) AS somma
FROM join_csv2
GROUP BY sector, dates;

CREATE VIEW IF NOT EXISTS quotazione_giornaliera_media AS
SELECT sector, YEAR(dates) AS anno, AVG(somma) AS media
FROM prezzo_chiusura
GROUP BY sector, YEAR(dates);

CREATE TABLE IF NOT EXISTS risultati2 AS
SELECT a.sector, a.anno, c.avg_volume, b.differenza_percentuale, a.media
FROM quotazione_giornaliera_media AS a, variazione_settore2 AS b, volume_medio_settore AS c
WHERE a.sector=b.sector AND b.sector=c.sector AND a.anno=b.anno AND c.anno=b.anno
ORDER BY sector, anno;
