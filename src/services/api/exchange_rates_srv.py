import requests
import os
import json
from typing import Dict
from requests.exceptions import RequestException

from src.services.logger.logging import LoggerConfig

logger = LoggerConfig.set_up_logger()


class ExchangeRateService:
    def __init__(self, url: str, params: Dict = dict(), timeout: int = 10):
        self.base_url = url
        self.timeout = timeout
        self.params = params
        self.session = requests.Session()

    def get_response(self) -> bytes:
        try:
            logger.info(f"Fetching exchange rates from {self.base_url}")
            response = self.session.get(
                self.base_url,
                params=self.params,
                timeout=self.timeout
            )
            response.raise_for_status()
            return json.dumps(response.text).encode('utf-8')
        except RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            raise RequestException(f"Failed to fetch exchange rates: {str(e)}")
        except ValueError as e:
            logger.error(f"Failed to parse API response: {str(e)}")
            raise ValueError("Invalid JSON response from API")
        finally:
            self.session.close()
