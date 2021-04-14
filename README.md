# Iggy API Python Library

A Python wrapper for accessing the Iggy API

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [Support & Feedback](#support-feedback)
- [What is Iggy](#what-is-iggy)
- [Licensing](#licensing)
- [Publishing](#licensing)

# Installation

Using `pip`

```bash
pip install iggyapi
```

# Basic API Usage

After installing the package, you can import it into your file like so:

```python
from iggyapi import api

myapi = api.IggyAPI("<your_token_here>")
```

This library currently supports all public endpoints:

```python
options = {
    "method": "GET",
    "params": {
        "latitude": 44.976469,
        "longitude": -93.271205,
        # Other params here. An extensive list can be found at our documentation
    },
};

#  Lookup
myapi.lookup(options)

#  Points of Interest (GET)
myapi.points_of_option(options)

#  Points of Interest (POST)
myapi.points_of_options(options, body)

#  Isochrone
myapi.isochrone(options)

#  Amenities
myapi.amenities(options)

#  Clusters
myapi.clusters(options)

# Points of Interest Options
myapi.points_of_interest_options()
```

For certain endpoints (specifically /isochrone and /clusters), the results come back as a GeoDataFrame by default (for ease of access). If you would instead like the raw response, add the parameter `raw_response=True`.

## Mapping your isochrone and clusters endpoints

If you want to also plot your function, we provided a plot function after calling the api on isochrone or clusters. Simply call

```python
myapi.plot("isochrone")
# or
myapi.plot("clusters")
```

# Enriching data frames with `IggyFeature` and `IggyFeatureSet`

The `IggyFeature` base class and its derived classes make it easy to add new columns containing Iggy-enriched location data to your Pandas or GeoPandas data frames.

Let's say you have some data on homes for sale, and want to add the [amenities score](https://docs.askiggy.com/reference/amenities-score-1) and distance to the [nearest grocery store](https://docs.askiggy.com/reference/points-of-interest) to each point:

```python
import pandas as pd
from iggyapi import iggyfeature

# construct a pandas DataFrame
df = pd.DataFrame(
    {
        'address': ['123 Main St', '555 Orange Drive', '1015 6th Ave'],
        'lat': [27.73926873952831, 27.778781027081127, 27.903761715115724],
        'lng': [-82.69850674919671, -82.69463063223678, -82.812879978314456]
    }
)

# define IggyFeatures and combine them within an IggyFeatureSet
amenities_feature = iggyfeature.IggyAmenitiesScoreFeature(
    myapi,
    within_minutes_driving=10
)
nearest_grocery_feature = iggyfeature.IggyPOIFeature(
    myapi,
    calc_method='min',
    label='grocery_stores',
    within_minutes_driving=10
)
feature_set = iggyfeature.IggyFeatureSet(
    [amenities_feature, nearest_grocery_feature]
)

# enrich the DataFrame
enriched_df = feature_set.enrich_dataframe(
    df,
    longitude_col = 'lng',
    latitude_col = 'lat'
)
enriched_df.head()

#             address        lat        lng  amenities_minutes_driving_10  poi_grocery_stores_min
# 0       123 Main St  27.739269 -82.698507                      0.697528                    0.69
# 1  555 Orange Drive  27.778781 -82.694631                      0.676647                    0.40
# 2      1015 6th Ave  27.903762 -82.812880                      0.655141                    0.85

# ...or as a geopandas GeoDataFrame:
import geopandas as gpd

gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lng, df.lat))
enriched_gdf = feature_set.enrich_dataframe(gdf)
```

The `IggyFeature` class can be used to define a specific piece of information derived from the Iggy API, and the `IggyFeatureSet` can be used to enrich any data with latitude and longitude using a list of Iggy features.

# Documentation

Check out our [documentation website](https://docs.askiggy.com/docs)

# Contributing

Check out our document on [contribution](contributing.md)

# Support & Feedback

If you ever find an issue or problem, please feel free to open up an issue on the issues tab! We'd also love to hear feedback on our [discord server](https://discord.gg/5PAgtu9Sec)!

# What is Iggy?

Iggy is the world's first location enrichment API that makes it easy to integrate relevant location data into your product. It has a level of data that isn’t readily available elsewhere and doesn’t require a specialized geospatial data team to leverage it. Check us out [here](https://www.askiggy.com/)

# Publishing

First, ensure that all tests passed by running ` python setup.py pytest`. From there, run `python setup.py bdist_wheel` to generate an installable .whl file. From there, run `twine upload dist/\*` to upload the package. For a more robust documentation, see the official [packaging page](https://packaging.python.org/tutorials/packaging-projects/).

# Licensing

This project is licensed under the MIT license. See the [LICENSE](LICENSE) file for more info.
