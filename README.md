# @ask-iggy/iggypythonlib

A Python wrapper for accessing the Iggy API

## Table of Contents

-   [Installation](#installation)
-   [Usage](#usage)
-   [Contributing](#contributing)
-   [Support & Feedback](#support-feedback)
-   [What is Iggy](#what-is-iggy)
-   [Licensing](#licensing)
-   [Publishing](#licensing)

# Installation

Using `pip`

```bash
pip install iggy-python
```

# Usage

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
        # Other params here
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

#  Cluters
myapi.clusters(options)

# Points of Interest Options
myapi.points_of_interest_options()
```

# Documentation

Check out our [documentation website](https://docs.askiggy.com/docs)

# Contributing

Check out our document on [contribution](contributing.md)

# Support & Feedback

If you ever find an issue or problem, please feel free to open up an issue on the issues tab! We'd also love to hear feedback on our [discord server](https://discord.gg/5PAgtu9Sec)!

# What is Iggy?

Iggy is the world's first location enrichment API that makes it easy to integrate relevant location data into your product. It has a level of data that isn’t readily available elsewhere and doesn’t require a specialized geospatial data team to leverage it. Check us out [here](https://www.askiggy.com/)

# Publishing

First, ensure that all tests passed by running ` python setup.py pytest`. From there, run `python setup.py bdist_wheel` to generate an installable .whl file. From there, run twine upload dist/\* to upload the package. For a more robust documentation, see the official [packaging page](https://packaging.python.org/tutorials/packaging-projects/).

# Licensing

This project is licensed under the MIT license. See the [LICENSE](LICENSE) file for more info.
