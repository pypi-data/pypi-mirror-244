import base64
import datetime
from datetime import datetime as d

import requests

DATETIME_FORMAT = "%Y-%m-%dT00:00:00+01:00"


class RteApi:
    host = "https://digital.iservices.rte-france.com"
    api_tempo_path = "/open_api/tempo_like_supply_contract/v1/tempo_like_calendars"
    api_token_path = "/token/oauth"
    next_token_refresh = None

    def __init__(self, id_client, id_secret):
        self.headers = {}
        token = base64.b64encode(bytes(id_client + ":" + id_secret, "utf-8")).decode(
            "utf-8"
        )
        self.login_headers = {"Authorization": "Basic " + token}
        self.login()

    def get_calendar(self):
        if self.next_token_refresh < d.now():
            self.login()
        end_date = (d.now() + datetime.timedelta(days=2)).strftime(DATETIME_FORMAT)
        start_date = d.now().strftime(DATETIME_FORMAT)
        params = {"start_date": start_date, "end_date": end_date}
        response = requests.get(
            self.host + self.api_tempo_path, params=params, headers=self.headers
        )
        body = response.json()
        today = None
        tomorrow = None
        for value in body["tempo_like_calendars"]["values"]:
            if value["start_date"] == d.now().strftime(DATETIME_FORMAT):
                today = value["value"]
            else:
                tomorrow = value["value"]
        if tomorrow is None:
            tomorrow = "UNKNOWN"
        return today, tomorrow

    def login(self):
        response = requests.get(
            self.host + self.api_token_path, params=None, headers=self.login_headers
        )
        body = response.json()
        self.headers = {
            "Authorization": body["token_type"] + " " + body["access_token"]
        }
        self.next_token_refresh = d.now() + datetime.timedelta(
            seconds=body["expires_in"]
        )
