import geopandas as gpd
import pandas as pd
import pytest
from unittest.mock import MagicMock

import iggyapi.api as api
from iggyapi.iggyfeature import \
    FeatureCalc, IggyFeature, \
    IggyLookupFeature, IggyPOIFeature, \
    IggyAmenitiesScoreFeature, IggyFeatureSet

test_latitude = 44.976469
test_longitude = -93.271205
err_response = {
    "message":"Invalid location. Ensure your location is close to a road."
}

test_lookup_response = {
    "population_density_per_km": {
        "value": 1601,
    },
}

test_poi_response = {
    "bars": [
        {
            "name": "The Living Room",
            "straight_line_distance_miles": 0.13
        },
        {
            "name": "The Saloon",
            "straight_line_distance_miles": 0.28
        },
        {
            "name": "The News Room",
            "straight_line_distance_miles": 0.24
        },
        {
            "name": "Union Rooftop",
            "straight_line_distance_miles": 0.21
        }
    ]
}

test_df = pd.DataFrame(
    {
        'lat': [27.73926873952831, 27.778781027081127, 27.903761715115724],
        'lng': [-82.69850674919671, -82.69463063223678, -82.812879978314456]
    }
)

def test_iggyfeature_lookup_value():
    label = "population_density_per_km"
    curr_api = api.IggyAPI("test_string")
    curr_api.enrich = MagicMock(return_value=test_lookup_response)
    f = IggyFeature(curr_api, "poi_popdensity_value", "lookup",
                    params={"labels": label},
                    calc=FeatureCalc([label, "value"]))
    result = f.calculate(test_longitude, test_latitude)
    assert result == 1601


def test_iggyfeature_lookup_badcoords():
    label = "population_density_per_km"
    curr_api = api.IggyAPI("test_string")
    curr_api.enrich = MagicMock(return_value=err_response)
    f = IggyFeature(curr_api, "poi_popdensity_value", "lookup",
                    params={"labels": label},
                    calc=FeatureCalc([label, "value"]))
    result = f.calculate(-test_longitude, test_latitude)
    assert result is None


def test_iggylookup_popdensity():
    label = "population_density_per_km"
    curr_api = api.IggyAPI("test_string")
    curr_api.enrich = MagicMock(return_value=test_lookup_response)
    f = IggyLookupFeature(curr_api, "value", label=label)
    result = f.calculate(test_longitude, test_latitude)
    assert result == 1601


def test_iggypoi_bars():
    label = "bars"
    curr_api = api.IggyAPI("test_string")
    curr_api.enrich = MagicMock(return_value=test_poi_response)
    f = IggyPOIFeature(curr_api, calc_method="min", label=label,
                       within_minutes_walking=5)
    result = f.calculate(test_longitude, test_latitude)
    assert result == 0.13

    f = IggyPOIFeature(curr_api, calc_method="count", label=label,
                       within_minutes_walking=5)
    result = f.calculate(test_longitude, test_latitude)
    assert result == 4


def test_iggypoi_conflictinput():
    label = "bars"
    curr_api = api.IggyAPI("test_string")
    curr_api.enrich = MagicMock(return_value=test_poi_response)
    with pytest.raises(ValueError) as excinfo:
        f = IggyPOIFeature(curr_api, calc_method="min", label=label,
                           brand="some brand",
                           within_minutes_walking=5)
    with pytest.raises(ValueError) as excinfo:
        f = IggyPOIFeature(curr_api, calc_method="min", label=label,
                           within_minutes_walking=5,
                           within_minutes_driving=30)


def test_iggyamenities():
    curr_api = api.IggyAPI("test_string")
    curr_api.enrich = MagicMock(return_value={"score": 0.5})
    f = IggyAmenitiesScoreFeature(curr_api, within_minutes_biking=10)
    result = f.calculate(test_longitude, test_latitude)
    assert result == 0.5


def test_iggyfeatureset():
    local_api_1 = api.IggyAPI("test_token")
    f1 = IggyPOIFeature(local_api_1, calc_method="min", label="bars",
                        within_minutes_walking=5)
    local_api_1.enrich = MagicMock(return_value=test_poi_response)
    local_api_2 = api.IggyAPI("test_token")
    f2 = IggyLookupFeature(local_api_2, "value", label="population_density_per_km")
    local_api_2.enrich = MagicMock(return_value=test_lookup_response)

    fs = IggyFeatureSet([f1, f2])
    df_out = fs.enrich_dataframe(test_df, longitude_col='lng', latitude_col='lat')
    assert df_out.shape == (3, 4)
    assert df_out.poi_bars_min.iloc[0] == 0.13

    gdf = gpd.GeoDataFrame(test_df,
                           geometry=gpd.points_from_xy(test_df.lng, test_df.lat))
    gdf_out = fs.enrich_dataframe(gdf)
    assert gdf_out.shape == (3, 5)
    assert gdf_out.lookup_population_density_per_km_value.iloc[0] == 1601

