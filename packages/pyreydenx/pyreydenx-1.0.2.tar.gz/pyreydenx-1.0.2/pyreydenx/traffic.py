from typing import List

from . import Client
from .model.result import Result
from .model.traffic import Traffic as TrafficModel


class Traffic:
    @staticmethod
    def countries(client: Client):
        """
        Traffic statistics by country

        See: https://api.reyden-x.com/docs#/Traffic/Traffic_statistics_by_country_v1_traffic_countries__get

        Parameters:
            client (Client): Instance of Client

        Returns:
            Result[List[TrafficModel]]: Result object
        """
        r = client.get('/traffic/countries/')
        return Result[List[TrafficModel]](**r)

    @staticmethod
    def languages(client: Client):
        """
        Traffic statistics by language

        See: https://api.reyden-x.com/docs#/Traffic/Traffic_statistics_by_language_v1_traffic_languages__get

        Parameters:
            client (Client): Instance of Client

        Returns:
            Result[List[TrafficModel]]: Result object
        """
        r = client.get('/traffic/languages/')
        return Result[List[TrafficModel]](**r)
