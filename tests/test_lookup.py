import iggyapi.api as api
import requests_mock

curr_api = api.IggyAPI("test_string")

test_response = {
    "population_density_per_km": {
        "value": 1601,
    },
}


lookup_object = {
    "method": "GET",
    "params": {
        "latitude": 44.976469,
        "longitude": -93.271205,
        "labels": "population_density_per_km",
    },
}

lookup_summary_object = {
    "method": "GET",
    "params": {
        "latitude": 44.976469,
        "longitude": -93.271205,
        "labels": "population_density_per_km",
        "summary_radius_km": 5,
    }
}


lookup_summary_response = {
    "population_density_per_km": {
        "summary": {
            "average": 4921,
            "p10": 2256,
            "p20": 2911,
            "p30": 3155,
            "p40": 3399,
            "p50": 4636,
            "p60": 5873,
            "p70": 6300,
            "p80": 6727,
            "p90": 7871,
            "p99": 8901,
            "percentile": 0.0,
            "radius_km": 1.0,
        },
        "value": 1601,
    },
}


def test_lookup():
    with requests_mock.Mocker() as m:
        m.get("https://api.askiggy.com/v1/lookup?latitude=44.976469&longitude=-93.271205&labels=population_density_per_km", json=test_response)
        assert curr_api.lookup(lookup_object) == test_response


def test_summary_lookup():
    with requests_mock.Mocker() as m:
        m.get("https://api.askiggy.com/v1/lookup?latitude=44.976469&longitude=-93.271205&labels=population_density_per_km&summary_radius_km=5", json=lookup_summary_response)
        assert curr_api.lookup(
            lookup_summary_object) == lookup_summary_response
