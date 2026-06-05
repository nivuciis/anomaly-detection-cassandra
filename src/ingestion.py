import pandas as pd
import time
from cassandra_connection import get_cassandra_session
from cassandra.concurrent import execute_concurrent_with_args

def load_data():
    session = get_cassandra_session()
    
    query_sensor = session.prepare("""
        INSERT INTO data_by_sensor (sensor_id, date_bucket, event_time, sensor_value, anomaly_type) 
        VALUES (?, ?, ?, ?, ?)
    """)
    
    query_anomaly = session.prepare("""
        INSERT INTO data_by_anomaly (anomaly_type, date_bucket, event_time, sensor_id, sensor_value) 
        VALUES (?, ?, ?, ?, ?)
    """)

    csv_path = "../data/data.csv"
    
    sensor_columns = [
        'aimp', 'amud', 'arnd', 'asin1', 'asin2', 'adbr', 'adfl', 
        'bed1', 'bed2', 'bfo1', 'bfo2', 'bso1', 'bso2', 'bso3', 
        'ced1', 'cfo1', 'cso1'
    ]

    chunk_size = 5000 
    total_inserted = 0
    start_time = time.time()

    try:
        print(f"Starting data ingestion from '{csv_path}' with chunk size of {chunk_size}...")
        
        for chunk_idx, chunk in enumerate(pd.read_csv(csv_path, chunksize=chunk_size)):
            
            chunk['timestamp'] = pd.to_datetime(chunk['timestamp'])
            chunk['date_bucket'] = chunk['timestamp'].dt.strftime('%Y-%m-%d')
            chunk['anomaly_type'] = chunk['category'].astype(str) 

            melted_chunk = chunk.melt(
                id_vars=['timestamp', 'date_bucket', 'anomaly_type'],
                value_vars=sensor_columns,
                var_name='sensor_id',
                value_name='sensor_value'
            )

            params_sensor = []
            params_anomaly = []

            for row in melted_chunk.itertuples(index=False):
                event_time = row.timestamp
                date_bucket = row.date_bucket
                anomaly_type = row.anomaly_type
                sensor_id = row.sensor_id
                sensor_value = float(row.sensor_value)

                params_sensor.append((sensor_id, date_bucket, event_time, sensor_value, anomaly_type))
                params_anomaly.append((anomaly_type, date_bucket, event_time, sensor_id, sensor_value))

            execute_concurrent_with_args(session, query_sensor, params_sensor, concurrency=100)
            execute_concurrent_with_args(session, query_anomaly, params_anomaly, concurrency=100)
            
            total_inserted += len(melted_chunk)
            print(f"Chunk {chunk_idx + 1} processed. Total records inserted so far: {total_inserted}.")

        end_time = time.time()
        print(f"\n[SUCCESS] Operation completed in {end_time - start_time:.2f} seconds!")

    except FileNotFoundError:
        print(f"[ERROR] File not found: '{csv_path}'.")
    except Exception as e:
        print(f"[ERROR] An issue occurred during ingestion: {e}")
    finally:
        session.cluster.shutdown()

if __name__ == "__main__":
    load_data()