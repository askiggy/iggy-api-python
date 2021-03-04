from copy import deepcopy
import geopandas as gpd
import logging
import pandas as pd
from shapely.geometry import Point
from typing import List

from iggyapi.api import IggyAPI

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class FeatureCalc():
    """Calculates feature value from Iggy API response dict

    Parameters
    ----------
    calc_method: str, one of `count`, `min`, `max`, `value` (default)
        How to derive feature value from input
    result_keys : list of str
        keys for retrieving feature from API result dict, in order
        of traversal
    """
    def __init__(self, result_keys: List, calc_method: str = 'value'):
        self.calc_method = calc_method
        self.result_keys = result_keys

    def __call__(self, input_data: dict) -> float:
        contents = self._dict_find(input_data, self.result_keys[:-1])
        final_key = self.result_keys[-1]
        if self.calc_method == 'value':
            result = contents[final_key]
        elif self.calc_method == 'count':
            try:
                result = len([d[final_key] for d in contents])
            except ValueError:
                result = None
        elif self.calc_method == 'min':
            try:
                result = min([d[final_key] for d in contents])
            except ValueError:
                result = None
        elif self.calc_method == 'max':
            try:
                result = max([d[final_key] for d in contents])
            except ValueError:
                result = None
        else:
            logger.error(f'Unsupported `calc_method`: {self.calc_method}')
            raise ValueError
        return result

    def _dict_find(self, d: dict, path_keys: List):
        dc = deepcopy(d)
        for p in path_keys:
            dc = dc[p]
        return dc


class IggyFeature():
    """Location-based feature derived from Iggy API for input Point data

    Parameters
    ----------
    api : IggyAPI
        The IggyAPI object used to generate this feature
    name : str
        Feature name
    endpoint : str
        Iggy API endpoint used to calculate feature
    params : dict
        Parameters to be used with endpoint to get Iggy API data for feature
        (excluding latitude and longitude)
    calc : FeatureCalc
        Calculation method
    """
    def __init__(self, api: IggyAPI, name: str = None, endpoint: str = None,
                 params: dict = None, calc: FeatureCalc = None):
        self.api = api
        self.name = name
        self.endpoint = endpoint
        self.params = params
        self.calc = calc

    def from_dict(self, d: dict):
        self.name = d['name']
        self.endpoint = d['endpoint']
        self.params = d['params']
        self.calc = FeatureCalc(d['result_keys'],  d.get('calc_method', 'value'))

    def calculate(self, longitude: float, latitude: float) -> float:
        """Calculate feature value at input point"""
        querystring = deepcopy(self.params)
        querystring["latitude"] = latitude
        querystring["longitude"] = longitude
        options = {"params": querystring}
        api_response = self.api.enrich(self.endpoint, options)
        if "message" in api_response:
            logger.error(f"Error API response: {api_response['message']}")
            result = None
        else:
            result = self.calc(api_response)
        return result


class IggyLookupFeature(IggyFeature):
    def __init__(self, api: IggyAPI, label: str, calc_method: str = 'value'):
        super().__init__(api)
        if len(label.split(',')) > 1:
            logging.error('IggyLookupFeature supports only a single label')
            raise ValueError
        self.name = f'lookup_{label}_{calc_method}'
        self.endpoint = 'lookup'
        self.params = {
            'labels': label
        }
        result_key = 'value'
        self.calc = FeatureCalc(result_keys=[label, result_key],
                                calc_method=calc_method)


class IggyPOIFeature(IggyFeature):
    def __init__(self, api: IggyAPI, calc_method: str, label: str = None, brand: str = None,
                 within_minutes_driving: float = None, within_minutes_biking: float = None,
                 within_minutes_walking: float = None, within_miles: float = None):
        super().__init__(api)
        if label and len(label.split(',')) > 1:
            logging.error('IggyPOIFeature supports only a single brand or label')
            raise ValueError
        if brand and len(brand.split(',')) > 1:
            logging.error('IggyPOIFeature supports only a single brand or label')
            raise ValueError
        if (label is None) == (brand is None):
            logging.error('Must specify either brand or label')
            raise ValueError
        if sum([x is None for x in [within_minutes_driving, within_minutes_biking,
                                    within_minutes_walking, within_miles]]) != 3:
            logging.error('Must specify exactly one of `within_miles|minutes_driving|walking|biking')
            raise ValueError
        if label:
            self.name = f'poi_{label}_{calc_method}'
            self.params = {
                'labels': label
            }
            result_key = label
        else:
            self.name = f'poi_{brand}_{calc_method}'
            self.params = {
                'brands': brand
            }
            result_key = brand
        self.endpoint = 'points_of_interest'
        self.calc = FeatureCalc(result_keys=[result_key, 'straight_line_distance_miles'],
                                calc_method=calc_method)
        if within_minutes_driving:
            self.params['within_minutes_driving'] = within_minutes_driving
        elif within_minutes_biking:
            self.params['within_minutes_biking'] = within_minutes_biking
        elif within_minutes_walking:
            self.params['within_minutes_walking'] = within_minutes_walking
        else:
            self.params['within_miles'] = within_miles


class IggyAmenitiesScoreFeature(IggyFeature):
    def __init__(self, api: IggyAPI, within_minutes_driving: float = None,
                 within_minutes_biking: float = None,
                 within_minutes_walking: float = None, within_miles: float = None):
        super().__init__(api)
        if sum([x is None for x in [within_minutes_driving, within_minutes_biking,
                                    within_minutes_walking, within_miles]]) != 3:
            logging.error('Must specify exactly one of `within_miles|minutes_driving|walking|biking')
            raise ValueError
        if within_minutes_driving:
            name_method = 'minutes_driving'
            dist = within_minutes_driving
        elif within_minutes_biking:
            name_method = 'minutes_biking'
            dist = within_minutes_biking
        elif within_minutes_walking:
            name_method = 'minutes_walking'
            dist = within_minutes_walking
        else:
            name_method = 'miles'
            dist = within_miles
        self.name = f'amenities_{name_method}_{dist}'
        self.endpoint = 'amenities_score'
        self.params = {
            f'within_{name_method}': dist
        }
        self.calc = FeatureCalc(result_keys=['score'],
                                calc_method='value')


class IggyFeatureSet():
    """A collection of IggyFeatures"""
    def __init__(self, features: List):
        self.features = features

    def enrich_dataframe(self, df, longitude_col: str = None, latitude_col: str = None):
        """Enrich rows in data frame with this feature set.

        The data frame passed as input can be either a pandas DataFrame
        or geopandas GeoDataFrame object. If the input is a GeoDataFrame,
        points to be enriched will be inferred from the geometry column.
        If the input is a pandas DataFrame, then latitude_col and
        longitude_col must be specified.

        Parameters
        ----------
        df : pd.DataFrame or gpd.GeoDataFrame
            Input data frame
        latitude_col : str
            name of latitude column for pandas DataFrame input
        longitude_col : str
            name of longitude column for pandas DataFrame input

        Returns
        -------
        enriched_df : pd.DataFrame or gpd.GeoDataFrame (same type as input)
        """
        enriched_df = df.copy()
        if isinstance(df, gpd.GeoDataFrame):
            points = df.geometry
        else:
            points = [Point(lng, lat) for lng, lat in zip(df[longitude_col], df[latitude_col])]
            points = gpd.GeoSeries(points)
        for feature in self.features:
            enriched_df[feature.name] = points.apply(lambda p: feature.calculate(p.x, p.y))
        return enriched_df
