-- View 1: Temperatura media por dispositivo
-- Objetivo: identificar quais dispositivos/ambientes registram temperaturas
-- mais altas ou mais baixas em media, util para deteccao de anomalias por local.
CREATE OR REPLACE VIEW avg_temp_por_dispositivo AS
SELECT
    device_id,
    ROUND(AVG(temperature)::numeric, 2) AS avg_temp,
    COUNT(*) AS total_leituras
FROM temperature_readings
GROUP BY device_id
ORDER BY avg_temp DESC;

-- View 2: Contagem de leituras por hora do dia
-- Objetivo: entender a distribuicao temporal das leituras dos sensores,
-- revelando horarios de maior atividade/tráfego de dados.
CREATE OR REPLACE VIEW leituras_por_hora AS
SELECT
    EXTRACT(HOUR FROM reading_time)::int AS hora,
    COUNT(*) AS contagem
FROM temperature_readings
GROUP BY hora
ORDER BY hora;

-- View 3: Temperaturas maxima e minima por dia
-- Objetivo: observar a amplitude termica diaria, util para identificar
-- picos de calor/frio e variacoes bruscas ao longo do tempo.
CREATE OR REPLACE VIEW temp_max_min_por_dia AS
SELECT
    DATE(reading_time) AS data,
    ROUND(MAX(temperature)::numeric, 2) AS temp_max,
    ROUND(MIN(temperature)::numeric, 2) AS temp_min,
    ROUND(AVG(temperature)::numeric, 2) AS temp_media
FROM temperature_readings
GROUP BY DATE(reading_time)
ORDER BY data;
