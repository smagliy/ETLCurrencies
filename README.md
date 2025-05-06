# Exchange rates ETL 

There are subscriptions in different currencies (EUR, GBP, USD, UAH), but we need a unified report in US dollars (USD). 

## 🏁 Getting Started <a name = "getting_started"></a>

### Prerequisites

The system is running on Docker environment.

You can set up docker on your local machine [here](https://docs.docker.com/get-docker/).

---
Clone project to your local machine.

```
git clone https://github.com/smagliy/ETLCurrencies.git
```

### Setting up environment

In order to start docker environment, you need to build airflow and spark images.

In project root execute this command:
```
docker build -f docker/airflow/Dockerfile -t custom_airflow:1.0 .
```
And for Linux OS, you need to set your host user id.

```
echo -e "\n\n#Airflow user\nAIRFLOW_UID=$(id -u)" >> docker/env/main.env
```

And you are ready to start docker.

## 🚀 Deployment <a name = "deployment"></a>
### Start docker
First, you need to start airflow-init.
```
docker-compose -f docker-compose.yaml up -d airflow-init
```
It should exit with code 0.
<br />
<br />
Start rest of your environment
```
docker compose -f docker/docker-compose.yaml --env-file docker/env/main.env up -d 
```

## 🎈 Usage <a name="usage"></a>

## DAGs Details
### Daily Exchange Rate Loader
DAG ID: daily_exchange_rate_loader

Schedule: Runs daily (@daily)

Functionality:

- Fetches current exchange rates from the API
- Stores the data in MinIO under the 'exchange' bucket
- Processes the data for downstream consumption

### Monthly Historical Exchange Loader
DAG ID: monthly_historical_exchange_loader

Schedule: Runs monthly (@monthly)

Functionality:

- Processes historical exchange rates for the previous month 
- Stores the data in MinIO under the 'exchange' bucket 
- Handles all dates from the previous month automatically


