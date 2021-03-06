import iggyapi.api as api
import requests_mock

curr_api = api.IggyAPI("test_string")


isochrone_object = {
    "method": "GET",
    "params": {
        "lat": 44.976469,
        "lng": -93.271205,
        "time_limit_minutes": 1,
        "mode": "car",
    },
}

response = {
    "geometry": {
        "coordinates": [
            [
                [-93.27172280515433, 44.97662464510111],
                [-93.27145067269194, 44.97591181078656],
                [-93.27137837047975, 44.97582966407753],
                [-93.27131578560133, 44.9758020969287],
                [-93.27069943630768, 44.97554281671813],
                [-93.27061552414183, 44.97556153630231],
                [-93.27052639656945, 44.97557680999287],
                [-93.27024597533597, 44.97599888539312],
                [-93.27021170266445, 44.976046289713224],
                [-93.27016904808958, 44.976088944288094],
                [-93.27038930588341, 44.97671777330453],
                [-93.27040625595464, 44.97677709855386],
                [-93.27045943447484, 44.9767988915026],
                [-93.27053282269537, 44.97683158092569],
                [-93.27059680455767, 44.97686305962942],
                [-93.27090386161738, 44.9770375894838],
                [-93.27103452617752, 44.9769926997347],
                [-93.27117239350044, 44.97699289005534],
                [-93.27119623535887, 44.977001458223214],
                [-93.27162231544628, 44.97673007081891],
                [-93.2716862973086, 44.976664505708186],
                [-93.27172280515433, 44.97662464510111],
            ],
        ],
        "type": "Polygon",
    },
    "properties": {
        "bucket": 0,
    },
    "type": "Feature",
}


def test_isochrone():
    with requests_mock.Mocker() as m:
        m.get("https://api.askiggy.com/v1/isochrone?lat=44.976469&lng=-93.271205&time_limit_minutes=1&mode=car", json=response)
        assert curr_api.isochrone(isochrone_object, raw_response=True) == response

def test_isochrone_gdf():
    with requests_mock.Mocker() as m:
        m.get("https://api.askiggy.com/v1/isochrone?lat=44.976469&lng=-93.271205&time_limit_minutes=1&mode=car", json=response)
        gdf = curr_api.isochrone(isochrone_object)
        assert gdf.shape[0] == 1
