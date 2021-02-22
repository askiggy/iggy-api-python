import iggyapi.api as api
import requests_mock

curr_api = api.IggyAPI("test_string")

test_response = {
    "warehouses": []
}

poi_options_test_response = {
    "brands": [],
    "labels": []
}


poi_object = {
    "method": "GET",
    "params": {
        "latitude": 44.976469,
        "longitude": -93.271205,
        "labels": "warehouses",
        "within_minutes_driving": 5,
    },
}

poi_post_object = {
    "method": "POST",
    "params": {
        "latitude": 44.976469,
        "longitude": -93.271205,
        "labels": "warehouses",
        "within_minutes_driving": 5,
    },
}


body = {
    "labels": ["warehouses"],
    "geojson": {
        "type": "Polygon",
        "coordinates": [
            [
                [-122.1781826019287, 47.54003487204064],
                [-122.17363357543947, 47.54003487204064],
                [-122.17363357543947, 47.542642203571745],
                [-122.1781826019287, 47.542642203571745],
                [-122.1781826019287, 47.54003487204064],
            ],
        ],
    },
}


def test_get_poi():
    with requests_mock.Mocker() as m:
        m.get("https://api.askiggy.com/v1/points_of_interest?latitude=44.976469&longitude=-93.271205&labels=warehouses&within_minutes_driving=5", json=test_response)
        assert curr_api.poi(poi_object) == test_response


def test_poi_options():
    with requests_mock.Mocker() as m:
        m.get("https://api.askiggy.com/v1/points_of_interest_options",
              json=poi_options_test_response)
        assert curr_api.poi_options() == poi_options_test_response


def test_summary_lookup():
    with requests_mock.Mocker() as m:
        m.post("https://api.askiggy.com/v1/points_of_interest",
               json=test_response)
        assert curr_api.poi(poi_post_object) == test_response
