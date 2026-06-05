-- Criação do Banco de Dados
CREATE KEYSPACE IF NOT EXISTS cats_db WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'};
USE cats_db;

-- Modelagem por Sensor
CREATE TABLE IF NOT EXISTS data_by_sensor (
    sensor_id text,
    date_bucket text,
    event_time timestamp,
    sensor_value double,
    anomaly_type text,
    PRIMARY KEY ((sensor_id, date_bucket), event_time)
) WITH CLUSTERING ORDER BY (event_time ASC);

-- Modelagem por Anomalia
CREATE TABLE IF NOT EXISTS data_by_anomaly (
    anomaly_type text,
    date_bucket text,
    event_time timestamp,
    sensor_id text,
    sensor_value double,
    PRIMARY KEY ((anomaly_type, date_bucket), event_time, sensor_id)
) WITH CLUSTERING ORDER BY (event_time ASC, sensor_id ASC);

-- Inserindo Dados de Teste
-- Dado Nominal
INSERT INTO data_by_sensor (sensor_id, date_bucket, event_time, sensor_value, anomaly_type) 
VALUES ('sensor_1', '2026-06-05', '2026-06-05 10:15:00', 42.5, 'nominal');
INSERT INTO data_by_anomaly (anomaly_type, date_bucket, event_time, sensor_id, sensor_value) 
VALUES ('nominal', '2026-06-05', '2026-06-05 10:15:00', 'sensor_1', 42.5);

-- Dado Anômalo
INSERT INTO data_by_sensor (sensor_id, date_bucket, event_time, sensor_value, anomaly_type) 
VALUES ('sensor_5', '2026-06-05', '2026-06-05 14:30:00', 99.9, 'spike_anomaly');
INSERT INTO data_by_anomaly (anomaly_type, date_bucket, event_time, sensor_id, sensor_value) 
VALUES ('spike_anomaly', '2026-06-05', '2026-06-05 14:30:00', 'sensor_5', 99.9);


-- Filtrando por janela de tempo de um sensor
SELECT * FROM data_by_sensor 
WHERE sensor_id = 'sensor_1' 
  AND date_bucket = '2026-06-05' 
  AND event_time >= '2026-06-05 10:00:00' 
  AND event_time <= '2026-06-05 11:00:00';

-- Buscando diretamente por um tipo de anomalia
SELECT * FROM data_by_anomaly 
WHERE anomaly_type = 'spike_anomaly' 
  AND date_bucket = '2026-06-05';