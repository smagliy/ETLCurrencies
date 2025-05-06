import os
from abc import ABC, abstractmethod
from datetime import date

from src.config import APIConfig
from src.services.api.exchange_rates_srv import ExchangeRateService
from src.services.minio.bucket_service import BucketOperations
from src.services.utils.utils_handler import create_path, get_previous_month_dates
from src.services.logger.logging import LoggerConfig

logger = LoggerConfig.set_up_logger()


class BaseLoad(ABC):
    def __init__(self, minio_client: BucketOperations, bucket_name: str, endpoint: str, path_key: str):
        self.url = f"{APIConfig.BASE_API_URL}{endpoint}"
        self.params = APIConfig.PARAMS
        self.minio = minio_client
        self.bucket = bucket_name
        self.path_key = path_key
        self.filename = 'rates.json'

    def fetch_rates(self, historical_date: date = None) -> bytes:
        try:
            logger.info(f"Fetching data from {self.url}...")
            url = self.url + historical_date.strftime('%Y-%m-%d') + '.json' if historical_date else self.url
            response = ExchangeRateService(url, self.params).get_response()
            return response
        except Exception as e:
            logger.error(f"Failed to fetch exchange rates: {e}")
            raise

    def store_rates(self, data: bytes, historical_date: date = None):
        try:
            path = create_path(self.path_key, historical_date)
            logger.info(f"Writing data to bucket: {self.bucket}/{path}/{self.filename}")
            self.minio.write_string_to_bucket(self.bucket, path, self.filename, data)
        except Exception as e:
            logger.error(f"Failed to write to MinIO: {e}")
            raise

    def load(self, historical_date: date = None):
        data = self.fetch_rates(historical_date=historical_date)
        self.store_rates(data, historical_date)

    @abstractmethod
    def run(self):
        """Defines a template method to execute the load process."""
        pass


class DailyLoad(BaseLoad):
    def __init__(self, minio_client: BucketOperations, bucket_name: str):
        super().__init__(minio_client, bucket_name, APIConfig.DAILY_ENDPOINT, 'daily')

    def run(self):
        self.load()


class HistoricalLoad(BaseLoad):
    def __init__(self, minio_client: BucketOperations, bucket_name: str):
        super().__init__(minio_client, bucket_name, APIConfig.HISTORICAL_ENDPOINT, 'historical')

    def run(self):
        for hist_date in get_previous_month_dates():
            logger.info(f'Processing historical data for {hist_date.strftime("%Y-%m-%d")}')
            self.load(historical_date=hist_date)
