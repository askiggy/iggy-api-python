import requests
import json
from typing import Dict, Union
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx


class IggyAPI():
    """Basic Implementation of the Iggy API in python

    Parameters
    ----------
    api_token : str
        A string representing the token of the Iggy User.
        See your user dashboard at `https://www.askiggy.com/dashboard`
        to find your API token.
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

    def plot(self, endpoint: str):
        """Plots result of last call to `isochrone` or `clusters` endpoint.

        :param endpoint: str
            Name of endpoint result to plot
        :return: None
        """
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
        """Generic method to execute a call to the Iggy API

        :param endpoint: str
            Endpoint name, e.g. `lookup` or `clusters`
        :param options: dict
            Endpoint parameters. Must contain key `params` with query params.
            See the API documentation for details
        :param body: dict
            For POST requests, the body of the request
        :return: dict
        """
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
        """Call `/lookup` endpoint

        This endpoint looks up the value of data at an input point. It
        can be used to answer the question, "Tell me what you know about
        this point."

        Options dict should contain key `params` with value being a dict
        of API query parameters. For example:
        {
          'params':
          {
            'latitude': 44.976,
            'longitude': -93.271,
            'labels': 'population_density_per_km,air_quality'
          }
        }

        The query parameters include:
            - `latitude` (float), ex. 44.976
            - `longitude` (float), ex. -93.271
            - `labels` (str), ex. 'population_density_per_km,air_quality'
            - `summary_radius_km` (float, optional), ex. 5

        :param options: dict
        :return: dict
        """
        return self.enrich("lookup", options)

    def isochrone(self, options: Dict, raw_response: bool = False) \
            -> Union[gpd.GeoDataFrame,Dict]:
        """Call `/isochrone` endpoint

        This endpoint returns a polygon representing the area traversable
        by foot, bike, or car from an input point.

        This function returns a gpd.GeoDataFrame by default. In order
        to return the raw JSON API response, set `raw_response=True`.

        Options dict should contain key `params` with value being a dict
        of API query parameters. For example:
        {
          'params':
          {
            'latitude': 44.976,
            'longitude': -93.271,
            'within_minutes_walking': 20
          }
        }

        The query parameters include:
            - `latitude` (float), ex. 44.976
            - `longitude` (float), ex. -93.271
            - One of:
                - `within_minutes_driving` (int), ex. 15
                - `within_minutes_biking` (int), ex. 15
                - `within_minutes_walking` (int), ex. 15
                - `within_miles` (int), ex. 10

        :param options: dict
        :param raw_response: bool

        :return: gpd.GeoDataFrame or dict
        """
        if raw_response:
            return self.enrich("isochrone", options)
        else:
            return self._create_isochrone_gdf(self.enrich("isochrone", options))

    def points_of_interest(self, options: Dict, body: Dict = {}) -> Dict:
        """Call to `/points_of_interest` endpoint

        This endpoint returns the names of POIs within a given distance
        of an input point, or located within an input polygon. It answers
        questions like, "Are there any bars within 5 minutes walk of this
        point?" or "Are there any bars within this input polygon?"

        Options dict should contain key `params` with value being a dict
        of API query parameters. For example:
        {
          'params':
          {
            'latitude': 44.976,
            'longitude': -93.271,
            'labels': 'coffee_shops,book_stores',
            'within_minutes_walking': 20
          }
        }

        The query parameters include:
            - `latitude` (float), ex. 44.976
            - `longitude` (float), ex. -93.271
            - One of:
                - `labels` (str), ex. 'coffee_shops,book_stores'
                - `brands` (str), ex. 'Starbucks'
            - One of:
                - `within_minutes_driving` (int), ex. 15
                - `within_minutes_biking` (int), ex. 15
                - `within_minutes_walking` (int), ex. 15
                - `within_miles` (int), ex. 10

        Alternatively, this request can be made using POST and a geojson
        object as the body to get the points of interest within an input
        polygon. For example:

        options = {'method': 'POST', 'parms': {'labels': 'book_stores'}}
        body = {'type': 'Feature', 'properties': {}, 'geometry': {...}}

        :param options: dict
        :param body: dict
            GeoJSON object, to be used with POST
        :return: dict
        """
        return self.enrich("points_of_interest", options, body)

    def amenities_score(self, options: Dict) -> Dict:
        """Call `/amenities_score` endpoint

        This endpoint returns a numeric score representing the diversity
        of quality of life amenities (i.e. parks, bakeries restaurants, etc)
        within a given distance of an input point.

        Options dict should contain key `params` with value being a dict
        of API query parameters. For example:
        {
          'params':
          {
            'latitude': 44.976,
            'longitude': -93.271,
            'within_minutes_walking': 20
          }
        }

        The query parameters include:
            - `latitude` (float), ex. 44.976
            - `longitude` (float), ex. -93.271
            - One of:
                - `within_minutes_driving` (int), ex. 15
                - `within_minutes_biking` (int), ex. 15
                - `within_minutes_walking` (int), ex. 15
                - `within_miles` (int), ex. 10

        :param options: dict

        :return: dict
        """
        return self.enrich("amenities_score", options)

    def clusters(self, options: Dict, raw_response: bool = False) \
            -> Union[gpd.GeoDataFrame,Dict]:
        """Call `/clusters` endpoint

        This endpoint returns a set of clusters (polygons) comprising
        a region containing amenities of a given type (e.g. restaurants,
        bars), within a given distance of an input point.

        This function returns a gpd.GeoDataFrame by default. In order
        to return the raw JSON API response, set `raw_response=True`.

        Options dict should contain key `params` with value being a dict
        of API query parameters. For example:
        {
          'params':
          {
            'latitude': 44.976,
            'longitude': -93.271,
            'category': 'restaurants',
            'within_minutes_walking': 20
          }
        }

        The query parameters include:
            - `latitude` (float), ex. 44.976
            - `longitude` (float), ex. -93.271
            - `category` (str), ex. 'restaurants'
            - One of:
                - `within_minutes_driving` (int), ex. 15
                - `within_minutes_biking` (int), ex. 15
                - `within_minutes_walking` (int), ex. 15
                - `within_miles` (int), ex. 10

        :param options: dict
        :param raw_response: bool

        :return: gpd.GeoDataFrame or dict
        """
        raw_response = options.get("raw", False)
        if raw_response:
            return self.enrich("clusters", options)
        else:
            return self._convert_clusters_to_gdf_res(self.enrich("clusters", options))

    def points_of_interest_options(self) -> Dict:
        """Call `/points_of_interest_options` endpoint.
        
        This endpoint returns a dict containing supported parameters
        for the `/points_of_interest` endpoint.

        :return: dict
        """
        return self.enrich("points_of_interest_options", {"method": "GET", "params": None})
