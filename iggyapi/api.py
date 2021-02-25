import requests
import json
from typing import Dict
import shapely.geometry as sg
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx


class IggyAPI():
    """Basic Implementation of the API in python

    Parameters
    ----------
    api_token : str
        A string representing the token of the Iggy User

    """

    def __init__(self, api_token: str):
        self.api_token = api_token
        self.base_url = "https://api.askiggy.com/v1/"
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-Iggy-Token": self.api_token,
        }
        self.last_clusters = None
        self.last_isochrone = None

    def _convert_clusters_to_gdf_res(self, response: Dict):
        num_clusters = len(response["clusters"])

        names = [c["summary"]["place_names"] for c in response["clusters"]]
        geoms = [c["geojson"] for c in response["clusters"]]
        gdf = gpd.GeoDataFrame.from_features(geoms)
        gdf["names"] = names
        gdf.crs = {"init": "epsg:4326"}
        self.last_clusters = gdf
        return gdf

    def _create_isochrone_gdf(self, response: Dict):
        gdf = gpd.GeoDataFrame.from_features([response])
        gdf.crs = {"init": "epsg:4326"}
        self.last_isochrone = gdf
        return gdf

    def plot(self, endpoint):
        if endpoint == "isochrone":
            gdf = self.last_isochrone
        elif endpoint == "clusters":
            gdf = self.last_clusters
        else:
            print("Endpoint not yet supported")
            return

        ax = gdf.plot(edgecolor="k", alpha=0.5)
        ctx.add_basemap(
            ax, zoom=16, source=ctx.providers.Stamen.TonerLite, crs=gdf.crs)
        ax.set_axis_off()
        plt.show()

    def enrich(self, endpoint: str, options: Dict, body: Dict = {}) -> Dict:
        method = options.get("method") or "GET"
        params = options.get("params")
        requestURL = self.base_url + endpoint

        if (method == "GET"):
            r = requests.get(requestURL, params=params, headers=self.headers)
            return r.json()

        elif (method == "POST"):
            r = requests.post(requestURL, data=json.dumps(
                body), headers=self.headers)
            return r.json()

    def lookup(self, options: Dict) -> Dict:
        return self.enrich("lookup", options)

    def isochrone(self, options: Dict) -> sg.Polygon:
        # Defaults to False seems to be a better option
        raw_response = options.get("raw", False)
        if raw_response:
            return self.enrich("isochrone", options)
        else:
            return self._create_isochrone_gdf(self.enrich("isochrone", options))

    def points_of_interest(self, options: Dict, body: Dict = {}) -> Dict:
        return self.enrich("points_of_interest", options, body)

    def amenities_score(self, options: Dict):
        return self.enrich("amenities_score", options)

    def clusters(self, options: Dict):
        raw_response = options.get("raw", False)
        if raw_response:
            return self.enrich("clusters", options)
        else:
            return self._convert_clusters_to_gdf_res(self.enrich("clusters", options))

    def points_of_interest_options(self):
        return self.enrich("points_of_interest_options", {"method": "GET", "params": None})
