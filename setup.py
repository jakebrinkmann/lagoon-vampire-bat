"""These tools allow for the independent validation of higher level science products generated from Level-1 Landsat
data that are generated via the EROS Science Processing Architecture (ESPA).

As algorithms are continually developed, it is necessary to perform these validations prior to public release.  This
allows for the identification of unwanted artifacts and the confirmation of desired changes.
The ordering interface via an API is also tested to ensure consistent and expected performance for public use.

Example usage and logical order:

1) order.exe -u USERNAME -env ESPA_ENVIRONMENT -o OUTPUT_DIRECTORY/

2) download.exe -u USERNAME -env ESPA_ENVIRONMENT -o ESPA_ENVIRONMENT/ -i order_123456789.txt

3) validate.exe -m MASTER/ -t TEST/ -o RESULTS/ --verbose --include-nodata

"""

from setuptools import setup, find_packages

setup(
    name="espa_validation",

    version="0.1.0",

    packages=find_packages(),

    install_requires=[
        "matplotlib",
        "numpy",
        "gdal",
        "requests",
        "pandas",
        "lxml",
        "scikit_image",
        "pyyaml"
    ],

    entry_points={"console_scripts": [
        "download = espa_validation.download:main",
        "order = espa_validation.place_order:main",
        "qa = espa_validation.validate:main"
    ]},

    dependency_links=["https://github.com/conda-forge/"],

    python_requires=">=3.5",

    author="Daniel Zelenak, modified from code written by Steve Foga",

    author_email="daniel.zelenak.ctr@usgs.gov",

    long_description=__doc__,

    description="A series of validation tools that can be used to compare the outputs "
                "from different ESPA environments.",

    license="Public Domain",

    url="https://github.com/danzelenak-usgs/Science_Validation"
)
