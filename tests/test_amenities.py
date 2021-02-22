import iggyapi.api as api
import requests_mock

curr_api = api.IggyAPI("test_string")

amenities_object = {
    "method": "GET",
    "params": {
        "latitude": 44.976469,
        "longitude": -93.271205,
        "within_minutes_driving": 3,
    },
}

response = {
    "score": 4
}


def test_amenities():
    with requests_mock.Mocker() as m:
        m.get("https://api.askiggy.com/v1/amenities_score?latitude=44.976469&longitude=-93.271205&within_minutes_driving=3", json=response)
        assert curr_api.amenities(amenities_object) == response
