import requests
import json
from typing import Dict
import shapely.geometry as sg
import geopandas as gpd


class IggyAPI():
    def __init__(self, api_token: str):
        self.api_token = api_token
        self.base_url = "https://api.askiggy.com/v1/"
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-Iggy-Token": self.api_token,
        }

    def _get_coordinates(self, return_dict: Dict):
        return return_dict.get("geometry").get("coordinates")[0]

    def _convert_ischrone_to_gdf_res(self, response: Dict):
        num_clusters = len(response["clusters"])

        names = [None] * num_clusters
        d2 = [None] * num_clusters
        gdf_l = [None] * num_clusters
        cluster = [None] * num_clusters
        line_dist = [None] * num_clusters
        for i in range(num_clusters):
            d2[i] = response['clusters'][i]['geojson']
            ['geometry']['coordinates'][0]
            names[i] = response['clusters'][i]['summary']['place_names']
            line_dist[i] = response["clusters"][i]["geojson"]
            ["properties"]["straight_line_distance_miles"]

            cluster[i] = sg.Polygon(d2[i])
            gdf = gpd.GeoSeries([cluster[i]])
            # give it a crs (iggy data is 4326, then update it for basemap to 3857 (standard here))
            gdf.crs = {'init': 'epsg:4326'}
            gdf = gdf.to_crs(epsg=3857)
            gdf_l[i] = (gdf)

        polys_gdf = gpd.GeoDataFrame(gdf_l, geometry=0)
        polys_gdf = polys_gdf.rename(
            columns={0: "polygon"}).set_geometry("polygon")

        polys_gdf['names'] = names
        polys_gdf["straight_line_distance"] = line_dist

        return polys_gdf

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
        # Should there be an option to get the entire response
        return sg.Polygon(self._get_coordinates(self.enrich("isochrone", options)))

    def points_of_interest(self, options: Dict, body: Dict = {}) -> Dict:
        return self.enrich("points_of_interest", options, body)

    def amenities_score(self, options: Dict):
        return self.enrich("amenities_score", options)

    def clusters(self, options: Dict):
        return self._convert_ischrone_to_gdf_res(self.enrich("clusters", options))

    def points_of_interest_options(self):
        return self.enrich("points_of_interest_options", {"method": "GET", "params": None})
