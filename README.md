# Modeling and Performance Evaluation of Time Series in Apache Cassandra

This project consists of the design, implementation, and comparative analysis of NoSQL modeling strategies for storing and querying large-scale multivariate time series. As an experimental basis, the **Controlled Anomalies Time Series (CATS) Dataset** is used to evaluate the efficiency of **Apache Cassandra** in time window query and anomaly detection scenarios.

Work developed as part of the Database course at the **Institute of Computing (IC) of the Federal University of Alagoas (UFAL)**.

---

## Directory System and Project Structure

The repository is organized in a modular way to separate the responsibilities of infrastructure, database logic, ingestion scripts, and scientific writing:

```text
cassandra-cats-timeseries/
├── article/               # Source files (LaTeX) and images for the scientific paper.
├── cql/                  # Data Definition Language (DDL) scripts and test queries.
│   └── schema.cql        # Final schema containing both modeling strategies.
├── data/                 # Local directory for storing the CATS Dataset CSV files.
├── docker/               # Infrastructure as code configuration files.
│   └── docker-compose.yml# Recipe for the Apache Cassandra container and volumes.
├── notebooks/            # Jupyter Notebooks for exploratory analysis and performance graphs.
├── src/                  # Source code for automated Python scripts.
│   ├── connection.py     # Module for managing the connection to the Cassandra cluster.
│   └── ingestion.py      # Script for reading CSVs and performing mass data load.
├── .gitignore            # Git filters to prevent uploading heavy data (data/) and virtual environments (venv/).
├── README.md             # Main project documentation (this file).
└── requirements.txt      # List of dependencies and Python libraries for the project.
```

---

## Prerequisites

Before starting, ensure you have the following installed on your machine:
* **Docker** and **Docker Compose**
* **Python 3.11+**
* **Git**

---

## Environment Setup and Execution

Follow the steps below to clone the project, start the database, and prepare the execution environment.

### 1. Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/cassandra-cats-timeseries.git](https://github.com/YOUR_USERNAME/cassandra-cats-timeseries.git)
cd cassandra-cats-timeseries
```

### 2. Initialize the Infrastructure (Apache Cassandra)
The database runs in a fully isolated environment via Docker. To download the official image and start the service in the background, execute:
```bash
cd docker
docker-compose up -d
cd ..
```
*Cassandra will be available locally on the default port `9042`.*

### 3. Configure the Python Environment
It is highly recommended to use a virtual environment to isolate project dependencies. At the root of the repository, run:

```bash
# Create the virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows (PowerShell):
.\venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install the necessary dependencies
pip install -r requirements.txt
```

### 4. Prepare the Data (CATS Dataset)
1. Download the **Controlled Anomalies Time Series (CATS) Dataset** directly from Kaggle.
2. Extract the compressed files.
3. Paste the extracted `.csv` files into the `data/` directory of this project. 
*(Note: This directory is protected by `.gitignore` and the data will not be pushed to your remote repository).*

---

## Modeling Strategies (CQL)

The database architecture was designed using a *Query-Driven Modeling* philosophy, resulting in two mirrored tables for a comparative performance analysis:

1. **`data_by_sensor`**: Uses `(sensor_id, date_bucket)` as the *Partition Key* and `event_time` as the *Clustering Key*. Optimized for aggregate analytical queries over specific sensor time windows.
2. **`data_by_anomaly`**: Uses `(anomaly_type, date_bucket)` as the *Partition Key* and `event_time, sensor_id` as *Clustering Keys*. Optimized for immediate tracking of system failures without the need for full table scans.

To manually create the table structure in the cluster, access the container terminal:
```bash
docker exec -it cassandra_cats cqlsh
```
And execute the commands contained in the `cql/schema.cql` file.
