from cassandra.cluster import Cluster

def get_cassandra_session():
    """
    Makes the connection to the Apache Cassandra cluster and returns a session object for executing queries.
    Assumes Cassandra is running locally on the default port (9042) and that the keyspace 'cats_db' has already been created.
    """
    cluster = Cluster(['127.0.0.1'], port=9042)
    session = cluster.connect('cats_db')
    print("Connected to Cassandra cluster and keyspace 'cats_db'.")
    return session