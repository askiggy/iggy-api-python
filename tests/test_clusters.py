from iggypythonlib import api
import requests_mock

curr_api = api.IggyAPI("test_string")

cluster_response = {
    "clusters": [
        {
            "geojson": {
                "geometry": {
                    "coordinates": [
                        [
                            [-93.27951, 44.974911],
                            [-93.276035, 44.972828],
                            [-93.268903, 44.975631],
                            [-93.267602, 44.984578],
                            [-93.269522, 44.985574],
                            [-93.273494, 44.983997],
                            [-93.27951, 44.974911],
                        ],
                    ],
                    "type": "Polygon",
                },
                "properties": {},
                "type": "Feature",
            },
            "summary": {
                "place_names": [
                    "801 Chophouse",
                    "AC Lounge",
                    "Bar Fly Minneapolis",
                    "Breakfast Bar of Minnesota",
                    "Cobble Social House",
                    "Demi",
                    "Fine Line Music Cafe",
                    "Gay 90's",
                    "Gluek's Restaurant & Bar",
                    "HopCat",
                    "Krona Bar & Grill",
                    "Mackenzie Pub",
                    "O'Donovan's Irish Pub",
                    "Prohibition",
                    "Red Cow Minneapolis",
                    "REV Ultra Lounge",
                    "Sphere",
                    "The Bulldog Downtown",
                    "The Exchange & Alibi Lounge",
                    "The Library Lounge",
                    "The Living Room",
                    "The Marquette Lounge",
                    "The News Room",
                    "The Saloon",
                    "Union Rooftop",
                    "Wild Gregs Saloon",
                ],
            },
        },
        {
            "geojson": {
                "geometry": {
                    "coordinates": [
                        [
                            [-93.261036, 44.980433],
                            [-93.265968, 44.981333],
                            [-93.264066, 44.979588],
                            [-93.260729, 44.97699],
                            [-93.258623, 44.976678],
                            [-93.259339, 44.978562],
                            [-93.261036, 44.980433],
                        ],
                    ],
                    "type": "Polygon",
                },
                "properties": {},
                "type": "Feature",
            },
            "summary": {
                "place_names": ["Crooked Pint Ale House", "eagleBOLTbar"],
            },
        },
        {
            "geojson": {
                "geometry": {
                    "coordinates": [
                        [
                            [-93.288511, 44.949467],
                            [-93.288817, 44.948025],
                            [-93.28836, 44.947666],
                            [-93.287667, 44.949261],
                            [-93.288511, 44.949467],
                        ],
                    ],
                    "type": "Polygon",
                },
                "properties": {},
                "type": "Feature",
            },
            "summary": {
                "place_names": ["The Lyndale Tap House"],
            },
        },
        {
            "geojson": {
                "geometry": {
                    "coordinates": [
                        [
                            [-93.246947, 44.973182],
                            [-93.248073, 44.972935],
                            [-93.24745, 44.968726],
                            [-93.246915, 44.968723],
                            [-93.246947, 44.973182],
                        ],
                    ],
                    "type": "Polygon",
                },
                "properties": {},
                "type": "Feature",
            },
            "summary": {
                "place_names": [
                    "Bullwinkle's Saloon & Funbar",
                    "Part Wolf",
                    "The Red Sea",
                ],
            },
        },
        {
            "geojson": {
                "geometry": {
                    "coordinates": [
                        [
                            [-93.252096, 44.990528],
                            [-93.255012, 44.989145],
                            [-93.257667, 44.987806],
                            [-93.258187, 44.987146],
                            [-93.258232, 44.987033],
                            [-93.252929, 44.988878],
                            [-93.252096, 44.990528],
                        ],
                    ],
                    "type": "Polygon",
                },
                "properties": {},
                "type": "Feature",
            },
            "summary": {
                "place_names": ["Ground Zero Nightclub"],
            },
        },
        {
            "geojson": {
                "geometry": {
                    "coordinates": [
                        [
                            [-93.296333, 44.949429],
                            [-93.297999, 44.951108],
                            [-93.297947, 44.949408],
                            [-93.296649, 44.949168],
                            [-93.296333, 44.949429],
                        ],
                    ],
                    "type": "Polygon",
                },
                "properties": {},
                "type": "Feature",
            },
            "summary": {
                "place_names": ["Mansion at Uptown"],
            },
        },
    ],
}

cluster_object = {
    "method": "GET",
    "params": {
        "latitude": 44.976469,
        "longitude": -93.271205,
        "category": "restaurants",
        "within_miles": 3,
    },
}


def test_cluster_endpoint():
    with requests_mock.Mocker() as m:
        m.get("https://api.askiggy.com/v1/clusters?latitude=44.976469&longitude=-93.271205&category=restaurants&within_miles=3",
              json=cluster_response)
        assert curr_api.clusters(cluster_object) == cluster_response
