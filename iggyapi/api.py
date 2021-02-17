import requests
import json


class IggyAPI():
    def __init__(self, api_token):
        self.api_token = api_token
        self.base_url = "https://api.askiggy.com/v1/"
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-Iggy-Token": self.api_token,
        }

    def enrich(self, endpoint: str, options, body={}):
        method = options["method"] or "GET"
        params = options["params"]
        requestURL = self.base_url + endpoint

        if (method == "GET"):
            r = requests.get(requestURL, params=params, headers=self.headers)
            return r.json()

        elif (method == "POST"):
            r = requests.post(requestURL, data=json.dumps(
                body), headers=self.headers)
            return r.json()

    def lookup(self, options):
        return self.enrich("lookup", options)

    def isochrone(self, options):
        return self.enrich("isochrone", options)

    def points_of_interest(self, options, body={}):
        return self.enrich("points_of_interest", options, body)

    def amenities_score(self, options):
        return self.enrich("amenities_score", options)

    def clusters(self, options):
        return self.enrich("clusters", options)

    def points_of_interest_options(self):
        return self.enrich("points_of_interest_options", {"method": "GET", "params": None})
