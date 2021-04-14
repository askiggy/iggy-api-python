from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="iggyapi",
    packages=find_packages(include=["iggyapi"]),
    version="0.1.4",
    description="Python Library for ask iggy API functionality",
    url='https://github.com/askiggy/iggy-api-python',
    author="Ask Iggy, Inc.",
    author_email="support@askiggy.com",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    setup_requires=["pytest-runner"],
    tests_require=["pytest == 4.4.1"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    test_suite="tests",
    install_requires=['requests', 'geopandas', 'matplotlib',
                      'Shapely', 'pandas', 'contextily'],
    platforms='any'
)
