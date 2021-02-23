import pytest

import iggyapi.api as api
from iggyapi.iggyfeature import FeatureCalc

curr_api = api.IggyAPI("test_string")

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
    ],
    "waste_management": []
}


def test_featurecalc_value():
    fc_val = FeatureCalc(result_keys=["population_density_per_km", "value"],
                         calc_method="value")
    assert fc_val(test_lookup_response) == 1601


def test_featurecalc_count():
    fc_count = FeatureCalc(result_keys=["bars", "straight_line_distance_miles"],
                           calc_method="count")
    assert fc_count(test_poi_response) == 4


def test_featurecalc_min():
    fc_min = FeatureCalc(result_keys=["bars", "straight_line_distance_miles"],
                         calc_method="min")
    assert fc_min(test_poi_response) == 0.13


def test_featurecalc_max():
    fc_max = FeatureCalc(result_keys=["bars", "straight_line_distance_miles"],
                         calc_method="max")
    assert fc_max(test_poi_response) == 0.28


def test_featurecalc_invalid_method():
    fc_invalid = FeatureCalc(result_keys=["bars", "straight_line_distance_miles"],
                             calc_method="not_supported")
    with pytest.raises(ValueError) as excinfo:
        fc_invalid(test_poi_response)


def test_featurecalc_no_result():
    fc_max = FeatureCalc(result_keys=["waste_management", "straight_line_distance_miles"],
                         calc_method="max")
    assert fc_max(test_poi_response) is None
