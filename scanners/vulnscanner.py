import json
import requests


class VulnerabilityScanner:
    def __init__(self, database_url):
        self.db_url = database_url
        self.founded = 0
        host = database_url.split("://")[1].split("/")[0]
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:63.0) Gecko/20100101 Firefox/63.0'",
            "Host": host,
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive"
        }

    def add_founded(self):
        self.founded = self.founded + 1

    def get_founded(self):
        return self.founded

    def parse_vulnerabilities(self, text):
        data = json.loads(text)["list"]
        return data

    def find(self, type, product):
        url = self.db_url.replace("{type}", type.lower()).replace(
            "{product}", product.lower())
        req = requests.get(url, headers=self.headers)

        if req.status_code == 200:
            return self.parse_vulnerabilities(req.text)
        else:
            return []
